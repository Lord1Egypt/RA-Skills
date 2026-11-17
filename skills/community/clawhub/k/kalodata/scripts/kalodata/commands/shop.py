"""`kalo shop` — shop rank / detail."""

from __future__ import annotations

from .. import api
from ..core import Command, Flag
from . import common

SORT_FIELDS = (
    "revenue",
    "sales_volumn",
    "revenue_growth_rate",
    "unit_price",
    "on_sell_product_count",
    "affiliate_revenue",
    "self_promotion_revenue",
    "shopping_mall_revenue",
)
ALL_FIELDS = (
    "shop_id",
    "shop_name",
    "rank",
    "shop_type",
    "revenue",
    "sales_volumn",
    "revenue_growth_rate",
    "unit_price",
    "affiliate_revenue",
    "self_promotion_revenue",
    "shopping_mall_revenue",
    "on_sell_product_count",
    "image_url",
)
DEFAULT_FIELDS = ("shop_id", "shop_name", "revenue", "sales_volumn")


def rank(cfg, opts, args):
    body = {}
    common.put_optional(body, opts, {"type": "shop_type", "keyword": "keyword"})
    common.put_range(body, opts, "revenue", "revenue_range", "--revenue")
    common.put_range(body, opts, "price", "unit_price_range", "--price")
    if opts.get("category"):
        body["category_ids"] = opts["category"]
    common.apply_images(opts, body, "image_url")
    return common.run_rank(
        cfg,
        opts,
        endpoint="/tiktok/shop/rank",
        noun="shops",
        tier="rank",
        default_fields=DEFAULT_FIELDS,
        all_fields=ALL_FIELDS,
        sort_fields=SORT_FIELDS,
        body_extra=body,
        title_fields=("shop_name",),
        # keyword search and sorting are mutually exclusive upstream
        omit_sort=bool(opts.get("keyword")),
        suggestions=(
            "Run `kalo shop detail <shop_id>` for revenue split + top products",
            "Run `kalo product rank --shop <shop_id>` for a shop's products",
        ),
    )


def detail(cfg, opts, ids):
    def fetch(shop_id):
        body = common.base_body(cfg, opts, "detail")
        body.update(shop_id=shop_id, need_extra=True)
        if opts.get("category"):
            body["category_ids"] = opts["category"]
        return api.request(cfg, "/tiktok/shop/detail", body)

    def post(d, o, notes):
        common.summarize_trend(d, o.get("full"))
        if not o.get("full"):
            notes.append("Add `--full` for the day-by-day revenue_trend series")
        return d

    return common.run_detail_batch(
        cfg,
        opts,
        ids,
        noun="shop",
        fetch=fetch,
        postprocess=post,
        suggestions=("Run `kalo product detail <top3_product_ids[i]>` for its best sellers",),
    )


COMMANDS = [
    Command(
        path="shop rank",
        summary="Top TikTok shops by revenue",
        handler=rank,
        flags=common.common_flags("rank")
        + common.list_flags(SORT_FIELDS)
        + [
            common.category_flag(),
            Flag("--revenue", 'revenue range "min-max"', metavar="MIN-MAX"),
            Flag("--price", 'unit price range "min-max"', metavar="MIN-MAX"),
            Flag("--type", "shop type", choices=("BRAND", "RETAILER")),
            Flag("--keyword", "shop name keyword (disables --sort upstream)", metavar="TEXT"),
            common.images_flag(),
        ],
        examples=[
            "kalo shop rank --region GB --type BRAND",
            "kalo shop rank --keyword anker",
        ],
    ),
    Command(
        path="shop detail",
        summary="Full metrics for one or more shops (batched client-side)",
        handler=lambda cfg, opts, args: detail(cfg, opts, args),
        flags=common.common_flags("detail")
        + [
            common.category_flag(),
            Flag("--full", "include the full revenue_trend series", kind="flag", default=False),
        ],
        positional="shop_id",
        pos_min=1,
        pos_max=None,
        examples=["kalo shop detail 7495012345"],
    ),
]
