"""Canonical model — the only shapes a caller ever sees.

Every adapter, for every supplier and every service version, normalises
into these dataclasses. PromoStandards field names (`partId` vs `partID`,
`quantityAvailable` as a scalar vs a `Quantity` complex, `attributeColor`
vs `partColor`) stop at the adapter boundary and never reach a caller.

Two conventions hold throughout:

- **Every field is optional.** The specs mark most elements optional and
  suppliers omit them freely, so each field defaults to None or an empty
  list. Absent means absent; it is never inferred, defaulted to zero, or
  back-filled from another field.
- **The shape is stable.** `to_dict()` always emits every key, with None
  for what the supplier did not send. A caller can index without guarding,
  and can tell "supplier said 0" from "supplier said nothing" — a
  distinction that matters for inventory.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any


def _clean(value: Any) -> Any:
    """Recursively convert dataclasses to plain dicts, preserving None."""
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {k: _clean(v) for k, v in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    return value


@dataclass
class _Base:
    def to_dict(self) -> dict:
        return {k: _clean(v) for k, v in dataclasses.asdict(self).items()}


# ---------------------------------------------------------------------------
# provenance
# ---------------------------------------------------------------------------

@dataclass
class Source(_Base):
    """Where a normalised record came from.

    Kept on every top-level result so a caller (or a bug report) can tell
    which supplier, service and version produced a given shape — essential
    when two suppliers disagree about completeness.
    """

    supplier: str | None = None
    service: str | None = None
    version: str | None = None
    operation: str | None = None


# ---------------------------------------------------------------------------
# inventory
# ---------------------------------------------------------------------------

@dataclass
class LocationStock(_Base):
    """Stock at one named warehouse.

    Only Inventory 2.0.0 reports this. Inventory 1.2.1 has no location
    breakdown in its schema at all, so adapters for that version leave
    `InventoryLevel.locations` empty — that emptiness means "this version
    cannot say", not "zero warehouses".
    """

    location_id: str | None = None
    name: str | None = None
    postal_code: str | None = None
    country: str | None = None
    quantity: float | None = None
    uom: str | None = None


@dataclass
class InventoryLevel(_Base):
    """Available stock for one part (a style/color/size combination)."""

    part_id: str | None = None
    product_id: str | None = None
    color: str | None = None
    size: str | None = None
    description: str | None = None
    quantity: float | None = None
    uom: str | None = None
    locations: list[LocationStock] = field(default_factory=list)
    lead_time_days: int | None = None
    is_main_part: bool | None = None
    buy_to_order: bool | None = None
    last_modified: str | None = None
    # True only when the source version can report per-warehouse stock.
    locations_supported: bool = False


@dataclass
class InventoryResult(_Base):
    product_id: str | None = None
    levels: list[InventoryLevel] = field(default_factory=list)
    messages: list[dict] = field(default_factory=list)
    source: Source | None = None


# ---------------------------------------------------------------------------
# product data
# ---------------------------------------------------------------------------

@dataclass
class Part(_Base):
    """One orderable variant of a product."""

    part_id: str | None = None
    description: str | None = None
    color: str | None = None
    size: str | None = None
    country_of_origin: str | None = None
    primary_material: str | None = None
    gtin: str | None = None
    unspsc: str | None = None
    lead_time_days: int | None = None
    is_closeout: bool | None = None
    is_caution: bool | None = None
    caution_comment: str | None = None
    is_hazmat: bool | None = None
    is_rush_service: bool | None = None
    effective_date: str | None = None
    end_date: str | None = None
    weight: float | None = None
    weight_uom: str | None = None
    dimensions: dict | None = None


@dataclass
class Product(_Base):
    product_id: str | None = None
    name: str | None = None
    brand: str | None = None
    description: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    categories: list[dict] = field(default_factory=list)
    marketing_points: list[str] = field(default_factory=list)
    primary_image_url: str | None = None
    line_name: str | None = None
    is_closeout: bool | None = None
    is_caution: bool | None = None
    caution_comment: str | None = None
    effective_date: str | None = None
    end_date: str | None = None
    last_change_date: str | None = None
    parts: list[Part] = field(default_factory=list)
    messages: list[dict] = field(default_factory=list)
    source: Source | None = None


# ---------------------------------------------------------------------------
# pricing & configuration
# ---------------------------------------------------------------------------

@dataclass
class PriceBreak(_Base):
    min_quantity: float | None = None
    price: float | None = None
    discount_code: str | None = None
    uom: str | None = None


@dataclass
class PriceGrid(_Base):
    """Quantity-break pricing for one part."""

    part_id: str | None = None
    product_id: str | None = None
    currency: str | None = None
    price_type: str | None = None
    breaks: list[PriceBreak] = field(default_factory=list)
    effective_date: str | None = None
    expiry_date: str | None = None
    source: Source | None = None


@dataclass
class DecorationLocation(_Base):
    """A place on a product that can be decorated, and how."""

    location_id: str | None = None
    name: str | None = None
    decorations: list[dict] = field(default_factory=list)
    max_colors: int | None = None
    height: float | None = None
    width: float | None = None
    uom: str | None = None
    source: Source | None = None


@dataclass
class Charge(_Base):
    charge_id: str | None = None
    name: str | None = None
    description: str | None = None
    charge_type: str | None = None
    is_required: bool | None = None
    breaks: list[PriceBreak] = field(default_factory=list)


# ---------------------------------------------------------------------------
# order lifecycle
# ---------------------------------------------------------------------------

@dataclass
class ShipmentPackage(_Base):
    tracking_number: str | None = None
    carrier: str | None = None
    ship_method: str | None = None
    ship_date: str | None = None
    weight: float | None = None
    weight_uom: str | None = None
    contents: list[dict] = field(default_factory=list)


@dataclass
class Shipment(_Base):
    po_number: str | None = None
    sales_order_number: str | None = None
    ship_date: str | None = None
    packages: list[ShipmentPackage] = field(default_factory=list)
    source: Source | None = None


@dataclass
class InvoiceLine(_Base):
    line_number: str | None = None
    part_id: str | None = None
    description: str | None = None
    quantity: float | None = None
    unit_price: float | None = None
    amount: float | None = None


@dataclass
class Invoice(_Base):
    invoice_number: str | None = None
    po_number: str | None = None
    sales_order_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    currency: str | None = None
    subtotal: float | None = None
    tax: float | None = None
    freight: float | None = None
    total: float | None = None
    lines: list[InvoiceLine] = field(default_factory=list)
    source: Source | None = None


@dataclass
class PurchaseOrderResult(_Base):
    """Outcome of a `sendPO` call.

    `accepted` is tri-state on purpose: True (supplier acknowledged),
    False (supplier rejected outright), or None (we do not know — the
    transport failed after the request left). None must escalate; it is
    never retried, since a duplicate PO is worse than a late one.
    """

    accepted: bool | None = None
    po_number: str | None = None
    sales_order_number: str | None = None
    messages: list[dict] = field(default_factory=list)
    submitted_to: str | None = None
    is_test: bool | None = None
    source: Source | None = None


# ---------------------------------------------------------------------------
# capability introspection
# ---------------------------------------------------------------------------

@dataclass
class Capability(_Base):
    """One service a supplier actually publishes, and whether we can drive it."""

    service: str | None = None
    service_name: str | None = None
    version: str | None = None
    url: str | None = None
    test_url: str | None = None
    status: str | None = None
    # False when the registry lists it but this package has no adapter.
    supported: bool = False
    operations: list[str] = field(default_factory=list)
