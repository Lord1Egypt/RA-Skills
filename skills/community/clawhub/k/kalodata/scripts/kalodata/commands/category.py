"""`kalo category` — category rank / detail / search."""

from __future__ import annotations

import json

from .. import api, render
from ..core import Command, Flag
from . import common

SORT_FIELDS = ("revenue", "revenue_growth_rate", "top3_shop_revenue_ratio", "average_revenue")
ALL_FIELDS = (
    "category_id",
    "category_name",
    "rank",
    "revenue",
    "sale",
    "average_revenue",
    "revenue_growth_rate",
    "top3_shop_revenue_ratio",
)
DEFAULT_FIELDS = ("category_id", "category_name", "revenue", "revenue_growth_rate")


def rank(cfg, opts, args):
    body = {"need_extra": True}
    if opts.get("category"):
        body["category_ids"] = opts["category"]
    if opts.get("level"):
        body["category_level"] = opts["level"]
    common.put_range(body, opts, "revenue", "revenue_range", "--revenue")
    return common.run_rank(
        cfg,
        opts,
        endpoint="/tiktok/category/rank",
        noun="categories",
        tier="category",
        default_fields=DEFAULT_FIELDS,
        all_fields=ALL_FIELDS,
        sort_fields=SORT_FIELDS,
        body_extra=body,
        title_fields=("category_name",),
        suggestions=(
            "Run `kalo category detail <category_id>` for the revenue split + trend",
            "Run `kalo product rank --category <category_id>` for its top products",
        ),
    )


def detail(cfg, opts, ids):
    def fetch(category_id):
        body = common.base_body(cfg, opts, "category")
        body.update(category_id=category_id, need_extra=True)
        return api.request(cfg, "/tiktok/category/detail", body)

    def post(d, o, notes):
        common.summarize_trend(d, o.get("full"))
        if not o.get("full"):
            notes.append("Add `--full` for the day-by-day revenue_trend series")
        return d

    return common.run_detail_batch(
        cfg,
        opts,
        ids,
        noun="category",
        fetch=fetch,
        postprocess=post,
        suggestions=("Run `kalo shop rank --category <category_id>` for its top shops",),
    )


def search(cfg, opts, args):
    body = common.base_body(cfg, opts, "full")
    body["keyword"] = args[0]
    data = api.request(cfg, "/tiktok/category/searchByKeyword", body, empty_on_not_found=True)
    rows = api.as_list(data)
    if opts.get("json"):
        render.out(json.dumps(rows, ensure_ascii=False))
        return 0
    if not rows:
        render.emit_empty(
            "categories",
            f"keyword '{args[0]}', region {body['region']}",
            ["Try a broader or English keyword"],
        )
        return 0
    fields = [k for k in ("id", "name", "level") if any(k in r for r in rows)] or ["id", "name"]
    render.emit_table("categories", rows, fields)
    render.emit_help(
        [
            "Run `kalo product rank --category <id>` for top products in a category",
            "Run `kalo category detail <id>` for category-level metrics",
        ]
    )
    return 0


COMMANDS = [
    Command(
        path="category rank",
        summary="Top TikTok Shop categories by revenue",
        handler=rank,
        flags=common.common_flags("category", default_range="last30Day")
        + common.list_flags(SORT_FIELDS)
        + [
            common.category_flag(),
            Flag("--level", "category level", choices=("1", "2", "3")),
            Flag("--revenue", 'revenue range "min-max"', metavar="MIN-MAX"),
        ],
        examples=["kalo category rank --region US --level 1"],
    ),
    Command(
        path="category detail",
        summary="Full metrics for one or more categories",
        handler=lambda cfg, opts, args: detail(cfg, opts, args),
        flags=common.common_flags("category")
        + [Flag("--full", "include the full revenue_trend series", kind="flag", default=False)],
        positional="category_id",
        pos_min=1,
        pos_max=None,
        examples=["kalo category detail 601739"],
    ),
    Command(
        path="category search",
        summary="Resolve category ids by keyword",
        handler=search,
        flags=common.common_flags("full"),
        positional="keyword",
        pos_min=1,
        pos_max=1,
        examples=["kalo category search 'beauty'"],
    ),
]
