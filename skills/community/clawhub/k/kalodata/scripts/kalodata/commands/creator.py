"""`kalo creator` — creator rank / detail."""

from __future__ import annotations

from .. import api, render
from ..core import Command, Flag
from ..errors import UsageError
from . import common

SORT_FIELDS = (
    "revenue",
    "revenue_growth_rate",
    "content_views",
    "creator_followers",
    "sales_volumn",
    "video_revenue",
    "live_revenue",
)
ALL_FIELDS = (
    "creator_id",
    "creator_nickname",
    "creator_handle",
    "revenue",
    "revenue_growth_rate",
    "sales_volumn",
    "video_revenue",
    "live_revenue",
    "content_views",
    "creator_followers",
    "image_url",
)
DEFAULT_FIELDS = ("creator_id", "creator_handle", "revenue", "creator_followers")


def rank(cfg, opts, args):
    body = {}
    common.put_optional(
        body, opts, {"shop": "shop_id", "type": "creator_type", "engagement": "engagement_rate", "keyword": "keyword"}
    )
    common.put_numeric_id(body, opts, "product", "product_id", "--product")
    common.put_range(body, opts, "revenue", "revenue_range", "--revenue")
    common.put_range(body, opts, "followers", "followers_range", "--followers")
    if opts.get("category"):
        body["category_ids"] = opts["category"]
    common.apply_images(opts, body, "image_url")
    return common.run_rank(
        cfg,
        opts,
        endpoint="/tiktok/creator/rank",
        noun="creators",
        tier="rank",
        default_fields=DEFAULT_FIELDS,
        all_fields=ALL_FIELDS,
        sort_fields=SORT_FIELDS,
        body_extra=body,
        title_fields=("creator_nickname",),
        suggestions=(
            "Run `kalo creator detail <creator_id>` for contact info, GPM, trend",
            "Run `kalo video rank --creator <creator_id>` for a creator's top videos",
        ),
    )


def detail(cfg, opts, ids):
    any_handle = any(not i.lstrip("@").isdigit() for i in ids)

    def fetch(ident):
        body = common.base_body(cfg, opts, "detail")
        body["need_extra"] = True
        if ident.lstrip("@").isdigit():
            body["creator_id"] = ident.lstrip("@")
            endpoint = "/tiktok/creator/detail"
            if opts.get("shop"):
                body["shop_id"] = opts["shop"]
            if opts.get("category"):
                try:
                    body["category_ids"] = [int(c) for c in opts["category"]]
                except ValueError:
                    raise UsageError("--category must be numeric ids for creator detail") from None
        else:
            # upstream rejects a leading @ and matches handles fuzzily
            body["creator_handle"] = ident.lstrip("@")
            endpoint = "/tiktok/creator/detailByHandle"
        return api.request(cfg, endpoint, body)

    def post(d, o, notes):
        if any_handle:
            notes.append(
                "Handle lookup is fuzzy — check creator_handle in the result matches what you meant"
            )
        render.truncate_text(
            d, "creator_bio", 300, o.get("full"), notes, "Add `--full` for the complete bio"
        )
        common.summarize_trend(d, o.get("full"))
        if not o.get("full"):
            notes.append("Add `--full` for the day-by-day revenue_trend series")
        return d

    return common.run_detail_batch(
        cfg,
        opts,
        ids,
        noun="creator",
        fetch=fetch,
        postprocess=post,
        suggestions=("Run `kalo product detail <top3_product_ids[i]>` for their best sellers",),
    )


def images(cfg, opts, ids):
    import json

    body = common.base_body(cfg, opts, "detail")
    body["creator_ids"] = ids
    body["need_image"] = 1
    data = api.request(cfg, "/tiktok/creator/images", body)
    mapping = data if isinstance(data, dict) else {}
    if opts.get("json"):
        render.out(json.dumps(mapping, ensure_ascii=False))
        return 0
    if not mapping:
        render.emit_empty("creator images", f"{len(ids)} id(s)")
        return 0
    rows = [{"creator_id": k, "image_url": v} for k, v in mapping.items()]
    render.emit_table("creator_images", rows, ("creator_id", "image_url"))
    return 0


COMMANDS = [
    Command(
        path="creator rank",
        summary="Top TikTok Shop creators by revenue",
        handler=rank,
        flags=common.common_flags("rank")
        + common.list_flags(SORT_FIELDS)
        + [
            common.category_flag(),
            Flag("--shop", "filter by shop id", metavar="ID"),
            Flag("--product", "filter by product id (numeric)", metavar="ID"),
            Flag("--revenue", 'revenue range "min-max"', metavar="MIN-MAX"),
            Flag("--followers", 'followers range "min-max"', metavar="MIN-MAX"),
            Flag("--type", "creator type", choices=("BELONGED_TO_SELLER", "INDEPENDENT")),
            Flag("--engagement", "engagement tier", choices=("LOW", "MEDIUM", "HIGH")),
            Flag("--keyword", "creator name or id keyword", metavar="TEXT"),
            common.images_flag(),
        ],
        examples=[
            "kalo creator rank --region US --followers 10000-1000000",
            "kalo creator rank --product 1729386274",
        ],
    ),
    Command(
        path="creator detail",
        summary="Full profile for one or more creators, by id or @handle (contact, GPM, trend)",
        handler=lambda cfg, opts, args: detail(cfg, opts, args),
        flags=common.common_flags("detail")
        + [
            common.category_flag(),
            Flag("--shop", "scope metrics to one shop id (id lookups only)", metavar="ID"),
            Flag("--full", "include full bio and revenue_trend series", kind="flag", default=False),
        ],
        positional="creator_id_or_handle",
        pos_min=1,
        pos_max=None,
        examples=["kalo creator detail 7212345678", "kalo creator detail @myfamilypov"],
    ),
    Command(
        path="creator images",
        summary="Avatar image URLs for a batch of creator ids",
        handler=lambda cfg, opts, args: images(cfg, opts, args),
        flags=common.common_flags("detail"),
        positional="creator_id",
        pos_min=1,
        pos_max=None,
        examples=["kalo creator images 7212345678 7212345679"],
    ),
]
