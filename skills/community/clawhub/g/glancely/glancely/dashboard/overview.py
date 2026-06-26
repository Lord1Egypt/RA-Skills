"""Overview panel — composites key signals from all tracker components."""

from __future__ import annotations

import html as html_mod
from typing import Any

from glancely.dashboard.charts import render_sparkline


def _esc(s: Any) -> str:
    return html_mod.escape(str(s))


def resolve_data_key(payload: dict, data_key: str) -> Any:
    """Resolve a dot-notation path into a stats payload dict.

    Example: "summary.by_category_today" → payload["summary"]["by_category_today"]
    """
    parts = data_key.split(".")
    current: Any = payload
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def render_overview_panel(components_meta: list[dict]) -> str:
    """Render the overview panel compositing key info from all components.

    Args:
        components_meta: List of dicts, each with:
            - name: str
            - title: str
            - overview: dict from chart.toml [overview] section
            - payload: dict from stats.py output

    Returns:
        HTML string for the overview panel section.
    """
    contributing = [m for m in components_meta if m.get("overview", {}).get("enabled") is not False]
    if not contributing:
        return ""

    cards_html = []
    for meta in contributing:
        ov = meta.get("overview", {})
        payload = meta.get("payload", {})
        card_type = ov.get("card_type", "stat")
        label = ov.get("label", meta.get("title", ""))
        data_key = ov.get("data_key", "")
        suffix = ov.get("suffix", "")
        color = ov.get("color", "")

        raw_value = resolve_data_key(payload, data_key) if data_key else None

        if card_type == "sparkline":
            # If data_key points to summary, draw a sparkline from rows
            rows = payload.get("rows", [])
            value_field = ov.get("value_field", "value")
            if rows:
                spark_values = [
                    float(r.get(value_field, 0))
                    for r in rows[-14:]  # last 14 data points
                    if r.get(value_field) is not None
                ]
                spark_svg = (
                    render_sparkline(
                        spark_values,
                        width=ov.get("width", 120),
                        height=ov.get("height", 30),
                        color=color or "var(--ok)",
                    )
                    if spark_values
                    else ""
                )
            else:
                spark_svg = ""
            val_str = _esc(raw_value) if raw_value is not None else "—"
            cards_html.append(
                f'<div class="ov-card ov-sparkline">'
                f'<span class="ov-label">{_esc(label)}</span>'
                f"{spark_svg}"
                f'<span class="ov-value">{val_str}{_esc(suffix)}</span>'
                f"</div>"
            )

        elif card_type == "badge":
            cls = "ok" if raw_value else "bad" if raw_value is False else "muted"
            text = str(raw_value) if raw_value is not None else "—"
            cards_html.append(
                f'<div class="ov-card ov-badge">'
                f'<span class="ov-label">{_esc(label)}</span>'
                f'<span class="badge {cls} ov-badge-value">{_esc(text)}</span>'
                f"</div>"
            )

        elif card_type == "progress":
            max_v = ov.get("max_value", 100)
            current = float(raw_value) if raw_value is not None else 0
            pct = min(current / max_v * 100, 100) if max_v > 0 else 0
            cards_html.append(
                f'<div class="ov-card ov-progress">'
                f'<span class="ov-label">{_esc(label)}</span>'
                f'<div class="progress-track ov-track">'
                f'<div class="progress-fill" style="width:{pct:.0f}%;'
                f'background:{color or "var(--ok)"}"></div></div>'
                f'<span class="ov-value">{current:.0f}{_esc(suffix)}</span>'
                f"</div>"
            )

        else:  # "stat" — default
            val_str = ""
            if isinstance(raw_value, bool):
                val_str = "done" if raw_value else "pending"
            elif isinstance(raw_value, (int, float)):
                val_str = f"{raw_value}{suffix}"
            elif isinstance(raw_value, dict):
                val_str = ", ".join(f"{k}: {v}" for k, v in raw_value.items())
            else:
                val_str = str(raw_value) if raw_value is not None else "—"
            cards_html.append(
                f'<div class="ov-card ov-stat">'
                f'<span class="ov-label">{_esc(label)}</span>'
                f'<span class="ov-value">{_esc(val_str)}</span>'
                f"</div>"
            )

    return (
        f'<section class="panel overview-panel">'
        f"<header><h2>Overview</h2></header>"
        f'<div class="overview-grid">{"".join(cards_html)}</div>'
        f"</section>"
    )
