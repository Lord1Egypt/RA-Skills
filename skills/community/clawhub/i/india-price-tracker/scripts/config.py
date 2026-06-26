from dataclasses import dataclass
from typing import Dict, List
import random


STORES: Dict[str, str] = {
    "amazon_in": "Amazon India",
    "flipkart": "Flipkart",
    "reliance_digital": "Reliance Digital",
    "croma": "Croma",
    "vijay_sales": "Vijay Sales",
    "tata_cliq": "Tata CLiQ",
    "jiomart": "JioMart",
    "myntra": "Myntra",
    "ajio": "AJIO",
    "nykaa": "Nykaa",
    "snapdeal": "Snapdeal",
}


@dataclass
class Offer:
    instant_discount: float = 0.0
    coupon_discount: float = 0.0
    card_cashback: float = 0.0
    shipping: float = 0.0


@dataclass
class Listing:
    store: str
    title: str
    sku_hint: str
    list_price: float
    offer: Offer
    in_stock: bool
    seller_rating: float

    @property
    def effective_price(self) -> float:
        value = (
            self.list_price
            - self.offer.instant_discount
            - self.offer.coupon_discount
            - self.offer.card_cashback
            + self.offer.shipping
        )
        return round(max(0.0, value), 2)


def mock_search(keyword: str, stores: List[str]) -> List[Listing]:
    random.seed(hash(keyword) % 100000)
    results: List[Listing] = []
    for s in stores:
        base = random.randint(8000, 90000)
        instant = random.choice([0, 500, 1000, 1500, 2000])
        coupon = random.choice([0, 250, 500, 1000])
        cashback = random.choice([0, 500, 1000, 1500])
        shipping = random.choice([0, 49, 99, 149])
        in_stock = random.choice([True, True, True, False])
        rating = round(random.uniform(3.7, 4.9), 1)
        results.append(
            Listing(
                store=s,
                title=f"{keyword} - {STORES.get(s, s)}",
                sku_hint=f"{keyword[:12].upper()}-{s[:4].upper()}",
                list_price=float(base),
                offer=Offer(
                    instant_discount=float(instant),
                    coupon_discount=float(coupon),
                    card_cashback=float(cashback),
                    shipping=float(shipping),
                ),
                in_stock=in_stock,
                seller_rating=rating,
            )
        )
    return results

