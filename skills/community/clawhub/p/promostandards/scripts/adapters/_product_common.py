"""Parsing shared between Product Data 1.0.0 and 2.0.0.

The two versions diverge in what they *carry* — 2.0.0 adds price groups,
FOB points, a primary image, decoration locations and compliance flags —
but the elements they have in common are spelled identically. That common
core is parsed once here; each adapter still owns its own namespaces,
request construction and version-specific extras, so adding a version
remains a new module rather than a branch.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

import soap
from schemas import Part, Product


def parse_part(node: ET.Element) -> Part:
    dimension = soap.child(node, "Dimension") or soap.find(node, "Dimension")
    dims = None
    if dimension is not None:
        dims = {
            "depth": soap.number(dimension, "depth"),
            "height": soap.number(dimension, "height"),
            "width": soap.number(dimension, "width"),
            "uom": soap.text(dimension, "dimensionUom"),
        }

    # Colour lives in a nested <Color><colorName>; size in <ApparelSize>.
    color_node = soap.child(node, "primaryColor") or soap.child(node, "ColorArray")
    size_node = soap.child(node, "ApparelSize")

    return Part(
        part_id=soap.text(node, "partId"),
        description=soap.text(node, "description"),
        color=soap.text(color_node, "colorName") if color_node is not None else None,
        size=(soap.text(size_node, "labelSize", "apparelStyle")
              if size_node is not None else None),
        country_of_origin=soap.text(node, "countryOfOrigin"),
        primary_material=soap.text(node, "primaryMaterial"),
        gtin=soap.text(node, "gtin"),
        unspsc=soap.text(node, "unspsc"),
        lead_time_days=soap.integer(node, "leadTime"),
        is_closeout=soap.boolean(node, "isCloseout"),
        is_caution=soap.boolean(node, "isCaution"),
        caution_comment=soap.text(node, "cautionComment"),
        is_hazmat=soap.boolean(node, "isHazmat"),
        is_rush_service=soap.boolean(node, "isRushService"),
        effective_date=soap.text(node, "effectiveDate"),
        end_date=soap.text(node, "endDate"),
        weight=soap.number(dimension, "weight") if dimension is not None else None,
        weight_uom=(soap.text(dimension, "weightUom")
                    if dimension is not None else None),
        dimensions=dims,
    )


def parse_product(root: ET.Element, source, messages: list[dict]) -> Product:
    """Parse the elements common to both Product Data versions."""
    node = soap.find(root, "Product") or root

    categories = []
    for cat in soap.find_all(node, "ProductCategory"):
        categories.append({
            "category": soap.text(cat, "category"),
            "sub_category": soap.text(cat, "subCategory"),
        })

    return Product(
        product_id=soap.text(node, "productId"),
        name=soap.text(node, "productName"),
        brand=soap.text(node, "productBrand"),
        # Direct children only: parts carry their own <description>, and a
        # descendant search would fold those into the product's.
        description=[e.text.strip() for e in soap.children(node, "description")
                     if e.text and e.text.strip()],
        keywords=[e.text.strip() for e in soap.find_all(node, "keyword")
                  if e.text and e.text.strip()],
        categories=categories,
        marketing_points=[e.text.strip()
                          for e in soap.find_all(node, "pointCopy")
                          if e.text and e.text.strip()],
        line_name=soap.text(node, "lineName"),
        is_closeout=soap.boolean(node, "isCloseout"),
        is_caution=soap.boolean(node, "isCaution"),
        caution_comment=soap.text(node, "cautionComment"),
        effective_date=soap.text(node, "effectiveDate"),
        end_date=soap.text(node, "endDate"),
        last_change_date=soap.text(node, "lastChangeDate"),
        parts=[parse_part(p) for p in soap.find_all(node, "ProductPart")],
        messages=messages,
        source=source,
    )
