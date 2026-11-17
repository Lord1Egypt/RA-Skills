"""Product Data 1.0.0 — `getProduct`, `getProductSellable`,
`getProductCloseOut`, `getProductDateModified`.

494 suppliers publish this version, near-parity with 2.0.0's 502, so it
cannot be treated as a deprecated tail.

Relative to 2.0.0 the wire format is close enough that the response parser
is shared, but this version carries **no** `primaryImageUrl`, no
`ProductPriceGroupArray`, no FOB points and no decoration locations. Those
fields stay None here rather than being synthesised — a caller checking
`primary_image_url` needs to see "this supplier's version cannot provide
it", not an empty string that looks like a supplier omission.
"""

from __future__ import annotations

import soap
from adapters._product_common import parse_product
from adapters.base import Adapter

NS = "http://www.promostandards.org/WSDL/ProductDataService/1.0.0/"
NS_SHARED = (
    "http://www.promostandards.org/WSDL/ProductDataService/1.0.0/SharedObjects/"
)


class Product100(Adapter):
    SERVICE = "PRODUCT"
    VERSION = "1.0.0"
    NAMESPACES = {"ns": NS, "shar": NS_SHARED}
    AUTH_PREFIX = "shar"
    OPERATIONS = ("getProduct", "getProductSellable", "getProductCloseOut",
                  "getProductDateModified")

    def get_product(self, product_id: str, *, part_id: str | None = None,
                    color: str | None = None, country: str = "US",
                    language: str = "EN"):
        body = (
            "<ns:GetProductRequest>"
            + self.auth_xml()
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + soap.element("shar:productId", product_id)
            + soap.element("shar:partId", part_id)
            + soap.element("ns:colorName", color)
            + "</ns:GetProductRequest>"
        )
        root = self.post("getProduct", body)
        messages = self.raise_on_error(root)
        return parse_product(root, self.source("getProduct"), messages)

    def get_product_sellable(self, product_id: str | None = None, *,
                             country: str = "US", language: str = "EN") -> dict:
        body = (
            "<ns:GetProductSellableRequest>"
            + self.auth_xml()
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + soap.element("shar:productId", product_id)
            + "</ns:GetProductSellableRequest>"
        )
        root = self.post("getProductSellable", body)
        messages = self.raise_on_error(root)
        return {
            "products": [
                {"product_id": soap.text(p, "productId"),
                 "part_id": soap.text(p, "partId")}
                for p in soap.find_all(root, "ProductSellable")
            ],
            "messages": messages,
            "source": self.source("getProductSellable").to_dict(),
        }

    def get_product_date_modified(self, changed_since: str) -> dict:
        body = (
            "<ns:GetProductDateModifiedRequest>"
            + self.auth_xml()
            + soap.element("shar:changeTimeStamp", changed_since)
            + "</ns:GetProductDateModifiedRequest>"
        )
        root = self.post("getProductDateModified", body)
        messages = self.raise_on_error(root)
        return {
            "product_ids": [e.text for e in soap.find_all(root, "productId")
                            if e.text],
            "messages": messages,
            "source": self.source("getProductDateModified").to_dict(),
        }

    def get_product_close_out(self, *, country: str = "US",
                              language: str = "EN") -> dict:
        body = (
            "<ns:GetProductCloseOutRequest>"
            + self.auth_xml()
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + "</ns:GetProductCloseOutRequest>"
        )
        root = self.post("getProductCloseOut", body)
        messages = self.raise_on_error(root)
        return {
            "product_ids": [e.text for e in soap.find_all(root, "productId")
                            if e.text],
            "messages": messages,
            "source": self.source("getProductCloseOut").to_dict(),
        }
