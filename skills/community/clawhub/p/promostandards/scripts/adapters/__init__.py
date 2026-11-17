"""Adapter registry: (service, version) -> adapter class.

Registration is an explicit table rather than import-time scanning so that
the set of supported versions is greppable, and so a missing adapter fails
loudly at lookup instead of silently falling back to a near-miss version.
Version strings are matched exactly as the registry reports them.
"""

from __future__ import annotations

from adapters.base import Adapter
from adapters.inventory_1_2_1 import Inventory121
from adapters.inventory_2_0_0 import Inventory200
from adapters.pricing_1_0_0 import Pricing100
from adapters.product_1_0_0 import Product100
from adapters.product_2_0_0 import Product200
from adapters.purchase_order_1_0_0 import PurchaseOrder100

ADAPTERS: dict[tuple[str, str], type[Adapter]] = {
    ("INV", "1.2.1"): Inventory121,
    ("INV", "2.0.0"): Inventory200,
    ("PRODUCT", "1.0.0"): Product100,
    ("PRODUCT", "2.0.0"): Product200,
    ("PPC", "1.0.0"): Pricing100,
    ("PO", "1.0.0"): PurchaseOrder100,
}


def versions_for(service: str) -> list[str]:
    """Every version of `service` this package can drive."""
    return sorted(v for (s, v) in ADAPTERS if s == service.upper())


def supported_services() -> list[str]:
    return sorted({s for (s, _) in ADAPTERS})


def get_adapter_class(service: str, version: str) -> type[Adapter]:
    """Look up an adapter, or raise NotSupportedError naming what exists.

    Deliberately strict about the version: a supplier on Inventory 1.2.1
    served by the 2.0.0 adapter would send the wrong namespace and the
    wrong element names, and the failure would surface as an empty result
    rather than an error.
    """
    from errors import NotSupportedError

    key = (service.upper(), str(version))
    adapter = ADAPTERS.get(key)
    if adapter is None:
        available = versions_for(service)
        if available:
            message = (
                f"no adapter for {service.upper()} version {version}; "
                f"this package implements {', '.join(available)}"
            )
        else:
            message = (
                f"no adapter for service '{service.upper()}'; "
                f"this package implements {', '.join(supported_services())}"
            )
        raise NotSupportedError(message, service=service.upper(),
                                version=str(version), available=available)
    return adapter


def build(config, service: str, client=None, *, use_test: bool = False):
    """Resolve config + registry into a ready adapter instance.

    Raises NotSupportedError when the supplier does not publish the service
    (from the config) or when we have no adapter for the version they run.
    Both are structural facts known before any request goes out.
    """
    from config import normalize_service

    code = normalize_service(service)
    endpoint = config.endpoint(code)
    adapter_cls = get_adapter_class(code, endpoint.ws_version)
    return adapter_cls(config, endpoint, client, use_test=use_test)
