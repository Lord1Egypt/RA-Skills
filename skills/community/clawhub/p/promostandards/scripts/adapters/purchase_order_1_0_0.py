"""Purchase Order 1.0.0 — `sendPO`, `getSupportedOrderTypes`.

468 suppliers publish PO, all at 1.0.0, so one adapter covers the service.

**This is the only write in the package, and it is treated as one.** Three
rules are enforced here rather than left to the caller:

1. **Production submission requires an explicit opt-in.** `send_po` targets
   the supplier's registered test endpoint by default. Reaching production
   takes `allow_production=True`, a non-default argument that has to be
   typed deliberately.
2. **A missing test endpoint is a refusal, not a fallback.** If a supplier
   registers no TestURL, a test-mode submission raises instead of quietly
   posting a real order to production — the failure mode that turns a
   development run into a real purchase. A TestURL that is *identical to*
   the production URL counts as missing, since honouring it would post that
   real order while reporting a successful test.
3. **`sendPO` is never retried.** A request that timed out may still have
   been received; retrying risks a duplicate order. On an ambiguous
   failure the result is `accepted=None` and an `EscalationRequired` that
   names the PO, because only a human can check whether the order landed.
"""

from __future__ import annotations

import soap
from adapters.base import Adapter
from errors import (
    ConfigError,
    EscalationRequired,
    ServiceMessageError,
    SoapFaultError,
    TransportError,
)
from schemas import PurchaseOrderResult

NS = "http://www.promostandards.org/WSDL/PO/1.0.0/"
NS_SHARED = "http://www.promostandards.org/WSDL/PO/1.0.0/SharedObjects/"


