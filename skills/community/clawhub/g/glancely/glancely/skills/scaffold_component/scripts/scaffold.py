#!/usr/bin/env python3
"""scaffold.py — create a new tracking component end-to-end.

Usage:
    ./scaffold.py --name coffee_intake --title "Coffee" \\
        --field shots:int --field notes:text \\
        --cron "0 9 * * *" --notify "How much coffee today?"

Steps:
    1. Validate name/title/fields.
    2. Render templates/component/* into skills/<name>/.
    3. Run migrations for the new component → its tables appear in data.db.
    4. (TODO) Register openclaw cron if --cron is supplied.
    5. (TODO) Trigger dashboard rebuild.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core import openclaw_cron  # noqa: E402
from glancely.core.storage import apply_component_migrations  # noqa: E402

GLANCE_HOME = Path(os.environ.get("GLANCE_HOME", Path.home() / ".glancely"))
SKILLS_ROOT = GLANCE_HOME / "components"
SKILLS_ROOT.mkdir(parents=True, exist_ok=True)

TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates" / "component"

FIELD_TYPE_TO_SQL = {
    "int": "INTEGER",
    "integer": "INTEGER",
    "float": "REAL",
    "real": "REAL",
    "text": "TEXT",
    "str": "TEXT",
    "string": "TEXT",
    "bool": "INTEGER",
}

NUMERIC_FIELD_TYPES = frozenset({"int", "integer", "float", "real"})


def _infer_chart_type(fields: list[tuple[str, str]]) -> str:
    """Pick heatmap for numeric trackers, calendar_grid for text/bool."""
    if not fields:
        return "calendar_grid"
    for _name, ftype in fields:
        if ftype.lower() in NUMERIC_FIELD_TYPES:
            return "heatmap"
    return "calendar_grid"

NAME_RE = re.compile(r"^[a-z][a-z0-9_]{1,40}$")


class ScaffoldError(RuntimeError):
    pass


def parse_field(spec: str) -> tuple[str, str]:
    if ":" not in spec:
        raise ScaffoldError(f"--field {spec!r} must be name:type (e.g. shots:int)")
    name, ftype = spec.split(":", 1)
    name = name.strip()
    ftype = ftype.strip().lower()
    if not re.match(r"^[a-z][a-z0-9_]{0,40}$", name):
        raise ScaffoldError(f"Invalid field name {name!r}")
    if ftype not in FIELD_TYPE_TO_SQL:
        raise ScaffoldError(
            f"Unsupported field type {ftype!r}. Use one of: {', '.join(FIELD_TYPE_TO_SQL)}"
        )
    return name, ftype


def render(template_path: Path, mapping: dict) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, val in mapping.items():
        text = text.replace("{{" + key + "}}", str(val))
        text = text.replace("{{" + key + "!r}}", repr(val))
    return text


def _next_panel_order() -> int:
    existing = []
    for child in SKILLS_ROOT.iterdir():
        cfg = child / "component.toml"
        if not cfg.is_file():
            continue
        for line in cfg.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*order\s*=\s*(\d+)", line)
            if m:
                existing.append(int(m.group(1)))
                break
    return (max(existing) + 10) if existing else 10


def build_mapping(args, fields: list[tuple[str, str]]) -> dict:
    name = args.name
    title = args.title or name.replace("_", " ").title()
    fields_sql = "".join(f",\n    {fn}        {FIELD_TYPE_TO_SQL[ft]}" for fn, ft in fields)
    if not any(fn == "note" for fn, _ in fields):
        fields_sql += ",\n    note        TEXT"
    fields_doc = (
        "\n".join(f"- `{fn}` ({ft})" for fn, ft in fields)
        or "_No typed fields. Free-form `--note` only._"
    )
    example_args = (
        " ".join(f"--{fn.replace('_', '-')} <{ft}>" for fn, ft in fields[:2]) or '--note "..."'
    )
    cron_block = ""
    if args.cron:
        cron_block = (
            "\n[cron]\n"
            f'schedule = "{args.cron}"\n'
            'command  = "python3 scripts/notify.py"\n'
            f'description = "{title} reminder"\n'
        )
    inferred = _infer_chart_type(fields) if args.chart_type == "auto" else args.chart_type
    first_numeric = "_presence"
    for fn, ft in fields:
        if ft.lower() in NUMERIC_FIELD_TYPES:
            first_numeric = fn
            break
    color_scheme = "green" if inferred == "heatmap" else "blue"
    return {
        "name": name,
        "title": title,
        "title_lower": title.lower(),
        "description": args.description or f"{title} tracking.",
        "order": args.order or _next_panel_order(),
        "freshness_hours": args.freshness_hours,
        "chart_type": inferred,
        "first_numeric": first_numeric,
        "color_scheme": color_scheme,
        "cron_block": cron_block,
        "fields_sql": fields_sql,
        "fields_doc": fields_doc,
        "fields_python_list": repr(fields),
        "example_args": example_args,
        "created_date": date.today().isoformat(),
        "notification_text": args.notify or f"Time to log {title}.",
    }


def render_tree(mapping: dict, dest: Path, want_notify: bool) -> list[Path]:
    written: list[Path] = []
    for src in TEMPLATE_ROOT.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(TEMPLATE_ROOT)
        if rel.name == "notify.py.tmpl" and not want_notify:
            continue
        out_rel = Path(*[p.replace("{{name}}", mapping["name"]) for p in rel.parts])
        if out_rel.name.endswith(".tmpl"):
            out_rel = out_rel.with_name(out_rel.name[:-5])
        out_path = dest / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render(src, mapping), encoding="utf-8")
        if out_path.suffix == ".py":
            out_path.chmod(0o755)
        written.append(out_path)
    return written


def scaffold(args) -> dict:
    if not NAME_RE.match(args.name):
        raise ScaffoldError(f"Invalid component name {args.name!r}; use snake_case 2-40 chars.")
    dest = SKILLS_ROOT / args.name
    if dest.exists() and not args.force:
        raise ScaffoldError(f"{dest} already exists. Use --force to overwrite.")

    fields = [parse_field(f) for f in (args.field or [])]
    mapping = build_mapping(args, fields)
    written = render_tree(mapping, dest, want_notify=bool(args.cron or args.notify))

    applied = apply_component_migrations(args.name, dest / "migrations")

    cron_status: dict | None = None
    if args.cron:
        try:
            cron_status = openclaw_cron.upsert_component_cron(
                component=args.name,
                label=mapping["title"],
                cron_expr=args.cron,
                tz=args.cron_tz,
                notification_text=mapping["notification_text"],
            )
            cron_status = {"action": cron_status["action"], "job_id": cron_status["job"]["id"]}
        except openclaw_cron.CronConfigMissing as exc:
            cron_status = {"action": "skipped", "reason": str(exc)}

    next_steps = [
        "Run dashboard/build.py to see the new panel.",
        f"Try: python3 {Path(dest, 'scripts', 'log.py')} {mapping['example_args']}",
    ]
    if cron_status and cron_status.get("action") == "skipped":
        next_steps.append(
            "Cron not registered — fill in ~/.glancely/openclaw.toml then re-scaffold with --force."
        )

    return {
        "ok": True,
        "name": args.name,
        "path": str(dest),
        "files_written": [str(p) for p in written],
        "migrations_applied": applied,
        "cron": cron_status,
        "next_steps": next_steps,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Scaffold a new glancely component.")
    p.add_argument("--name", required=True, help="snake_case folder name")
    p.add_argument("--title", help="Dashboard panel title (default: name capitalized)")
    p.add_argument("--description")
    p.add_argument(
        "--field", action="append", help="name:type, repeatable (int, float, text, bool)"
    )
    p.add_argument("--order", type=int)
    p.add_argument("--freshness-hours", type=float, default=24, dest="freshness_hours")
    p.add_argument("--cron", help="Cron schedule, e.g. '0 9 * * *'")
    p.add_argument("--cron-tz", default="America/Denver", dest="cron_tz")
    p.add_argument("--notify", help="Notification text (only used if --cron set)")
    p.add_argument("--force", action="store_true")
    p.add_argument("--chart-type", default="auto", dest="chart_type",
                   help="Chart type for dashboard (bar, pie, donut, heatmap, sparkline, status_card, progress_bar, calendar_grid, timeline)")
    args = p.parse_args(argv)

    try:
        result = scaffold(args)
    except ScaffoldError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
