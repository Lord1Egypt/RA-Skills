"""Load and validate chart.toml per component directory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

SUPPORTED_CHART_TYPES = frozenset(
    {
        "bar",
        "pie",
        "donut",
        "heatmap",
        "sparkline",
        "status_card",
        "progress_bar",
        "calendar_grid",
        "timeline",
    }
)

SUPPORTED_OVERVIEW_TYPES = frozenset({"stat", "sparkline", "badge", "progress"})

REQUIRED_DATA_FIELDS: dict[str, set[str]] = {
    "bar": {"source"},
    "pie": {"source"},
    "donut": {"source"},
    "heatmap": {"source", "date_field", "value_field"},
    "sparkline": {"source", "value_field"},
    "status_card": set(),  # no data section required
    "progress_bar": {"source", "value_field"},
    "calendar_grid": {"source", "date_field", "value_field"},
    "timeline": {"source", "time_field", "title_field"},
}


def load_chart_config(component_dir: Path) -> dict[str, Any] | None:
    """Read and validate chart.toml from a component directory.

    Returns None if chart.toml does not exist (component renders as basic card).
    Returns parsed + validated dict on success.
    Raises ValueError for invalid configuration.
    """
    cfg_path = component_dir / "chart.toml"
    if not cfg_path.is_file():
        return None

    with cfg_path.open("rb") as fh:
        cfg = tomllib.load(fh)

    chart = cfg.get("chart")
    if not chart:
        raise ValueError("chart.toml requires a [chart] section")

    chart_type = chart.get("type")
    if not chart_type:
        raise ValueError("chart.toml [chart] section requires 'type'")
    if chart_type not in SUPPORTED_CHART_TYPES:
        raise ValueError(
            f"Unsupported chart type {chart_type!r}. "
            f"Use one of: {', '.join(sorted(SUPPORTED_CHART_TYPES))}"
        )

    if chart_type != "status_card":
        data = cfg.get("chart", {}).get("data")
        if not data:
            raise ValueError(
                f"chart.toml [chart.data] section required for chart type {chart_type!r}"
            )
        required = REQUIRED_DATA_FIELDS.get(chart_type, set())
        missing = required - set(data.keys())
        if missing:
            raise ValueError(
                f"chart.toml [chart.data] missing required fields for {chart_type!r}: {', '.join(sorted(missing))}"
            )
        source = data.get("source")
        if source not in ("rows", "summary"):
            raise ValueError(
                f"chart.toml [chart.data].source must be 'rows' or 'summary', got {source!r}"
            )

    overview = cfg.get("overview", {})
    if overview.get("enabled") is not False:
        ov_type = overview.get("card_type", "stat")
        if ov_type not in SUPPORTED_OVERVIEW_TYPES:
            raise ValueError(
                f"Unsupported overview card_type {ov_type!r}. "
                f"Use one of: {', '.join(sorted(SUPPORTED_OVERVIEW_TYPES))}"
            )
        if ov_type in ("sparkline", "progress") and not overview.get("data_key"):
            raise ValueError(f"overview card_type {ov_type!r} requires 'data_key'")
    else:
        overview = {"enabled": False}

    return {"chart": chart, "overview": overview}