class PurchaseOrder100(Adapter):
    SERVICE = "PO"
    VERSION = "1.0.0"
    NAMESPACES = {"ns": NS, "shar": NS_SHARED}
    AUTH_PREFIX = "shar"
    OPERATIONS = ("sendPO", "getSupportedOrderTypes")

    def get_supported_order_types(self) -> dict:
        body = (
            "<ns:GetSupportedOrderTypesRequest>"
            + self.auth_xml()
            + "</ns:GetSupportedOrderTypesRequest>"
        )
        root = self.post("getSupportedOrderTypes", body)
        messages = self.raise_on_error(root)
        return {
            "order_types": [e.text for e in soap.find_all(root, "orderType")
                            if e.text],
            "messages": messages,
            "source": self.source("getSupportedOrderTypes").to_dict(),
        }

    # -- submission --------------------------------------------------------

    def send_po(self, po: dict, *, allow_production: bool = False
                ) -> PurchaseOrderResult:
        """Submit a purchase order.

        `po` is the canonical order dict (see `build_po_xml` for the fields
        consumed). Returns a PurchaseOrderResult; raises EscalationRequired
        when the outcome cannot be determined.
        """
        order_number = po.get("order_number") or po.get("po_number")
        if not order_number:
            raise ConfigError("purchase order requires 'order_number'")

        use_test = not allow_production
        if use_test and not self.endpoint.has_test_endpoint:
            if self.endpoint.test_url_is_production:
                reason = (
                    "registers a test endpoint for PO that is the SAME URL as "
                    "production, so there is no such thing as a test "
                    "submission for this supplier — every PO is a real order"
                )
            else:
                reason = (
                    "registers no test endpoint for PO, so a test submission "
                    "cannot be made"
                )
            raise ConfigError(
                f"supplier '{self.config.supplier}' {reason}. Pass "
                f"allow_production=True to submit a REAL order to "
                f"{self.endpoint.url}, or obtain a test endpoint first."
            )

        target = self.endpoint.resolve_url(use_test=use_test)
        body = (
            "<ns:SendPORequest>"
            + self.auth_xml()
            + self.build_po_xml(po)
            + "</ns:SendPORequest>"
        )
        envelope = soap.build_envelope(body, namespaces=self.namespaces)

        try:
            # idempotent=False: never retry a write.
            root = self.client.call(target, "sendPO", envelope,
                                    idempotent=False)
        except (TransportError, SoapFaultError) as exc:
            # The request left the process; we cannot know whether the
            # supplier recorded it. This is the ambiguous case.
            raise EscalationRequired(
                f"sendPO for PO '{order_number}' failed with no confirmation "
                f"from {self.config.supplier}: {exc}. The order may or may "
                f"not have been received — do not resubmit without checking "
                f"with the supplier.",
                supplier=self.config.supplier,
                po_number=str(order_number),
                context={"endpoint": target, "is_test": use_test,
                         "underlying": exc.as_dict()},
            ) from exc

        try:
            messages = self.raise_on_error(root)
        except ServiceMessageError as exc:
            # An explicit, well-formed rejection: unambiguous, so it is a
            # result rather than an escalation. The caller decides.
            return PurchaseOrderResult(
                accepted=False,
                po_number=str(order_number),
                messages=exc.messages or [{"description": str(exc),
                                           "code": exc.code}],
                submitted_to=target,
                is_test=use_test,
                source=self.source("sendPO"),
            )

        transaction_id = soap.text(root, "transactionId")
        return PurchaseOrderResult(
            accepted=True,
            po_number=str(order_number),
            sales_order_number=transaction_id,
            messages=messages,
            submitted_to=target,
            is_test=use_test,
            source=self.source("sendPO"),
        )

    # -- payload -----------------------------------------------------------

    def build_po_xml(self, po: dict) -> str:
        """Render the canonical order dict into a PO 1.0.0 `<PO>` element.

        Exposed separately so a caller can inspect exactly what would be
        sent — a dry run for the one operation that cannot be un-done.
        """
        lines = "".join(
            self._line_item_xml(index, line)
            for index, line in enumerate(po.get("lines") or [], start=1)
        )
        if not lines:
            raise ConfigError("purchase order has no line items")

        contacts = "".join(
            self._contact_xml(c) for c in (po.get("contacts") or [])
        )
        shipments = "".join(
            self._shipment_xml(s) for s in (po.get("shipments") or [])
        )
        if not shipments:
            raise ConfigError(
                "purchase order requires at least one shipment (ShipmentArray "
                "is mandatory in PO 1.0.0)"
            )

        return (
            "<ns:PO>"
            + soap.element("ns:orderType", po.get("order_type") or "Blank")
            + soap.element("ns:orderNumber",
                           po.get("order_number") or po.get("po_number"))
            + soap.element("ns:orderDate", po.get("order_date"))
            + soap.element("ns:totalAmount", po.get("total_amount"))
            + soap.element("ns:paymentTerms", po.get("payment_terms"))
            + soap.element("ns:rush",
                           "true" if po.get("rush") else "false")
            + soap.element("shar:currency", po.get("currency") or "USD")
            + (f"<ns:OrderContactArray>{contacts}</ns:OrderContactArray>"
               if contacts else "")
            + f"<ns:ShipmentArray>{shipments}</ns:ShipmentArray>"
            + f"<ns:LineItemArray>{lines}</ns:LineItemArray>"
            + soap.element("ns:termsAndConditions",
                           po.get("terms_and_conditions") or "")
            + soap.element("ns:salesChannel", po.get("sales_channel"))
            + soap.element("ns:promoCode", po.get("promo_code"))
            + "</ns:PO>"
        )

    def _line_item_xml(self, index: int, line: dict) -> str:
        quantity = line.get("quantity")
        quantity_xml = ""
        if quantity is not None:
            quantity_xml = (
                "<shar:Quantity>"
                + soap.element("shar:value", quantity)
                + soap.element("shar:uom", line.get("uom") or "EA")
                + "</shar:Quantity>"
            )
        parts = "".join(
            "<shar:Part>"
            + soap.element("shar:partId", p.get("part_id"))
            + soap.element("shar:partQuantity", p.get("quantity"))
            + "</shar:Part>"
            for p in (line.get("parts") or [])
        )
        return (
            "<ns:LineItem>"
            + soap.element("ns:lineNumber", line.get("line_number") or index)
            + soap.element("ns:lineReferenceId", line.get("reference_id"))
            + soap.element("shar:description", line.get("description"))
            + soap.element("ns:lineType", line.get("line_type") or "New")
            + quantity_xml
            + soap.element("shar:fobId", line.get("fob_id"))
            + soap.element("ns:allowPartialShipments",
                           "true" if line.get("allow_partial_shipments")
                           else "false")
            + soap.element("shar:unitPrice", line.get("unit_price"))
            + soap.element("ns:lineItemTotal", line.get("line_total"))
            + soap.element("ns:requestedShipDate", line.get("ship_date"))
            + soap.element("ns:requestedInHandsDate", line.get("in_hands_date"))
            + soap.element("shar:productId", line.get("product_id"))
            + (f"<ns:PartArray>{parts}</ns:PartArray>" if parts else "")
            + "</ns:LineItem>"
        )

    @staticmethod
    def _contact_xml(contact: dict) -> str:
        return (
            "<shar:Contact>"
            + soap.element("shar:contactName", contact.get("name"))
            + soap.element("shar:contactType", contact.get("type") or "Buyer")
            + soap.element("shar:contactEmail", contact.get("email"))
            + soap.element("shar:contactPhone", contact.get("phone"))
            + "</shar:Contact>"
        )

    @staticmethod
    def _shipment_xml(shipment: dict) -> str:
        address = shipment.get("address") or {}
        return (
            "<shar:Shipment>"
            + soap.element("shar:shipmentId", shipment.get("shipment_id"))
            + soap.element("shar:shipmentReferenceNumber",
                           shipment.get("reference"))
            + "<shar:ShipTo>"
            + soap.element("shar:customerPickup",
                           "true" if shipment.get("customer_pickup")
                           else "false")
            + soap.element("shar:companyName", address.get("company"))
            + soap.element("shar:attentionTo", address.get("attention_to"))
            + soap.element("shar:address1", address.get("address1"))
            + soap.element("shar:address2", address.get("address2"))
            + soap.element("shar:city", address.get("city"))
            + soap.element("shar:region", address.get("state"))
            + soap.element("shar:postalCode", address.get("postal_code"))
            + soap.element("shar:country", address.get("country") or "US")
            + "</shar:ShipTo>"
            + "</shar:Shipment>"
        )
