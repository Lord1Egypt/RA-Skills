"""Shared machinery for rank/detail commands: body building, rendering, batching."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor

from .. import api, render, validate
from ..config import Config
from ..core import Flag
from ..errors import KaloError, UsageError

DETAIL_CONCURRENCY = 5  # client-side batching; upstream detail endpoints take one id

# ---------------------------------------------------------------- flag presets


def common_flags(tier: str, default_range: str = "last30Day") -> list[Flag]:
    return [
        Flag("--region", f"region code ({'|'.join(validate.REGIONS)})", metavar="REGION"),
        Flag(
            "--range",
            f"date window: {validate.tier_hint(tier)}",
            default=default_range,
            metavar="RANGE",
        ),
        Flag("--currency", "currency code (default from config, USD)", metavar="CUR"),
        Flag("--lang", "language code (default from config, en-US)", metavar="LANG"),
    ]


def list_flags(sort_fields: tuple, default_sort: str = "revenue") -> list[Flag]:
    return [
        Flag("--page", "page number 1-5", kind="int", default=1),
        Flag("--limit", "items per page 5-100", kind="int", default=20),
        Flag("--sort", f"sort field: {'|'.join(sort_fields)}", default=default_sort),
        Flag("--asc", "sort ascending (default descending)", kind="flag", default=False),
        Flag("--fields", "comma-separated extra output fields (see --help)", metavar="F1,F2"),
    ]


def category_flag() -> Flag:
    return Flag(
        "--category", "category id filter (repeatable)", kind="multi", default=[], metavar="ID"
    )


def images_flag() -> Flag:
    return Flag("--images", "include image URLs in the output", kind="flag", default=False)


def apply_images(opts: dict, body: dict, image_field: str) -> None:
    """--images: ask upstream for image URLs and surface the column in the output."""
    if not opts.get("images"):
        return
    body["need_image"] = 1
    spec = opts.get("fields")
    if not spec:
        opts["fields"] = image_field
    elif image_field not in spec:
        opts["fields"] = f"{spec},{image_field}"


# ---------------------------------------------------------------- body helpers


def base_body(cfg: Config, opts: dict, tier: str, default_range: str = "last30Day") -> dict:
    region = (opts.get("region") or cfg.region).upper()
    if region not in validate.REGIONS:
        raise UsageError(
            f"unknown region '{region}'", [f"valid regions: {', '.join(validate.REGIONS)}"]
        )
    rng = opts.get("range") or default_range
    err = validate.check_date_range(rng, tier)
    if err:
        raise UsageError(err)
    return {
        "region": region,
        "language": opts.get("lang") or cfg.language,
        "currency": opts.get("currency") or cfg.currency,
        "date_range": rng,
    }


def put_optional(body: dict, opts: dict, mapping: dict[str, str]) -> None:
    """Copy present opts into the body under upstream field names."""
    for opt_key, field in mapping.items():
        v = opts.get(opt_key)
        if v not in (None, "", []):
            body[field] = v


def put_range(body: dict, opts: dict, opt_key: str, field: str, flag: str) -> None:
    v = opts.get(opt_key)
    if v in (None, ""):
        return
    err = validate.check_minmax(v, flag)
    if err:
        raise UsageError(err)
    body[field] = v


def put_numeric_id(body: dict, opts: dict, opt_key: str, field: str, flag: str) -> None:
    v = opts.get(opt_key)
    if v in (None, ""):
        return
    err = validate.check_numeric_id(v, flag)
    if err:
        raise UsageError(err)
    body[field] = v


def tri_state(opts: dict, on_key: str, off_key: str, on_flag: str, off_flag: str) -> int | None:
    if opts.get(on_key) and opts.get(off_key):
        raise UsageError(f"{on_flag} and {off_flag} are mutually exclusive")
    if opts.get(on_key):
        return 1
    if opts.get(off_key):
        return 0
    return None


# ---------------------------------------------------------------- field/number utils

_NUMERIC_HINTS = (
    "revenue",
    "views",
    "price",
    "followers",
    "count",
    "volumn",
    "rate",
    "roas",
    "gpm",
    "number",
    "sale",
    "viewers",
    "duration",
    "rank",
)


def coerce_numbers(row: dict) -> dict:
    """Upstream returns some numeric fields as strings — normalize at the boundary."""
    out = {}
    for k, v in row.items():
        if isinstance(v, str) and any(h in k for h in _NUMERIC_HINTS):
            try:
                out[k] = float(v) if "." in v else int(v)
                continue
            except ValueError:
                pass
        out[k] = v
    return out


def resolve_fields(opts: dict, default_fields: tuple, all_fields: tuple) -> list[str]:
    spec = opts.get("fields")
    if not spec:
        return list(default_fields)
    fields = list(default_fields)
    for f in [s.strip() for s in spec.split(",") if s.strip()]:
        if f not in all_fields:
            raise UsageError(
                f"unknown field '{f}' for --fields",
                [f"valid fields: {', '.join(all_fields)}"],
            )
        if f not in fields:
            fields.append(f)
    return fields


def summarize_trend(d: dict, full: bool) -> None:
    """revenue_trend arrives ×100 — divide, then compress unless --full."""
    trend = d.get("revenue_trend")
    if not isinstance(trend, list) or not trend:
        return
    values = []
    normalized = []
    for item in trend:
        if isinstance(item, dict):
            fixed = dict(item)
            for k, v in item.items():
                try:
                    fixed[k] = round(float(v) / 100, 2)
                    values.append(fixed[k])
                except (TypeError, ValueError):
                    pass
            normalized.append(fixed)
        else:
            try:
                x = round(float(item) / 100, 2)
                values.append(x)
                normalized.append(x)
            except (TypeError, ValueError):
                normalized.append(item)
    if full or not values:
        d["revenue_trend"] = normalized
        return
    d["revenue_trend"] = {
        "points": len(trend),
        "total": round(sum(values), 2),
        "avg": round(sum(values) / len(values), 2),
        "peak": round(max(values), 2),
    }


# ---------------------------------------------------------------- runners


def run_rank(
    cfg: Config,
    opts: dict,
    *,
    endpoint: str,
    noun: str,
    tier: str,
    default_fields: tuple,
    all_fields: tuple,
    sort_fields: tuple,
    body_extra: dict,
    title_fields: tuple = (),
    suggestions: tuple = (),
    omit_sort: bool = False,
    timeout: float = 30.0,
) -> int:
    body = base_body(cfg, opts, tier)
    page = validate.clamp(int(opts.get("page") or 1), 1, 5)
    limit = validate.clamp(int(opts.get("limit") or 20), 5, 100)
    body["page_number"] = page
    body["page_size"] = limit
    if not omit_sort:
        sort = opts.get("sort") or "revenue"
        if sort not in sort_fields:
            raise UsageError(
                f"invalid --sort '{sort}' for `{noun}`",
                [f"valid sort fields: {', '.join(sort_fields)}"],
            )
        body["sort_field"] = {"field": sort, "type": "ASC" if opts.get("asc") else "DESC"}
    body.update(body_extra)
    fields = resolve_fields(opts, default_fields, all_fields)

    data = api.request(cfg, endpoint, body, timeout=timeout, empty_on_not_found=True)
    rows = [coerce_numbers(r) for r in api.as_list(data)]

    if opts.get("json"):
        render.out(json.dumps(rows, ensure_ascii=False))
        return 0

    context = f"region {body['region']}, {body['date_range']}"
    if not rows:
        render.emit_empty(
            noun,
            context,
            ["Broaden --range, drop filters, or try another --region"],
        )
        return 0

    display = [{k: render.clip(r.get(k)) if k in title_fields else r.get(k) for k in fields} for r in rows]
    render.emit_table(noun, display, fields)
    hints = list(suggestions)
    if len(rows) == limit:
        hints.append(f"More may exist: add `--page {page + 1}` (pages 1-5, --limit up to 100)")
    render.emit_help(hints)
    return 0


def run_detail_batch(
    cfg: Config,
    opts: dict,
    ids: list[str],
    *,
    noun: str,
    fetch,  # fetch(id) -> dict
    postprocess=None,  # postprocess(dict, opts, notes) -> dict
    suggestions: tuple = (),
) -> int:
    def one(entity_id: str):
        try:
            return entity_id, fetch(entity_id), None
        except KaloError as e:
            return entity_id, None, e

    if len(ids) == 1:
        results = [one(ids[0])]
    else:
        with ThreadPoolExecutor(max_workers=DETAIL_CONCURRENCY) as pool:
            results = list(pool.map(one, ids))

    if opts.get("json"):
        payload = [
            {"id": i, "data": d} if e is None else {"id": i, "error": str(e)}
            for i, d, e in results
        ]
        render.out(json.dumps(payload[0] if len(payload) == 1 else payload, ensure_ascii=False))
        return 0 if any(e is None for _, _, e in results) else 1

    ok = 0
    first = True
    notes: list[str] = []
    for entity_id, data, err in results:
        if not first:
            render.out()
        first = False
        if err is not None:
            render.emit_error(f"{noun} {entity_id}: {err}", err.help_lines)
            continue
        if not isinstance(data, dict) or not data:
            render.emit_empty(noun, f"id {entity_id}")
            continue
        ok += 1
        data = coerce_numbers(data)
        if postprocess:
            data = postprocess(data, opts, notes) or data
        render.emit_detail(noun, data)
    render.emit_help(list(dict.fromkeys(notes)) + list(suggestions if ok else ()))
    return 0 if ok or not ids else 1
