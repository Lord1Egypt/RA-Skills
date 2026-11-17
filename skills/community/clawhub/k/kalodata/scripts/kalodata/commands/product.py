"""`kalo product` — product rank / detail."""

from __future__ import annotations

from .. import api
from ..core import Command, Flag
from . import common

SORT_FIELDS = (
    "revenue",
    "video_revenue",
    "showcase_revenue",
    "commission_rate",
    "revenue_growth_rate",
    "sales_volumn",
    "unit_price",
    "launch_date",
)
ALL_FIELDS = (
    "product_id",
    "product_name",
    "launch_date",
    "revenue",
    "commission_rate",
    "revenue_growth_rate",
    "sales_volumn",
    "unit_price",
    "live_revenue",
    "video_revenue",
    "showcase_revenue",
    "master_image_url",
)
DEFAULT_FIELDS = ("product_id", "product_name", "revenue", "sales_volumn")


def rank(cfg, opts, args):
    body = {}
    common.put_optional(
        body,
        opts,
        {
            "shop": "shop_id",
            "creator": "creator_id",
            "video": "video_id",
            "live": "livestream_id",
            "commission": "commission_rate",
            "delivery": "delivery_type",
            "launch": "launch_date",
            "keyword": "keyword",
        },
    )
    common.put_range(body, opts, "price", "unit_price_range", "--price")
    common.put_range(body, opts, "revenue", "revenue_range", "--revenue")
    if opts.get("category"):
        body["category_ids"] = opts["category"]
    aff = common.tri_state(opts, "affiliate", "no_affiliate", "--affiliate", "--no-affiliate")
    if aff is not None:
        body["is_affiliate"] = aff
    tts = common.tri_state(opts, "tts", "no_tts", "--tts", "--no-tts")
    if tts is not None:
        body["is_tts_product"] = tts
    if opts.get("all"):
        body["need_all"] = True
    common.apply_images(opts, body, "master_image_url")
    return common.run_rank(
        cfg,
        opts,
        endpoint="/tiktok/product/rank",
        noun="products",
        tier="rank",
        default_fields=DEFAULT_FIELDS,
        all_fields=ALL_FIELDS,
        sort_fields=SORT_FIELDS,
        body_extra=body,
        title_fields=("product_name",),
        suggestions=(
            "Run `kalo product detail <product_id>` for price range, shop id, revenue trend",
            "Run `kalo creator rank --product <product_id>` for creators selling a product",
        ),
    )


def detail(cfg, opts, ids):
    def fetch(product_id):
        body = common.base_body(cfg, opts, "detail")
        body.update(product_id=product_id, need_extra=True)
        if opts.get("images"):
            body["need_image"] = 1
        return api.request(cfg, "/tiktok/product/detail", body, timeout=10)

    def post(d, o, notes):
        common.summarize_trend(d, o.get("full"))
        if not o.get("full"):
            notes.append("Add `--full` for the day-by-day revenue_trend series")
        return d

    return common.run_detail_batch(
        cfg,
        opts,
        ids,
        noun="product",
        fetch=fetch,
        postprocess=post,
        suggestions=(
            "Run `kalo shop detail <product_shop_id>` to resolve the shop name",
            "Run `kalo video rank --product <product_id>` for its top videos",
        ),
    )


COMMANDS = [
    Command(
        path="product rank",
        summary="Top TikTok Shop products by revenue/sales",
        handler=rank,
        flags=common.common_flags("rank")
        + common.list_flags(SORT_FIELDS)
        + [
            common.category_flag(),
            Flag("--shop", "filter by shop id", metavar="ID"),
            Flag("--creator", "filter by creator id", metavar="ID"),
            Flag("--video", "filter by video id", metavar="ID"),
            Flag("--live", "filter by livestream id", metavar="ID"),
            Flag("--price", 'unit price range "min-max"', metavar="MIN-MAX"),
            Flag("--revenue", 'revenue range "min-max"', metavar="MIN-MAX"),
            Flag("--commission", "commission rate filter", metavar="RATE"),
            Flag("--launch", "launch window: <3 | <7 | >30 days", choices=("<3", "<7", ">30")),
            Flag("--delivery", "delivery type", choices=("local", "global")),
            Flag("--keyword", "product name keyword", metavar="TEXT"),
            Flag("--affiliate", "only affiliate (commissioned) products", kind="flag", default=False),
            Flag("--no-affiliate", "only non-affiliate products", kind="flag", default=False),
            Flag("--tts", "only fully-managed (TTS) products", kind="flag", default=False),
            Flag("--no-tts", "exclude fully-managed products", kind="flag", default=False),
            Flag("--all", "include zero-sales products", kind="flag", default=False),
            common.images_flag(),
        ],
        examples=[
            "kalo product rank --region US --category 601739 --sort revenue",
            "kalo product rank --keyword 'hair dryer' --price 20-100 --launch '<7'",
        ],
    ),
    Command(
        path="product detail",
        summary="Full metrics for one or more products (batched client-side)",
        handler=lambda cfg, opts, args: detail(cfg, opts, args),
        flags=common.common_flags("detail")
        + [
            Flag("--full", "include the full revenue_trend series", kind="flag", default=False),
            common.images_flag(),
        ],
        positional="product_id",
        pos_min=1,
        pos_max=None,
        examples=["kalo product detail 1729386274 1729399999"],
    ),
]
