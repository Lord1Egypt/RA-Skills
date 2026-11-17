"""Product Pricing and Configuration 1.0.0 — the only PPC version.

513 of 601 endpoint-publishing suppliers offer it, second only to Product
Data, and it is the single version in the registry — so one adapter covers
every PPC supplier that exists today.

`getConfigurationAndPricing` requires `currency`, `fobId`, `priceType`,
`localizationCountry`, `localizationLanguage` and `configurationType` with
no schema defaults. `fobId` is the awkward one: it is supplier-specific and
must come from `getFobPoints` first, so callers that do not supply one get
a clear error rather than a silently wrong price.
"""

from __future__ import annotations

import soap
from adapters.base import Adapter
from errors import ConfigError
from schemas import Charge, DecorationLocation, PriceBreak, PriceGrid

NS = "http://www.promostandards.org/WSDL/PricingAndConfiguration/1.0.0/"
NS_SHARED = (
    "http://www.promostandards.org/WSDL/PricingAndConfiguration/1.0.0"
    "/SharedObjects/"
)

#: priceType values the spec enumerates; passed through verbatim.
PRICE_TYPES = ("Customer", "Distributor", "End Customer", "List", "Net")


class Pricing100(Adapter):
    SERVICE = "PPC"
    VERSION = "1.0.0"
    NAMESPACES = {"ns": NS, "shar": NS_SHARED}
    AUTH_PREFIX = "shar"
    OPERATIONS = ("getConfigurationAndPricing", "getAvailableLocations",
                  "getDecorationsForLocation", "getAvailableCharges",
                  "getFobPoints")

    def get_fob_points(self, product_id: str | None = None, *,
                       country: str = "US", language: str = "EN") -> list[dict]:
        # Element ORDER matters: the request type is an xs:sequence, and the
        # .asmx services most PPC suppliers run deserialize it positionally.
        # Out-of-order elements do not bind, and because every field is
        # minOccurs="0" nothing faults — productId simply arrives null and the
        # service answers with an empty FobPointArray. That reads exactly like
        # "this supplier publishes no FOB points", which is how it survived:
        # pricing is unobtainable without a fobId, so the whole PPC service
        # looks broken supplier-side. Keep productId before the localization
        # pair, per the spec sequence.
        body = (
            "<ns:GetFobPointsRequest>"
            + self.auth_xml()
            + soap.element("shar:productId", product_id)
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + "</ns:GetFobPointsRequest>"
        )
        root = self.post("getFobPoints", body)
        self.raise_on_error(root)
        points = []
        for node in soap.find_all(root, "FobPoint"):
            points.append({
                "fob_id": soap.text(node, "fobId"),
                "city": soap.text(node, "fobCity"),
                "state": soap.text(node, "fobState"),
                "postal_code": soap.text(node, "fobPostalCode"),
                "country": soap.text(node, "fobCountry"),
            })
        return points

    def get_configuration_and_pricing(
        self, product_id: str, *, fob_id: str, currency: str = "USD",
        price_type: str = "Net", part_id: str | None = None,
        configuration_type: str = "Blank", country: str = "US",
        language: str = "EN",
    ) -> list[PriceGrid]:
        if not fob_id:
            raise ConfigError(
                "getConfigurationAndPricing requires a fobId; call "
                "get_fob_points() first — it is supplier-specific and the "
                "price depends on it"
            )
        body = (
            "<ns:GetConfigurationAndPricingRequest>"
            + self.auth_xml()
            + soap.element("shar:productId", product_id)
            + soap.element("shar:partId", part_id)
            + soap.element("shar:currency", currency)
            + soap.element("shar:fobId", fob_id)
            + soap.element("shar:priceType", price_type)
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + soap.element("shar:configurationType", configuration_type)
            + "</ns:GetConfigurationAndPricingRequest>"
        )
        root = self.post("getConfigurationAndPricing", body)
        self.raise_on_error(root)

        grids = []
        for part in soap.find_all(root, "PartPrice", "PartArray", "Part"):
            part_id_value = soap.text(part, "partId")
            if part_id_value is None:
                continue
            breaks = []
            for price in soap.find_all(part, "PartPrice", "Price"):
                quantity = soap.number(price, "minQuantity")
                amount = soap.number(price, "price", "salePrice")
                if quantity is None and amount is None:
                    continue
                breaks.append(PriceBreak(
                    min_quantity=quantity,
                    price=amount,
                    discount_code=soap.text(price, "discountCode"),
                    uom=soap.text(price, "priceUom", "uom"),
                ))
            if not breaks:
                continue
            grids.append(PriceGrid(
                part_id=part_id_value,
                product_id=product_id,
                currency=currency,
                price_type=price_type,
                breaks=breaks,
                source=self.source("getConfigurationAndPricing"),
            ))
        return grids

    def get_available_locations(self, product_id: str, *, country: str = "US",
                                language: str = "EN") -> list[DecorationLocation]:
        body = (
            "<ns:GetAvailableLocationsRequest>"
            + self.auth_xml()
            + soap.element("shar:productId", product_id)
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + "</ns:GetAvailableLocationsRequest>"
        )
        root = self.post("getAvailableLocations", body)
        self.raise_on_error(root)
        locations = []
        for node in soap.find_all(root, "Location"):
            locations.append(DecorationLocation(
                location_id=soap.text(node, "locationId"),
                name=soap.text(node, "locationName"),
                source=self.source("getAvailableLocations"),
            ))
        return locations

    def get_decorations_for_location(
        self, product_id: str, location_id: str, *, country: str = "US",
        language: str = "EN",
    ) -> DecorationLocation:
        body = (
            "<ns:GetDecorationsForLocationRequest>"
            + self.auth_xml()
            + soap.element("shar:productId", product_id)
            + soap.element("shar:locationId", location_id)
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + "</ns:GetDecorationsForLocationRequest>"
        )
        root = self.post("getDecorationsForLocation", body)
        self.raise_on_error(root)
        decorations = []
        for node in soap.find_all(root, "Decoration"):
            decorations.append({
                "decoration_id": soap.text(node, "decorationId"),
                "name": soap.text(node, "decorationName"),
                "max_colors": soap.integer(node, "maxColors"),
                "height": soap.number(node, "decorationHeight", "height"),
                "width": soap.number(node, "decorationWidth", "width"),
                "uom": soap.text(node, "decorationUom", "uom"),
            })
        return DecorationLocation(
            location_id=location_id,
            name=soap.text(root, "locationName"),
            decorations=decorations,
            source=self.source("getDecorationsForLocation"),
        )

    def get_available_charges(self, product_id: str, *, country: str = "US",
                              language: str = "EN") -> list[Charge]:
        body = (
            "<ns:GetAvailableChargesRequest>"
            + self.auth_xml()
            + soap.element("shar:productId", product_id)
            + soap.element("shar:localizationCountry", country)
            + soap.element("shar:localizationLanguage", language)
            + "</ns:GetAvailableChargesRequest>"
        )
        root = self.post("getAvailableCharges", body)
        self.raise_on_error(root)
        charges = []
        for node in soap.find_all(root, "Charge"):
            breaks = []
            for price in soap.find_all(node, "ChargePrice"):
                breaks.append(PriceBreak(
                    min_quantity=soap.number(price, "minQuantity"),
                    price=soap.number(price, "price", "salePrice"),
                    discount_code=soap.text(price, "discountCode"),
                ))
            charges.append(Charge(
                charge_id=soap.text(node, "chargeId"),
                name=soap.text(node, "chargeName"),
                description=soap.text(node, "chargeDescription"),
                charge_type=soap.text(node, "chargeType"),
                is_required=soap.boolean(node, "isRequired"),
                breaks=breaks,
            ))
        return charges
