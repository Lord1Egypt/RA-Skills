"""Walk user components (default ~/.glancely/components/) and return in dashboard order.

A component is any folder with a component.toml. Nothing else needs registering.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


GLANCE_HOME = Path(os.environ.get("GLANCE_HOME", Path.home() / ".glancely"))
USER_COMPONENTS_ROOT = GLANCE_HOME / "components"


@dataclass
class Component:
    name: str
    path: Path
    config: dict[str, Any] = field(default_factory=dict)

    @property
    def title(self) -> str:
        return self.config.get("component", {}).get("title", self.name)

    @property
    def panel_enabled(self) -> bool:
        return bool(self.config.get("panel", {}).get("enabled", True))

    @property
    def panel_order(self) -> int:
        return int(self.config.get("panel", {}).get("order", 100))

    @property
    def freshness_hours(self) -> float | None:
        v = self.config.get("panel", {}).get("freshness_hours")
        return float(v) if v is not None else None

    @property
    def cron(self) -> dict[str, Any] | None:
        c = self.config.get("cron")
        return c if c else None

    @property
    def migrations_dir(self) -> Path:
        return self.path / "migrations"

    @property
    def stats_script(self) -> Path:
        return self.path / "scripts" / "stats.py"

    @property
    def auth(self) -> dict[str, Any] | None:
        a = self.config.get("auth")
        return a if a else None

    @property
    def chart_config(self) -> dict | None:
        """Chart configuration from chart.toml, or None if no chart config."""
        from glancely.dashboard.load_chart_config import load_chart_config
        return load_chart_config(self.path)


def load_component(path: Path) -> Component | None:
    cfg_path = path / "component.toml"
    if not cfg_path.is_file():
        return None
    with cfg_path.open("rb") as fh:
        cfg = tomllib.load(fh)
    declared = cfg.get("component", {}).get("name")
    name = declared or path.name
    if declared and declared != path.name:
        raise ValueError(f"component.toml name {declared!r} does not match folder {path.name!r}")
    return Component(name=name, path=path, config=cfg)


def discover_components(
    skills_root: Path | None = None,
    user_root: Path | None = None,
    panel_only: bool = False,
) -> list[Component]:
    """Discover components from user_root (default ~/.glancely/components/).

    If skills_root is also provided, discover from both locations.
    """
    if user_root is None:
        user_root = USER_COMPONENTS_ROOT

    components: list[Component] = []

    roots: list[Path] = [user_root]
    if skills_root is not None:
        roots.insert(0, skills_root)

    seen: set[str] = set()
    for root in roots:
        if not root.is_dir():
            continue
        for child in sorted(p for p in root.iterdir() if p.is_dir()):
            comp = load_component(child)
            if comp is None:
                continue
            if comp.name == "scaffold_component":
                continue
            if panel_only and not comp.panel_enabled:
                continue
            if comp.name in seen:
                continue
            seen.add(comp.name)
            components.append(comp)

    components.sort(key=lambda c: (c.panel_order, c.name))
    return components


if __name__ == "__main__":
    import json
    import sys

    skills_root = Path(__file__).resolve().parents[2] / "skills"
    if len(sys.argv) > 1:
        skills_root = Path(sys.argv[1]).resolve()
    out = [
        {
            "name": c.name,
            "title": c.title,
            "order": c.panel_order,
            "panel_enabled": c.panel_enabled,
            "cron": c.cron,
        }
        for c in discover_components(skills_root=skills_root)
    ]
    print(json.dumps(out, indent=2))
