"""Adapter base — one module per (service, version).

Adding support for a new version means adding a module here and listing it
in `adapters/__init__.py`. It never means adding a branch to a request
builder: the versions of a single service diverge far more than they look.
Inventory is the worked example —

    1.2.1  namespace .../WSDL/InventoryService/1.0.0/   root <Request>
           productID + required productIDtype, quantityAvailable a scalar,
           errors as a bare <errorMessage>, no warehouse breakdown at all
    2.0.0  namespace .../WSDL/Inventory/2.0.0/          root <GetInventoryLevelsRequest>
           productId, quantityAvailable a <Quantity> complex with a uom,
           errors as a ServiceMessageArray, full InventoryLocationArray

— four incompatible spellings, two different error channels, and one
capability that simply does not exist in the older version.

Note especially that **1.2.1's namespace says `InventoryService/1.0.0`**.
The namespace does not track the service version, so `NAMESPACES` is a
constant owned by each adapter and must never be interpolated from the
configured `wsVersion`.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

import soap
from schemas import Source


class Adapter:
    """Base class for a single service version."""

    #: canonical service code, e.g. "INV"
    SERVICE: str = ""
    #: exact version string as the registry reports it, e.g. "2.0.0"
    VERSION: str = ""
    #: prefix -> namespace URI, declared on the envelope
    NAMESPACES: dict[str, str] = {}
    #: prefix that auth elements (wsVersion/id/password) live under
    AUTH_PREFIX: str = "ns"
    #: operations this adapter implements, in canonical (camelCase) spelling
    OPERATIONS: tuple[str, ...] = ()

    def __init__(self, config, endpoint, client: soap.SoapClient | None = None,
                 *, use_test: bool = False) -> None:
        self.config = config
        self.endpoint = endpoint
        self.client = client or soap.SoapClient()
        self.use_test = use_test

    # -- helpers -----------------------------------------------------------

    @property
    def url(self) -> str:
        return self.endpoint.resolve_url(use_test=self.use_test)

    def source(self, operation: str) -> Source:
        return Source(
            supplier=self.config.supplier,
            service=self.SERVICE,
            version=self.VERSION,
            operation=operation,
        )

    def auth_xml(self) -> str:
        """The wsVersion/id/password triple every operation begins with.

        `wsVersion` is sent as this adapter's VERSION rather than whatever
        the config says, so a config typo cannot produce a request that
        claims one version while using another's element names.

        `password` is omitted entirely when unset — it is `minOccurs="0"`
        in every spec, and an empty element is not the same as an absent
        one to several suppliers.
        """
        cred_id, password = self.config.require_credentials()
        prefix = self.AUTH_PREFIX
        return (
            soap.element(f"{prefix}:wsVersion", self.VERSION)
            + soap.element(f"{prefix}:id", cred_id)
            + soap.element(f"{prefix}:password", password)
        )

    @property
    def namespaces(self) -> dict[str, str]:
        """Adapter defaults, with any per-supplier override merged over them.

        Overrides exist because compliance is not universal — 3M serves
        Inventory 1.2.1 under its own `promostandards.mmm` namespace. The
        default remains the spec's, so an override is always a deliberate
        per-supplier act recorded in that supplier's config.
        """
        overrides = getattr(self.endpoint, "namespaces", None) or {}
        return {**self.NAMESPACES, **overrides}

    def post(self, soap_action: str, body_xml: str, *,
             idempotent: bool = True) -> ET.Element:
        envelope = soap.build_envelope(body_xml, namespaces=self.namespaces)
        return self.client.call(self.url, soap_action, envelope,
                                idempotent=idempotent)

    # -- error channels ----------------------------------------------------

    @staticmethod
    def service_messages(root: ET.Element) -> list[dict]:
        """Collect ServiceMessage entries (2.x services) into plain dicts."""
        messages = []
        for node in soap.find_all(root, "ServiceMessage"):
            messages.append({
                "code": soap.text(node, "code"),
                "description": soap.text(node, "description"),
                "severity": soap.text(node, "severity"),
            })
        return messages

    @classmethod
    def raise_on_error(cls, root: ET.Element) -> list[dict]:
        """Raise if the supplier reported an error; return any warnings.

        Handles both channels the specs use: a `ServiceMessageArray` with
        per-message severity, and the older bare `errorMessage` element.
        Messages that are not error-severity are returned so a caller can
        surface them alongside good data rather than losing them.
        """
        from errors import ServiceMessageError

        messages = cls.service_messages(root)
        errors = [
            m for m in messages
            if (m.get("severity") or "").strip().lower() in ("error", "fatal")
        ]
        if errors:
            first = errors[0]
            raise ServiceMessageError(
                first.get("description") or "service returned an error",
                code=first.get("code"),
                severity=first.get("severity"),
                messages=messages,
            )

        legacy = soap.text(root, "errorMessage")
        if legacy:
            raise ServiceMessageError(legacy, messages=messages)

        return messages
