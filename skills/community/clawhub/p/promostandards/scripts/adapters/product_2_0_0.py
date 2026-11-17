"""Product Data 2.0.0 — `getProduct`, `getProductSellable`,
`getProductCloseOut`, `getProductDateModified`.

502 of the 540 Product Data suppliers publish this version, but 494 also
publish 1.0.0 and some publish only 1.0.0 — hence both adapters.

`localizationCountry` and `localizationLanguage` are required by the
schema with no default, so they are explicit parameters defaulting to
US/EN rather than being quietly omitted.
"""

from __future__ import annotations

import soap
from adapters._product_common import parse_product
from adapters.base import Adapter
from schemas import PriceBreak, PriceGrid

NS = "http://www.promostandards.org/WSDL/ProductDataService/2.0.0/"
NS_SHARED = (
    "http://www.promostandards.org/WSDL/ProductDataService/2.0.0/SharedObjects/"
)


class Product200(Adapter):
    SERVICE = "PRODUCT"
    VERSION = "2.0.0"
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
            + soap.element("shar:colorName", color)
            + "</ns:GetProductRequest>"
        )
        root = self.post("getProduct", body)
        messages = self.raise_on_error(root)
        product = parse_product(root, self.source("getProduct"), messages)

        # 2.0.0-only enrichment.
        node = soap.find(root, "Product") or root
        product.primary_image_url = soap.text(node, "primaryImageUrl")
        return product

    def get_price_grids(self, product_id: str, *, country: str = "US",
                        language: str = "EN") -> list[PriceGrid]:
        """Price groups carried on the product record (2.0.0 only).

        Product Data 2.0.0 embeds list pricing; net and configured pricing
        still comes from PPC. Returns an empty list when the supplier omits
        the price group array, which many do.
        """
        body = (
            "<ns:GetProductRequest>"
            + self.auth_xml()
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + soap.element("shar:productId", product_id)
            + "</ns:GetProductRequest>"
        )
        root = self.post("getProduct", body)
        self.raise_on_error(root)

        grids = []
        for group in soap.find_all(root, "ProductPriceGroup"):
            breaks = []
            for price in soap.find_all(group, "ProductPrice"):
                breaks.append(PriceBreak(
                    min_quantity=soap.number(price, "minQuantity"),
                    price=soap.number(price, "price", "salePrice"),
                    discount_code=soap.text(price, "discountCode"),
                    uom=soap.text(price, "priceUom", "uom"),
                ))
            grids.append(PriceGrid(
                product_id=product_id,
                currency=soap.text(group, "currency"),
                price_type=soap.text(group, "groupName"),
                breaks=breaks,
                source=self.source("getProduct"),
            ))
        return grids

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
