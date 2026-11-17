"""Inventory 1.2.1 — `getInventoryLevels`, `getFilterValues`.

139 of the 201 inventory-publishing suppliers run this version, so it is
not a legacy tail that can be skipped in favour of 2.0.0.

Three traps, all of which would be invisible in a shared request builder:

1. **The namespace is `.../WSDL/InventoryService/1.0.0/`** — it says 1.0.0
   even though the service version is 1.2.1, and the path segment is
   `InventoryService`, not 2.0.0's `Inventory`. Hardcoded on purpose.
2. **Everything is in one namespace.** There is no SharedObjects split, so
   auth elements take the same prefix as the payload.
3. **There is no warehouse breakdown.** The schema has no location array
   at any depth, so `locations` is always empty and `locations_supported`
   is False — the caller must be able to tell "this version cannot say"
   from "this product is in no warehouse".

Element spellings also differ from 2.0.0: `productID`/`partID` with a
capital D, a required `productIDtype`, `attributeColor`/`attributeSize`
instead of `partColor`/`labelSize`, and `quantityAvailable` as a bare
scalar with no unit of measure.
"""

from __future__ import annotations

import soap
from adapters.base import Adapter
from schemas import InventoryLevel, InventoryResult

NS = "http://www.promostandards.org/WSDL/InventoryService/1.0.0/"


class Inventory121(Adapter):
    SERVICE = "INV"
    VERSION = "1.2.1"
    NAMESPACES = {"ns": NS}
    AUTH_PREFIX = "ns"
    OPERATIONS = ("getInventoryLevels", "getFilterValues")

    #: `productIDtype` is required by the schema. "Supplier" means the id is
    #: the supplier's own style number, which is what a caller always has.
    DEFAULT_ID_TYPE = "Supplier"

    def get_inventory_levels(self, product_id: str, *,
                             part_ids: list[str] | None = None,
                             colors: list[str] | None = None,
                             sizes: list[str] | None = None,
                             id_type: str | None = None) -> InventoryResult:
        # part_ids/colors/sizes have no filter equivalent in this version's
        # schema, so they are applied client-side after the fetch rather
        # than silently ignored.
        body = (
            "<ns:Request>"
            + self.auth_xml()
            + soap.element("ns:productID", product_id)
            + soap.element("ns:productIDtype", id_type or self.DEFAULT_ID_TYPE)
            + "</ns:Request>"
        )
        root = self.post("getInventoryLevels", body)
        messages = self.raise_on_error(root)

        levels = []
        for node in soap.find_all(root, "ProductVariationInventory"):
            levels.append(InventoryLevel(
                part_id=soap.text(node, "partID"),
                product_id=soap.text(root, "productID") or product_id,
                color=soap.text(node, "attributeColor"),
                size=soap.text(node, "attributeSize"),
                description=soap.text(node, "partDescription"),
                quantity=soap.number(node, "quantityAvailable"),
                # 1.2.1 has no uom element; absent, not assumed to be EA.
                uom=None,
                locations=[],
                is_main_part=None,
                last_modified=soap.text(node, "validTimestamp"),
                locations_supported=False,
            ))

        levels = _apply_client_filters(levels, part_ids, colors, sizes)
        return InventoryResult(
            product_id=soap.text(root, "productID") or product_id,
            levels=levels,
            messages=messages,
            source=self.source("getInventoryLevels"),
        )

    def get_filter_values(self, product_id: str,
                          id_type: str | None = None) -> dict:
        body = (
            "<ns:GetFilterValuesRequest>"
            + self.auth_xml()
            + soap.element("ns:productID", product_id)
            + soap.element("ns:productIDtype", id_type or self.DEFAULT_ID_TYPE)
            + "</ns:GetFilterValuesRequest>"
        )
        root = self.post("getFilterValues", body)
        messages = self.raise_on_error(root)
        return {
            "product_id": product_id,
            "part_ids": [e.text for e in soap.find_all(root, "partID")
                         if e.text],
            "colors": [e.text for e in soap.find_all(root, "attributeColor")
                       if e.text],
            "sizes": [e.text for e in soap.find_all(root, "attributeSize")
                      if e.text],
            "messages": messages,
            "source": self.source("getFilterValues").to_dict(),
        }


def _apply_client_filters(levels: list[InventoryLevel],
                          part_ids: list[str] | None,
                          colors: list[str] | None,
                          sizes: list[str] | None) -> list[InventoryLevel]:
    """Filter locally, since 1.2.1's request has no Filter element.

    Comparison is case-insensitive: suppliers are inconsistent about the
    casing of colour and size labels between services.
    """
    def matches(value: str | None, wanted: list[str] | None) -> bool:
        if not wanted:
            return True
        if value is None:
            return False
        return value.strip().lower() in {w.strip().lower() for w in wanted}

    return [
        level for level in levels
        if matches(level.part_id, part_ids)
        and matches(level.color, colors)
        and matches(level.size, sizes)
    ]
