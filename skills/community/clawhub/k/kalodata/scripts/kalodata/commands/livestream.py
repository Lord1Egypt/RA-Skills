"""`kalo live` — livestream rank / detail."""

from __future__ import annotations

import datetime

from .. import api
from ..core import Command, Flag
from . import common

SORT_FIELDS = (
    "livestream_start_time",
    "livestream_end_time",
    "livestream_duration",
    "revenue",
    "unit_price",
    "views",
)
ALL_FIELDS = (
    "livestream_id",
    "livestream_title",
    "creator_handle",
    "creator_id",
    "livestream_start_time",
    "livestream_end_time",
    "livestream_duration",
    "revenue",
    "unit_price",
    "views",
    "record_type",
)
DEFAULT_FIELDS = ("livestream_id", "livestream_title", "revenue", "views")


def _fmt_times(d: dict) -> dict:
    # *_time fields are epoch milliseconds — render as UTC for the agent
    for key in ("livestream_start_time", "livestream_end_time"):
        v = d.get(key)
        if isinstance(v, (int, float)) and v > 1e11:
            dt = datetime.datetime.fromtimestamp(v / 1000, tz=datetime.timezone.utc)
            d[key] = dt.strftime("%Y-%m-%d %H:%M UTC")
    return d


def rank(cfg, opts, args):
    body = {}
    common.put_optional(body, opts, {"shop": "shop_id", "creator": "creator_id", "keyword": "keyword"})
    common.put_numeric_id(body, opts, "product", "product_id", "--product")
    common.put_range(body, opts, "followers", "followers_range", "--followers")
    if opts.get("category"):
        body["category_ids"] = opts["category"]
    return common.run_rank(
        cfg,
        opts,
        endpoint="/tiktok/livestream/rank",
        noun="livestreams",
        tier="rank",
        default_fields=DEFAULT_FIELDS,
        all_fields=ALL_FIELDS,
        sort_fields=SORT_FIELDS,
        body_extra=body,
        title_fields=("livestream_title",),
        suggestions=(
            "Run `kalo live detail <livestream_id>` for viewers, GPM, top products",
            "Run `kalo product rank --live <livestream_id>` for products sold in a stream",
        ),
    )


def detail(cfg, opts, ids):
    def fetch(livestream_id):
        body = common.base_body(cfg, opts, "detail")
        body.update(livestream_id=livestream_id, need_extra=True)
        return api.request(cfg, "/tiktok/livestream/detail", body)

    def post(d, o, notes):
        return _fmt_times(d)

    return common.run_detail_batch(
        cfg,
        opts,
        ids,
        noun="livestream",
        fetch=fetch,
        postprocess=post,
        suggestions=("Run `kalo product detail <top3_product_ids[i]>` for its top products",),
    )


COMMANDS = [
    Command(
        path="live rank",
        summary="Top TikTok Shop livestreams by revenue/views",
        handler=rank,
        flags=common.common_flags("rank")
        + common.list_flags(SORT_FIELDS)
        + [
            common.category_flag(),
            Flag("--shop", "filter by shop id", metavar="ID"),
            Flag("--creator", "filter by creator id", metavar="ID"),
            Flag("--product", "filter by product id (numeric)", metavar="ID"),
            Flag("--followers", 'creator followers range "min-max"', metavar="MIN-MAX"),
            Flag("--keyword", "livestream title keyword", metavar="TEXT"),
        ],
        examples=["kalo live rank --region TH --sort views"],
    ),
    Command(
        path="live detail",
        summary="Full metrics for one or more livestreams (batched client-side)",
        handler=lambda cfg, opts, args: detail(cfg, opts, args),
        flags=common.common_flags("detail"),
        positional="livestream_id",
        pos_min=1,
        pos_max=None,
        examples=["kalo live detail 7301112223334"],
    ),
]
