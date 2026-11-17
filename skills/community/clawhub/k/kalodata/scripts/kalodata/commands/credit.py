"""`kalo credit` — remaining API credit quota."""

from __future__ import annotations

import datetime
import json

from .. import api, render
from ..core import Command


def _fmt_date(ms) -> str:
    try:
        return datetime.datetime.fromtimestamp(float(ms) / 1000, tz=datetime.timezone.utc).strftime(
            "%Y-%m-%d"
        )
    except (TypeError, ValueError):
        return str(ms)


def usage(cfg, opts, args):
    data = api.request(cfg, "/credit/usage", {}, method="GET")
    rows = api.as_list(data)
    if opts.get("json"):
        render.out(json.dumps(rows, ensure_ascii=False))
        return 0
    if not rows:
        render.emit_empty("credits", "no active credit packages on this account")
        return 0
    display = [
        {
            "type": r.get("type"),
            "remain": r.get("remain"),
            "total": r.get("total"),
            "expires": _fmt_date(r.get("endTime")),
        }
        for r in rows
    ]
    display.sort(key=lambda r: str(r["type"]))
    render.emit_table("credits", display, ("type", "remain", "total", "expires"))
    return 0


COMMANDS = [
    Command(
        path="credit",
        summary="Remaining API credit quota per endpoint group",
        handler=usage,
        examples=["kalo credit"],
    ),
]
