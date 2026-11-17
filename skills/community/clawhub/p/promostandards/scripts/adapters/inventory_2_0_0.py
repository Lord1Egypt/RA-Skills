"""Inventory 2.0.0 — `getInventoryLevels`, `getFilterValues`.

The version 155 of the 201 inventory-publishing suppliers run, and the only
one that reports per-warehouse stock.

Auth and payload elements both live in the SharedObjects namespace; only
the request root sits in the service namespace.
"""

from __future__ import annotations

import soap
from adapters.base import Adapter
from schemas import InventoryLevel, InventoryResult, LocationStock

NS = "http://www.promostandards.org/WSDL/Inventory/2.0.0/"
NS_SHARED = "http://www.promostandards.org/WSDL/Inventory/2.0.0/SharedObjects/"


class Inventory200(Adapter):
    SERVICE = "INV"
    VERSION = "2.0.0"
    NAMESPACES = {"ns": NS, "shar": NS_SHARED}
    AUTH_PREFIX = "shar"
    OPERATIONS = ("getInventoryLevels", "getFilterValues")

    def get_inventory_levels(self, product_id: str, *,
                             part_ids: list[str] | None = None,
                             colors: list[str] | None = None,
                             sizes: list[str] | None = None) -> InventoryResult:
        filters = ""
        if part_ids:
            filters += (
                "<shar:partIdArray>"
                + "".join(soap.element("shar:partId", p) for p in part_ids)
                + "</shar:partIdArray>"
            )
        if colors:
            filters += (
                "<shar:PartColorArray>"
                + "".join(soap.element("shar:partColor", c) for c in colors)
                + "</shar:PartColorArray>"
            )
        if sizes:
            filters += (
                "<shar:LabelSizeArray>"
                + "".join(soap.element("shar:labelSize", s) for s in sizes)
                + "</shar:LabelSizeArray>"
            )

        body = (
            "<ns:GetInventoryLevelsRequest>"
            + self.auth_xml()
            + soap.element("shar:productId", product_id)
            + (f"<shar:Filter>{filters}</shar:Filter>" if filters else "")
            + "</ns:GetInventoryLevelsRequest>"
        )
        root = self.post("getInventoryLevels", body)
        messages = self.raise_on_error(root)

        inventory = soap.find(root, "Inventory")
        levels = []
        for node in soap.find_all(root, "PartInventory"):
            quantity_node = soap.child(node, "quantityAvailable")
            locations = []
            for loc in soap.find_all(node, "InventoryLocation"):
                loc_qty = soap.child(loc, "inventoryLocationQuantity")
                locations.append(LocationStock(
                    location_id=soap.text(loc, "inventoryLocationId"),
                    name=soap.text(loc, "inventoryLocationName"),
                    postal_code=soap.text(loc, "postalCode"),
                    country=soap.text(loc, "country"),
                    quantity=soap.number(loc_qty, "value"),
                    uom=soap.text(loc_qty, "uom"),
                ))
            levels.append(InventoryLevel(
                part_id=soap.text(node, "partId"),
                product_id=soap.text(inventory, "productId"),
                color=soap.text(node, "partColor"),
                size=soap.text(node, "labelSize"),
                description=soap.text(node, "partDescription"),
                quantity=soap.number(quantity_node, "value"),
                uom=soap.text(quantity_node, "uom"),
                locations=locations,
                lead_time_days=soap.integer(node, "replenishmentLeadTime"),
                is_main_part=soap.boolean(node, "mainPart"),
                buy_to_order=soap.boolean(node, "buyToOrder"),
                last_modified=soap.text(node, "lastModified"),
                locations_supported=True,
            ))

        return InventoryResult(
            product_id=soap.text(inventory, "productId") or product_id,
            levels=levels,
            messages=messages,
            source=self.source("getInventoryLevels"),
        )

    def get_filter_values(self, product_id: str) -> dict:
        body = (
            "<ns:GetFilterValuesRequest>"
            + self.auth_xml()
            + soap.element("shar:productId", product_id)
            + "</ns:GetFilterValuesRequest>"
        )
        root = self.post("getFilterValues", body)
        messages = self.raise_on_error(root)
        return {
            "product_id": product_id,
            "part_ids": [e.text for e in soap.find_all(root, "partId")
                         if e.text],
            "colors": [e.text for e in soap.find_all(root, "partColor")
                       if e.text],
            "sizes": [e.text for e in soap.find_all(root, "labelSize")
                      if e.text],
            "messages": messages,
            "source": self.source("getFilterValues").to_dict(),
        }
