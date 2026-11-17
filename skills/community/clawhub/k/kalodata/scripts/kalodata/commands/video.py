"""`kalo video` — video rank / detail."""

from __future__ import annotations

from .. import api
from ..core import Command, Flag
from . import common

SORT_FIELDS = ("revenue", "views", "revenue_growth_rate", "ads_roas")
ALL_FIELDS = (
    "video_id",
    "video_title",
    "belonged_creator_id",
    "belonged_creator_handle",
    "revenue",
    "views",
    "revenue_growth_rate",
    "ads_roas",
    "digg_count",
    "share_count",
    "comment_count",
    "ad_revenue_ratio",
    "ad_view_ratio",
    "creator_debut",
    "ad",
    "ai_video",
)
DEFAULT_FIELDS = ("video_id", "video_title", "revenue", "views")


def rank(cfg, opts, args):
    body = {"need_extra": True}
    common.put_optional(
        body, opts, {"shop": "shop_id", "creator": "creator_id", "roas": "ads_roas", "keyword": "keyword"}
    )
    common.put_numeric_id(body, opts, "product", "product_id", "--product")
    common.put_range(body, opts, "revenue", "revenue_range", "--revenue")
    common.put_range(body, opts, "followers", "followers_range", "--followers")
    if opts.get("category"):
        body["category_ids"] = opts["category"]
    ai = common.tri_state(opts, "ai", "no_ai", "--ai", "--no-ai")
    if ai is not None:
        body["is_ai_video"] = ai
    return common.run_rank(
        cfg,
        opts,
        endpoint="/tiktok/video/rank",
        noun="videos",
        tier="rank",
        default_fields=DEFAULT_FIELDS,
        all_fields=ALL_FIELDS,
        sort_fields=SORT_FIELDS,
        body_extra=body,
        title_fields=("video_title",),
        suggestions=(
            "Run `kalo video detail <video_id>` for full metrics + revenue trend",
            "Run `kalo product rank --video <video_id>` for products sold via a video",
        ),
    )


def detail(cfg, opts, ids):
    def fetch(video_id):
        body = common.base_body(cfg, opts, "detail")
        body.update(video_id=video_id, need_extra=True)
        return api.request(cfg, "/tiktok/video/detail", body)

    def post(d, o, notes):
        common.summarize_trend(d, o.get("full"))
        if not o.get("full"):
            notes.append("Add `--full` for the day-by-day revenue_trend series")
        return d

    return common.run_detail_batch(
        cfg,
        opts,
        ids,
        noun="video",
        fetch=fetch,
        postprocess=post,
        suggestions=("Run `kalo creator detail <belonged_creator_id>` for the creator behind it",),
    )


COMMANDS = [
    Command(
        path="video rank",
        summary="Top TikTok shoppable videos by revenue/views",
        handler=rank,
        flags=common.common_flags("rank")
        + common.list_flags(SORT_FIELDS)
        + [
            common.category_flag(),
            Flag("--shop", "filter by shop id", metavar="ID"),
            Flag("--creator", "filter by creator id", metavar="ID"),
            Flag("--product", "filter by product id (numeric)", metavar="ID"),
            Flag("--revenue", 'revenue range "min-max"', metavar="MIN-MAX"),
            Flag("--followers", 'creator followers range "min-max"', metavar="MIN-MAX"),
            Flag("--roas", "ads ROAS filter", metavar="ROAS"),
            Flag("--keyword", "video title keyword", metavar="TEXT"),
            Flag("--ai", "only AI-generated videos", kind="flag", default=False),
            Flag("--no-ai", "only non-AI videos", kind="flag", default=False),
        ],
        examples=[
            "kalo video rank --region US --range last7Day",
            "kalo video rank --product 1729386274 --sort views",
        ],
    ),
    Command(
        path="video detail",
        summary="Full metrics for one or more videos (batched client-side)",
        handler=lambda cfg, opts, args: detail(cfg, opts, args),
        flags=common.common_flags("detail")
        + [Flag("--full", "include the full revenue_trend series", kind="flag", default=False)],
        positional="video_id",
        pos_min=1,
        pos_max=None,
        examples=["kalo video detail 7301234567890 --range last90Day"],
    ),
]
