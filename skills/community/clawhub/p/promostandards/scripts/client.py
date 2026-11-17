"""The caller-facing client.

One object per supplier. Every method returns canonical shapes and raises
the structured errors in `errors.py` — PromoStandards vocabulary does not
cross this boundary.

The client never guesses which version a supplier runs: it reads that from
the config (which provisioning derived from the registry) and dispatches to
the matching adapter. A supplier on a version with no adapter raises
NotSupportedError naming what is implemented, rather than being served by
a near-miss adapter that would send the wrong element names and return an
empty result.
"""

from __future__ import annotations

import adapters
import soap
from config import SupplierConfig
from schemas import InventoryResult, PriceGrid, Product, PurchaseOrderResult


class PromoStandardsClient:
    def __init__(self, config: SupplierConfig, *, session: object | None = None,
                 timeout: int = soap.DEFAULT_TIMEOUT,
                 use_test: bool = False) -> None:
        self.config = config
        self.soap = soap.SoapClient(session, timeout=timeout)
        self.use_test = use_test

    # -- construction ------------------------------------------------------

    @classmethod
    def from_file(cls, path: str, **kwargs) -> "PromoStandardsClient":
        return cls(SupplierConfig.load(path), **kwargs)

    @classmethod
    def from_dict(cls, raw: dict, **kwargs) -> "PromoStandardsClient":
        return cls(SupplierConfig.from_dict(raw), **kwargs)

    # -- introspection -----------------------------------------------------

    def adapter(self, service: str):
        return adapters.build(self.config, service, self.soap,
                              use_test=self.use_test)

    def capabilities(self) -> dict:
        """What this configured supplier can do, without calling anything."""
        result = {}
        for service, endpoint in sorted(self.config.services.items()):
            # `testUrlIsProduction` is reported alongside `hasTestEndpoint`
            # so a caller can distinguish "no test endpoint registered" from
            # "one is registered but it is production" — the second reads as
            # a supplier that supports test submissions until you look.
            entry = {
                "version": endpoint.ws_version,
                "hasTestEndpoint": endpoint.has_test_endpoint,
            }
            if endpoint.test_url_is_production:
                entry["testUrlIsProduction"] = True
            try:
                adapter_cls = adapters.get_adapter_class(
                    service, endpoint.ws_version
                )
                entry["supported"] = True
                entry["operations"] = list(adapter_cls.OPERATIONS)
            except Exception:  # noqa: BLE001 - NotSupportedError only
                entry["supported"] = False
                entry["operations"] = []
            result[service] = entry
        return result

    # -- inventory ---------------------------------------------------------

    def get_inventory(self, product_id: str, **kwargs) -> InventoryResult:
        return self.adapter("INV").get_inventory_levels(product_id, **kwargs)

    def get_inventory_filters(self, product_id: str) -> dict:
        return self.adapter("INV").get_filter_values(product_id)

    # -- product data ------------------------------------------------------

    def get_product(self, product_id: str, **kwargs) -> Product:
        return self.adapter("PRODUCT").get_product(product_id, **kwargs)

    def get_products_modified_since(self, timestamp: str) -> dict:
        return self.adapter("PRODUCT").get_product_date_modified(timestamp)

    def get_closeout_products(self, **kwargs) -> dict:
        return self.adapter("PRODUCT").get_product_close_out(**kwargs)

    # -- pricing -----------------------------------------------------------

    def get_fob_points(self, product_id: str | None = None) -> list[dict]:
        return self.adapter("PPC").get_fob_points(product_id)

    def get_pricing(self, product_id: str, *, fob_id: str | None = None,
                    **kwargs) -> list[PriceGrid]:
        """Configured pricing, resolving a FOB point when none is given.

        PPC requires a supplier-specific `fobId`; rather than fail, this
        fetches the supplier's FOB points and uses the first. Callers that
        care which warehouse the price is quoted from should pass one.
        """
        adapter = self.adapter("PPC")
        if not fob_id:
            points = adapter.get_fob_points(product_id)
            if not points:
                from errors import NotSupportedError
                raise NotSupportedError(
                    f"supplier '{self.config.supplier}' returned no FOB "
                    "points, so configured pricing cannot be requested",
                    supplier=self.config.supplier, service="PPC",
                )
            fob_id = points[0]["fob_id"]
        return adapter.get_configuration_and_pricing(
            product_id, fob_id=fob_id, **kwargs
        )

    def get_decoration_locations(self, product_id: str) -> list:
        return self.adapter("PPC").get_available_locations(product_id)

    # -- purchase order ----------------------------------------------------

    def send_purchase_order(self, po: dict, *, allow_production: bool = False
                            ) -> PurchaseOrderResult:
        """Submit a PO. Defaults to the supplier's test endpoint.

        `allow_production=True` is required to reach production, and is
        deliberately not the default — see `adapters/purchase_order_1_0_0`.
        """
        return self.adapter("PO").send_po(po, allow_production=allow_production)

    def preview_purchase_order(self, po: dict) -> str:
        """Render the PO XML without sending it — a dry run."""
        return self.adapter("PO").build_po_xml(po)
