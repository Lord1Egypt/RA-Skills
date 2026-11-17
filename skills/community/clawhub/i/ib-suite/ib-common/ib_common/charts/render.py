"""Dual-product chart rendering: interactive HTML + static PNG.

Every chart is archived twice — an interactive .html for exploration and a
static .png (rendered by kaleido, no browser needed) for pasting into
reports/Lark. Downstream chart builders produce a plotly Figure and hand it
here; this module owns file I/O so builders stay pure.
"""
from __future__ import annotations
from pathlib import Path
import plotly.graph_objects as go


def render(fig: go.Figure, out_dir: str | Path, name: str) -> dict[str, Path]:
    """Write fig as <name>.html and <name>.png into out_dir; return both paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    html_path = out / f"{name}.html"
    png_path = out / f"{name}.png"
    fig.write_html(str(html_path), include_plotlyjs="cdn")
    fig.write_image(str(png_path), format="png", scale=2)   # kaleido backend
    return {"html": html_path, "png": png_path}
