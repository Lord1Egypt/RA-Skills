#!/usr/bin/env python3
"""Read-only source-palette parity checks. Output: status<TAB>target<TAB>detail."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


ROOT = Path(sys.argv[1]).resolve()
HOME = Path.home()
RUNTIME = HOME / ".config/hekouwang-terminal"
theme = (RUNTIME / "theme").read_text(encoding="utf-8").strip() if (RUNTIME / "theme").is_file() else ""
p3 = (RUNTIME / "p3").is_file()
paid = (ROOT / "config/themes/_apply_pro.sh").is_file()
issues = 0


def row(status: str, target: str, detail: str = "") -> None:
    global issues
    if status in {"drift", "missing", "unsupported"}:
        issues += 1
    print(f"{status}\t{target}\t{detail}")


def same_file(target: str, source: Path, deployed: Path) -> None:
    if not deployed.is_file():
        row("missing", target, str(deployed))
    elif not source.is_file():
        row("unsupported", target, str(source))
    elif source.read_bytes() == deployed.read_bytes():
        row("same", target, theme)
    else:
        row("drift", target, str(deployed))


def same_text(target: str, source: Path, deployed: Path, drop: tuple[str, ...] = ()) -> None:
    """按行比对，忽略部署时注入的机器本地行（不是漂移，是运行时决定）。"""
    if not deployed.is_file():
        row("missing", target, str(deployed))
    elif not source.is_file():
        row("unsupported", target, str(source))
    else:
        def norm(p: Path) -> list[str]:
            lines = [l.rstrip() for l in p.read_text(encoding="utf-8", errors="replace").splitlines()
                     if not any(l.strip().startswith(d) for d in drop)]
            while lines and not lines[-1]:
                lines.pop()
            return lines
        if norm(source) == norm(deployed):
            row("same", target, theme)
        else:
            row("drift", target, str(deployed))


if not theme:
    row("missing", "theme", str(RUNTIME / "theme"))
    raise SystemExit(2)

source_profile = ROOT / f"config/themes/{theme}.json"
active_profile = HOME / "Library/Application Support/iTerm2/DynamicProfiles/hekouwang-active-theme.json"
if not active_profile.is_file():
    row("missing", "iTerm2", str(active_profile))
elif not source_profile.is_file():
    row("unsupported", "iTerm2", theme)
else:
    try:
        def neutral_colors(obj) -> None:
            """P3 只改部署档：颜色分量被重算、Color Space 变 Display P3。
            仓库 JSON 仍是 sRGB，所以比对时把颜色压成占位符，颜色空间另起 p3 行验。"""
            if isinstance(obj, dict):
                if "Red Component" in obj:
                    obj.clear()
                    obj["Color Space"] = "color"
                    return
                for val in obj.values():
                    neutral_colors(val)
            elif isinstance(obj, list):
                for val in obj:
                    neutral_colors(val)

        def normalized(path: Path) -> dict:
            data = json.loads(path.read_text(encoding="utf-8"))
            profile = data["Profiles"][0]
            for key in ("Normal Font", "Non Ascii Font", "Name", "Rows", "Columns",
                        "Transparency", "Blur", "Blur Radius", "Thin Strokes"):
                profile.pop(key, None)
            if p3:
                neutral_colors(profile)
            return data
        row("same" if normalized(source_profile) == normalized(active_profile) else "drift", "iTerm2", theme)
        if p3:
            active = json.loads(active_profile.read_text(encoding="utf-8"))["Profiles"][0]
            missing = [key for key in ("Background Color", "Ansi 1 Color")
                       if (active.get(key) or {}).get("Color Space") != "Display P3"]
            row("same" if not missing else "drift", "iTerm2 P3",
                f"not Display P3: {', '.join(missing)}" if missing else "Background Color / Ansi 1 Color")
    except (OSError, ValueError, KeyError, IndexError) as exc:
        row("drift", "iTerm2", f"parse: {exc}")

if not paid:
    row("paid", "Ghostty / Warp / cmux / Tabby / Terminal", "paid coverage")
    raise SystemExit(1 if issues else 0)

eco = ROOT / f"config/themes/ecosystem/{theme}"
# colors.sh 部署时会被追加一条机器本地的图标决策（HEKOUWANG_SOLO_NF），
# 那不是漂移，比对时按行剔掉。
same_text("shell colors", eco / "colors.sh", RUNTIME / "current/colors.sh",
          drop=("export HEKOUWANG_SOLO_NF=",))
same_file("git diff", eco / "delta.gitconfig", RUNTIME / "current/delta.gitconfig")
same_file("tmux", eco / "tmux.conf", RUNTIME / "current/tmux.conf")
ghostty_theme = f"hekouwang-{theme}-p3" if p3 else f"hekouwang-{theme}"
same_file("Ghostty theme", ROOT / f"config/themes/ghostty/{ghostty_theme}", HOME / f".config/ghostty/themes/{ghostty_theme}")

ghostty_cfg = HOME / ".config/ghostty/config"
if ghostty_cfg.is_file():
    text = ghostty_cfg.read_text(encoding="utf-8", errors="replace")
    if p3:
        # P3 必须同时钉住 -p3 主题和 display-p3；按整行比对，别用宽松正则伤到 font-family 等键。
        lines = {line.strip() for line in text.splitlines()}
        ok = f"theme = {ghostty_theme}" in lines and "window-colorspace = display-p3" in lines
    else:
        ok = f"theme = hekouwang-{theme}" in text
    row("same" if ok else "drift", "Ghostty config", str(ghostty_cfg))
else:
    row("not-installed", "Ghostty", "no config")

warp_theme = ROOT / f"config/themes/warp/{theme.replace('-', '_')}.yaml"
deployed_warp = HOME / f".warp/themes/{theme.replace('-', '_')}.yaml"
if (HOME / ".warp").exists():
    same_file("Warp theme", warp_theme, deployed_warp)
else:
    row("not-installed", "Warp", "no ~/.warp")

for target, path in (
    ("cmux", HOME / ".config/cmux/cmux.json"),
    ("Tabby", HOME / "Library/Application Support/tabby/config.yaml"),
):
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")
        if target == "cmux":
            ok = "HKW-CMUX-BEGIN" in text
        else:
            # 新英文名 + 旧 OneLook 主题名都算已对齐
            ok = (
                f"Hekouwang Terminal {theme}" in text
                or f"OneLook {theme}" in text
            )
        row("same" if ok else "drift", target, str(path))
    else:
        row("not-installed", target, str(path))

terminal_plist = HOME / "Library/Preferences/com.apple.Terminal.plist"
row("manual" if terminal_plist.is_file() else "not-installed", "macOS Terminal", "verify after fully quitting and reopening")
raise SystemExit(1 if issues else 0)
