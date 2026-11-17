#!/usr/bin/env python3
"""generate_plantuml.py — Convert PlantUML source to SVG, PNG, PDF, or ASCII art.

Unified cross-platform (Linux / macOS / Windows) replacement for the previous
Bash + PowerShell script pair. Requires only Python 3.8+ from the host; the
rendering backends (Docker / local plantuml.jar / opt-in Kroki) are unchanged.

Usage:
    python generate_plantuml.py <input.puml> [output_dir] [options]

Options:
    --format {svg,png,pdf,txt}   Output format (default: svg)
    --cjk                        Enable CJK (Chinese/Japanese/Korean) font support
    --no-fix                     Disable automatic aspect ratio correction
    --min-aspect N               Min width/height ratio before correction (default: 0.7)
    --max-aspect N               Max width/height ratio before correction (default: 1.4)
    --dark-mode                  Also emit <basename>.dark.<fmt> companion
    --no-a4-check                Disable automatic A4 paper fit validation
    --min-font-pt N              Min legible font size on A4 paper (default: 8.0)
    --use-public-server          OPT-IN: render via Kroki (kroki.io by default).
                                 Uploads diagram source to a third party.
                                 Override host via PLANTUML_PUBLIC_SERVER env var.

Privacy notice:
    This script renders LOCALLY by default. Diagram source is NOT transmitted
    off-host unless --use-public-server is passed. Backend priority:
        1. Docker (plantuml/plantuml)  — preferred, fully local
        2. Local plantuml.jar          — offline fallback (Java required)
        3. Kroki public server         — OPT-IN ONLY
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Optional, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

# A4 paper dimensions in CSS pixels @ 96 DPI (1in = 96px, A4 = 210×297 mm)
A4_PORTRAIT_W = 794
A4_PORTRAIT_H = 1123
A4_LANDSCAPE_W = 1123
A4_LANDSCAPE_H = 794

# Body font size (px) produced by the mandatory uml-diagrams.org preamble
DEFAULT_FONT_PX = 12.0

MAX_FIX_ATTEMPTS = 3

STRICTUML_RE = re.compile(
    r"(?im)^[ \t]*skinparam[ \t]+style[ \t]+strictuml[ \t]*\r?\n?"
)

CJK_RANGES = (
    (0x4E00, 0x9FFF),
    (0x3400, 0x4DBF),
    (0x20000, 0x2A6DF),
    (0xF900, 0xFAFF),
    (0x2F800, 0x2FA1F),
    (0x3000, 0x303F),
    (0xFF00, 0xFFEF),
    (0x3040, 0x309F),
    (0x30A0, 0x30FF),
    (0xAC00, 0xD7AF),
)

SPACING_GUARD_BLOCK = """<style>
root {
  padding 8
  wrapWidth 220
}
activityDiagram {
  activity { padding 8 }
}
sequenceDiagram {
  participant { padding 8 }
  box { padding 8 }
}
classDiagram {
  class { padding 8; MinimumWidth 100 }
}
stateDiagram {
  state { padding 8 }
}
</style>
skinparam NodeSep 35
skinparam RankSep 35"""

BARE_STROKE_CSS = """<style>@media (prefers-color-scheme: light) {
/* Bare elements: PlantUML CSS mode may omit stroke on some shapes */
ellipse:not([style*="stroke"]):not([stroke]),
circle:not([style*="stroke"]):not([stroke]) {
 stroke: #000000 !important;
 stroke-width: 0.75 !important;
}
rect[fill="#FFFFFF"]:not([style*="stroke"]):not([stroke]),
rect[fill="#ffffff"]:not([style*="stroke"]):not([stroke]) {
 stroke: #000000 !important;
 stroke-width: 0.75 !important;
}
path[fill="none"]:not([style*="stroke"]):not([stroke]) {
 stroke: #000000 !important;
 stroke-width: 0.75 !important;
}
/* Swimlane headers rendered with white stroke (invisible on white canvas) */
[style*="stroke:#FFFFFF"], [style*="stroke: #FFFFFF"],
[style*="stroke:#ffffff"], [style*="stroke: #ffffff"] {
 stroke: #000000 !important;
}
}</style>"""

DARK_MODE_CSS = """<style>@media (prefers-color-scheme: dark) {
 svg {
 background: transparent !important;
 }
 [style*="background:#FFFFFF"], [style*="background: #FFFFFF"],
 [style*="background:#ffffff"], [style*="background: #ffffff"] {
 background: #1e1e2e !important;
 }
 [fill="#FFFFFF"], [fill="#ffffff"], [fill="#FFF"], [fill="#fff"],
 [fill="#FEFEFE"], [fill="#fefefe"], [fill="#F1F1F1"], [fill="#f1f1f1"],
 [fill="#EEEEEE"], [fill="#eeeeee"], [fill="#ECECEC"], [fill="#ececec"],
 [fill="#FFFFCC"], [fill="#ffffcc"] {
 fill: #1e1e2e !important;
 }
 /* Use case ellipses/circles: transparent fill so outline visible */
 ellipse[fill="#FFFFFF"], ellipse[fill="#ffffff"],
 ellipse[fill="#FFF"], ellipse[fill="#fff"],
 ellipse[fill="#FEFEFE"], ellipse[fill="#fefefe"],
 ellipse[style*="fill:#FFFFFF"], ellipse[style*="fill:#ffffff"],
 circle[fill="#FFFFFF"], circle[fill="#ffffff"],
 circle[fill="#FFF"], circle[fill="#fff"],
 circle[fill="#FEFEFE"], circle[fill="#fefefe"],
 circle[style*="fill:#FFFFFF"], circle[style*="fill:#ffffff"] {
 fill: none !important;
 stroke-width: 1.5 !important;
 }
 [stroke="#000000"], [stroke="#000"], [stroke="#181818"],
 [stroke="#222222"], [stroke="#222"], [stroke="#333333"], [stroke="#333"] {
 stroke: #c9d1d9 !important;
 }
 [style*="stroke:#181818"], [style*="stroke: #181818"],
 [style*="stroke:#000000"], [style*="stroke: #000000"],
 [style*="stroke:#222222"], [style*="stroke: #222222"],
 [style*="stroke:#333333"], [style*="stroke: #333333"] {
 stroke: #c9d1d9 !important;
 }
 [style*="stroke:#FFDD88"], [style*="stroke: #FFDD88"],
 [style*="stroke:#ffdd88"], [style*="stroke: #ffdd88"] {
 stroke: #6e7681 !important;
 }
 text, [fill="#000000"], [fill="#000"], [fill="#181818"], [fill="#222222"] {
 fill: #c9d1d9 !important;
 }
 polygon[fill="#000000"], polygon[fill="#181818"], polygon[fill="#222222"],
 polygon[fill="#333333"] {
 fill: #c9d1d9 !important;
 stroke: #c9d1d9 !important;
 }
 rect[style*="stroke:#000000"], rect[style*="stroke: #000000"],
 rect[style*="stroke:#181818"], rect[style*="stroke: #181818"] {
 stroke: #c9d1d9 !important;
 }
 ellipse[style*="stroke:#000000"], ellipse[style*="stroke: #000000"],
 ellipse[style*="stroke:#181818"], ellipse[style*="stroke: #181818"] {
 stroke: #c9d1d9 !important;
 }
 polygon[style*="stroke:#000000"], polygon[style*="stroke: #000000"],
 polygon[style*="stroke:#181818"], polygon[style*="stroke: #181818"],
 polygon[style*="stroke:#222222"], polygon[style*="stroke: #222222"] {
 stroke: #c9d1d9 !important;
 }
 line[stroke="#181818"], line[stroke="#000000"],
 line[style*="stroke:#181818"], line[style*="stroke: #181818"],
 line[style*="stroke:#000000"], line[style*="stroke: #000000"] {
 stroke: #6e7681 !important;
 stroke-dasharray: 4 3 !important;
 }
 text[font-weight="700"], text[font-weight="bold"] {
 fill: #f0f6fc !important;
 }
  /* Bare elements: PlantUML CSS mode may omit stroke on some shapes */
  ellipse:not([style*="stroke"]):not([stroke]),
  circle:not([style*="stroke"]):not([stroke]) {
  stroke: #c9d1d9 !important;
  stroke-width: 0.75 !important;
  }
  rect[fill="#FFFFFF"]:not([style*="stroke"]):not([stroke]),
  rect[fill="#ffffff"]:not([style*="stroke"]):not([stroke]) {
  stroke: #c9d1d9 !important;
  stroke-width: 0.75 !important;
  }
  path[fill="none"]:not([style*="stroke"]):not([stroke]) {
  stroke: #c9d1d9 !important;
  stroke-width: 0.75 !important;
  }
  /* Swimlane headers rendered with white stroke (invisible on dark canvas) */
  [style*="stroke:#FFFFFF"], [style*="stroke: #FFFFFF"],
  [style*="stroke:#ffffff"], [style*="stroke: #ffffff"] {
  stroke: #c9d1d9 !important;
  }
}</style>"""


def log(msg: str = "") -> None:
    print(msg, flush=True)


def elog(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


# ─────────────────────────────────────────────────────────────────────────────
# Source Sanitization (defensive)
# ─────────────────────────────────────────────────────────────────────────────
def sanitize_puml_source(path: Path) -> None:
    """Strip forbidden `skinparam style strictuml` line from source.

    strictuml degrades key UML shapes (actors→text, use cases→rectangles,
    class header separator lost). All other skinparam lines are preserved.
    """
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    new_text, n = STRICTUML_RE.subn("", text)
    if n > 0:
        elog(
            "  ⓘ Stripped forbidden 'skinparam style strictuml' "
            "(see SKILL.md → Common Failure Patterns)"
        )
        path.write_text(new_text, encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# CJK Detection & Font Substitution
# ─────────────────────────────────────────────────────────────────────────────
def detect_cjk(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    for ch in text:
        cp = ord(ch)
        for lo, hi in CJK_RANGES:
            if lo <= cp <= hi:
                return True
    return False


def prepare_puml_for_cjk(src: Path) -> Path:
    dst = src.with_suffix(src.suffix + ".cjk.puml")
    text = src.read_text(encoding="utf-8", errors="replace")
    text = re.sub(
        r"skinparam\s+defaultFontName\s+\S+",
        'skinparam defaultFontName "WenQuanYi Micro Hei"',
        text,
    )
    if "defaultFontName" not in text:
        text = text.replace(
            "@startuml",
            '@startuml\n!pragma defaultFontName "WenQuanYi Micro Hei"\n'
            'skinparam defaultFontName "WenQuanYi Micro Hei"',
            1,
        )
    dst.write_text(text, encoding="utf-8")
    return dst


# ─────────────────────────────────────────────────────────────────────────────
# Dimension Detection
# ─────────────────────────────────────────────────────────────────────────────
def get_svg_dimensions(svg: Path) -> Optional[Tuple[int, int]]:
    if not svg.is_file():
        return None
    try:
        # SVGs from PlantUML have viewBox near the top; read a bounded chunk
        with svg.open("r", encoding="utf-8", errors="ignore") as fh:
            head = fh.read(4096)
    except OSError:
        return None
    m = re.search(r'viewBox="([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"', head)
    if not m:
        return None
    try:
        w = int(float(m.group(3)))
        h = int(float(m.group(4)))
    except ValueError:
        return None
    if w <= 0 or h <= 0:
        return None
    return w, h


def get_png_dimensions(png: Path) -> Optional[Tuple[int, int]]:
    """Read width/height from PNG IHDR — no ImageMagick required."""
    if not png.is_file():
        return None
    try:
        with png.open("rb") as fh:
            header = fh.read(24)
        if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        # IHDR: bytes 16..24 are width (BE u32) + height (BE u32)
        w, h = struct.unpack(">II", header[16:24])
        if w <= 0 or h <= 0:
            return None
        return int(w), int(h)
    except (OSError, struct.error):
        return None


def get_dimensions(img: Path, fmt: str) -> Optional[Tuple[int, int]]:
    if fmt == "svg":
        return get_svg_dimensions(img)
    if fmt == "png":
        return get_png_dimensions(img)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Aspect Ratio Validation & Auto-Fix
# ─────────────────────────────────────────────────────────────────────────────
def check_aspect_ratio(
    img: Path, fmt: str, min_aspect: float, max_aspect: float
) -> Tuple[Optional[str], Optional[Tuple[int, int]]]:
    """Return (problem, (w, h)) where problem ∈ {'ok', 'too_tall', 'too_wide', None}.

    None means dimensions could not be determined.
    """
    dims = get_dimensions(img, fmt)
    if dims is None:
        return None, None
    w, h = dims
    ratio = w / h
    log(
        f"  📐 Dimensions: {w}x{h}, width/height ratio: {ratio:.2f} "
        f"(target {min_aspect}–{max_aspect})"
    )
    if ratio < min_aspect:
        log(f"  ⚠ Aspect ratio {ratio:.2f} is below minimum {min_aspect} — diagram is too tall")
        return "too_tall", dims
    if ratio > max_aspect:
        log(f"  ⚠ Aspect ratio {ratio:.2f} exceeds maximum {max_aspect} — diagram is too wide")
        return "too_wide", dims
    return "ok", dims


def guess_diagram_type(text: str) -> str:
    if re.search(r"(?m)^\s*(start|stop)\s*$", text) or re.search(r"(?m)^\s*:[^;]+;", text):
        return "activity"
    if re.search(r"(?m)^\s*state\s+", text):
        return "state"
    if re.search(r"(?m)^\s*participant\s+", text):
        return "sequence"
    return "other"


def fix_puml_aspect_ratio(puml: Path, problem: str) -> Optional[Path]:
    """Inject spacing guards + direction directive; return new puml path.

    Returns None if already fixed or unable to fix.
    """
    elog(f"  → Attempting to fix aspect ratio ({problem})...")
    text = puml.read_text(encoding="utf-8", errors="replace")

    if "!pragma aspectRatioFixed" in text:
        elog("  → Already auto-fixed; skipping further attempts")
        return None

    # Inject pragma + spacing guards right after @startuml
    injection = "\n!pragma aspectRatioFixed\n" + SPACING_GUARD_BLOCK
    text = re.sub(r"^@startuml", "@startuml" + injection, text, count=1, flags=re.MULTILINE)
    elog("  → Applied: spacing guards (CSS padding/wrapWidth/MinimumWidth + skinparam NodeSep/RankSep)")

    diagram_type = guess_diagram_type(text)
    direction_safe = diagram_type not in ("activity", "sequence", "state")

    if direction_safe:
        if problem == "too_tall":
            text = re.sub(r"(?m)^top to bottom direction\s*\r?\n", "", text)
            if "left to right direction" not in text:
                text = _insert_before_enduml(text, "left to right direction")
                elog("  → Applied: left to right direction")
        else:  # too_wide
            text = re.sub(r"(?m)^left to right direction\s*\r?\n", "", text)
            if "top to bottom direction" not in text:
                text = _insert_before_enduml(text, "top to bottom direction")
                elog("  → Applied: top to bottom direction")
    else:
        elog(f"  → Direction change skipped for {diagram_type} diagram; using spacing guards only")

    fixed = puml.with_suffix(puml.suffix + ".fixed.puml")
    # Rename to match previous naming convention: strip .puml then add .fixed.puml
    if puml.suffix == ".puml":
        fixed = puml.with_name(puml.stem + ".fixed.puml")
    fixed.write_text(text, encoding="utf-8")
    return fixed


def _insert_before_enduml(text: str, line: str) -> str:
    if re.search(r"(?m)^@enduml", text):
        return re.sub(r"(?m)^@enduml", line + "\n@enduml", text, count=1)
    return text.rstrip() + "\n" + line + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# A4 Paper Fit Validation & Auto-Scale
# ─────────────────────────────────────────────────────────────────────────────
def check_a4_fit(img: Path, fmt: str) -> Tuple[Optional[bool], float]:
    """Return (fits, required_scale).

    fits=True  → already fits A4 portrait or landscape.
    fits=False → does not fit; required_scale is what to inject.
    fits=None  → could not determine dimensions.
    """
    dims = get_dimensions(img, fmt)
    if dims is None:
        return None, 1.0
    w, h = dims

    fits_portrait = w <= A4_PORTRAIT_W and h <= A4_PORTRAIT_H
    fits_landscape = w <= A4_LANDSCAPE_W and h <= A4_LANDSCAPE_H

    if fits_portrait or fits_landscape:
        log(
            f"  📄 A4 fit: {w}x{h}px fits A4 portrait ({A4_PORTRAIT_W}x{A4_PORTRAIT_H}) "
            f"or landscape ({A4_LANDSCAPE_W}x{A4_LANDSCAPE_H}) ✓"
        )
        return True, 1.0

    sp = min(A4_PORTRAIT_W / w, A4_PORTRAIT_H / h)
    sl = min(A4_LANDSCAPE_W / w, A4_LANDSCAPE_H / h)
    factor = max(sp, sl)
    factor = max(factor, 0.15)
    factor = round(factor, 3)

    log(
        f"  📄 A4 fit: {w}x{h}px exceeds A4 portrait ({A4_PORTRAIT_W}x{A4_PORTRAIT_H}) "
        f"and landscape ({A4_LANDSCAPE_W}x{A4_LANDSCAPE_H})"
    )
    log(
        f"     Required scale to fit: {factor} "
        f"(portrait factor {sp:.3f}, landscape factor {sl:.3f})"
    )
    return False, factor


def fix_puml_a4_fit(puml: Path, factor: float, min_font_pt: float) -> Optional[Path]:
    if factor == 1.0:
        return None
    text = puml.read_text(encoding="utf-8", errors="replace")
    if "!pragma a4FitFixed" in text:
        return None

    text = re.sub(r"^@startuml", "@startuml\n!pragma a4FitFixed", text, count=1, flags=re.MULTILINE)
    # PlantUML supports only one scale directive; drop any existing one first
    text = re.sub(r"(?m)^\s*scale\s+[\d.]+\s*\r?\n", "", text)
    text = text.replace(
        "!pragma a4FitFixed",
        f"!pragma a4FitFixed\nscale {factor}",
        1,
    )

    elog(f"  → Applied: scale {factor} (A4 fit)")

    effective_pt = round(factor * DEFAULT_FONT_PX * 0.75, 1)
    if effective_pt < min_font_pt:
        elog(f"  ⚠ After scaling to {factor}, estimated font ≈ {effective_pt}pt on A4")
        elog(f"    That is below --min-font-pt {min_font_pt} and may be hard to read in print.")
        elog("    Consider splitting into multiple diagrams or abbreviating labels.")
    else:
        elog(f"     Estimated font ≈ {effective_pt}pt on A4 (≥ min {min_font_pt}pt) ✓")

    fixed = puml.with_name(puml.stem + ".a4fixed.puml")
    fixed.write_text(text, encoding="utf-8")
    return fixed


# ─────────────────────────────────────────────────────────────────────────────
# Post-processing (SVG bare strokes / dark-mode)
# ─────────────────────────────────────────────────────────────────────────────
def _inject_after_svg_tag(content: str, block: str) -> str:
    return re.sub(r"(<svg[^>]*>)", r"\1\n" + block.replace("\\", r"\\"), content, count=1)


def postprocess_svg_bare_strokes(svg: Path) -> None:
    try:
        content = svg.read_text(encoding="utf-8", errors="replace")
        content = _inject_after_svg_tag(content, BARE_STROKE_CSS)
        svg.write_text(content, encoding="utf-8")
    except OSError:
        pass


def postprocess_dark_svg(light: Path, dark: Path) -> bool:
    try:
        content = light.read_text(encoding="utf-8", errors="replace")
        content = _inject_after_svg_tag(content, DARK_MODE_CSS)
        dark.write_text(content, encoding="utf-8")
        return True
    except OSError:
        return False


def postprocess_dark_png(light: Path, dark: Path) -> bool:
    convert = which("convert") or which("magick")
    if not convert:
        return False
    # ImageMagick 7 exposes both `magick` and legacy `convert`; use whichever is present.
    if Path(convert).name.lower().startswith("magick") and not Path(convert).name.lower().startswith("convert"):
        base_cmd = [convert, "convert"]
    else:
        base_cmd = [convert]
    args = [
        str(light),
        "-fuzz", "25%", "-fill", "#1A1A1A", "-opaque", "#FFFFFF",
        "-fuzz", "25%", "-fill", "#2D2D2D", "-opaque", "#FAFAFA",
        "-fuzz", "25%", "-fill", "#2D2D2D", "-opaque", "#F1F1F1",
        "-fuzz", "25%", "-fill", "#2D2D2D", "-opaque", "#F2F2F2",
        "-fuzz", "25%", "-fill", "#C0C0C0", "-opaque", "#222222",
        "-fuzz", "25%", "-fill", "#C0C0C0", "-opaque", "#181818",
        "-fuzz", "25%", "-fill", "#E8E8E8", "-opaque", "#000000",
        str(dark),
    ]
    try:
        subprocess.run(base_cmd + args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return dark.is_file()
    except (OSError, subprocess.CalledProcessError):
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Rendering Backends
# ─────────────────────────────────────────────────────────────────────────────
def _docker_mount_path(p: Path) -> str:
    """Return the string Docker expects for `-v <host>:/data` on the current OS."""
    s = str(p.resolve())
    # On Windows, Docker Desktop accepts both `C:\Users\...` and `/c/Users/...`;
    # Docker for Windows CLI also accepts native Windows paths. Passing the
    # native path avoids MSYS path translation surprises.
    return s


def _iter_output_candidate(dir_: Path, exts: Tuple[str, ...], exclude_name: str) -> Optional[Path]:
    for ext in exts:
        for cand in dir_.glob(f"*.{ext}"):
            if cand.name == exclude_name:
                continue
            return cand
    return None


def convert_via_docker(
    src: Path, output_file: Path, fmt: str, cjk: bool
) -> bool:
    if not which("docker"):
        log("  → Docker not available, skipping")
        return False

    log("  → Trying Docker (plantuml/plantuml)...")
    ext = "utxt" if fmt == "txt" else fmt

    tmpdir = Path(tempfile.gettempdir()) / f"plantuml_docker_{uuid.uuid4().hex}"
    tmpdir.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(src, tmpdir / src.name)
        mount = _docker_mount_path(tmpdir)

        env = os.environ.copy()
        env.setdefault("MSYS_NO_PATHCONV", "1")

        base = ["docker", "run", "--rm", "-v", f"{mount}:/data"]

        if cjk:
            font_dirs = []
            for fd in (
                "/usr/share/fonts",
                "/usr/local/share/fonts",
                "/System/Library/Fonts",
            ):
                if Path(fd).is_dir():
                    font_dirs.append((fd, fd))
            # Windows fonts
            windir = os.environ.get("WINDIR") or os.environ.get("SystemRoot")
            for host in (
                f"{windir}\\Fonts" if windir else None,
                "C:\\Windows\\Fonts",
                "/c/Windows/Fonts",
                "/mnt/c/Windows/Fonts",
            ):
                if host and Path(host).is_dir() and not any(h == host for h, _ in font_dirs):
                    font_dirs.append((host, "/Windows/Fonts"))

            if font_dirs:
                for host, guest in font_dirs:
                    base += ["-v", f"{host}:{guest}:ro"]
                cmd = base + [
                    "--entrypoint", "sh",
                    "plantuml/plantuml:latest",
                    "-c", f"fc-cache -f 2>/dev/null; plantuml -t{ext} /data/{src.name}",
                ]
                log("  → CJK mode: mounting host fonts and refreshing font cache")
                try:
                    r = subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if r.returncode == 0:
                        gen = _iter_output_candidate(tmpdir, (ext, fmt), src.name)
                        if gen:
                            shutil.move(str(gen), str(output_file))
                            log("  ✓ Success (Docker + CJK)")
                            return True
                except OSError:
                    pass
            else:
                log("  ⚠ CJK mode: no host font directories found. CJK characters may not render correctly.")
                log("    Install CJK fonts on your system (e.g. 'apt install fonts-wqy-zenhei').")

        cmd = base + ["plantuml/plantuml:latest", f"-t{ext}", f"/data/{src.name}"]
        try:
            r = subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if r.returncode == 0:
                gen = _iter_output_candidate(tmpdir, (ext, fmt), src.name)
                if gen:
                    shutil.move(str(gen), str(output_file))
                    log("  ✓ Success (Docker)")
                    return True
        except OSError:
            pass
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    log("  ✗ Docker conversion failed")
    return False


def _find_local_jar() -> Optional[Path]:
    candidates = [
        "/usr/local/bin/plantuml.jar",
        "/usr/share/plantuml/plantuml.jar",
        os.path.expanduser("~/plantuml.jar"),
        os.path.join(os.environ.get("USERPROFILE", ""), "plantuml.jar") if os.environ.get("USERPROFILE") else "",
        os.path.join(os.environ.get("PROGRAMFILES", ""), "PlantUML", "plantuml.jar") if os.environ.get("PROGRAMFILES") else "",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "PlantUML", "plantuml.jar") if os.environ.get("LOCALAPPDATA") else "",
        "./plantuml.jar",
    ]
    for c in candidates:
        if c and Path(c).is_file():
            return Path(c)
    return None


def convert_via_local(src: Path, output_file: Path, fmt: str) -> bool:
    jar = _find_local_jar()
    if not jar:
        log("  → No local plantuml.jar found, skipping")
        return False
    if not which("java"):
        log("  → Java not available, skipping local JAR")
        return False

    log(f"  → Trying local JAR ({jar})...")
    ext = "utxt" if fmt == "txt" else fmt

    tmpdir = Path(tempfile.gettempdir()) / f"plantuml_local_{uuid.uuid4().hex}"
    tmpdir.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(src, tmpdir / src.name)
        try:
            r = subprocess.run(
                ["java", "-jar", str(jar), f"-t{ext}", "-o", str(tmpdir), str(tmpdir / src.name)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            return False
        if r.returncode == 0:
            gen = _iter_output_candidate(tmpdir, (ext, fmt), src.name)
            if gen:
                shutil.move(str(gen), str(output_file))
                log("  ✓ Success (local JAR)")
                return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    log("  ✗ Local JAR failed")
    return False


def convert_via_server(
    src: Path, output_file: Path, fmt: str, use_public_server: bool
) -> bool:
    if not use_public_server:
        log("  → Public server disabled (privacy default). Pass --use-public-server to enable.")
        return False

    server_host = (os.environ.get("PLANTUML_PUBLIC_SERVER") or "https://kroki.io").rstrip("/")
    server_url = f"{server_host}/plantuml/{fmt}"
    host_label = re.sub(r"^https?://", "", server_host).split("/", 1)[0]

    log("")
    log(f"  ⚠  PRIVACY WARNING: about to upload diagram source to {server_url}")
    log(f"     The full contents of '{src}' will be transmitted to {host_label}.")
    if server_host == "https://kroki.io":
        log("     kroki.io is operated by Yuzu Tech (EU). Kroki is open source and")
        log("     self-hostable — set PLANTUML_PUBLIC_SERVER=<your-url> to use your own.")
    else:
        log("     (Custom backend selected via PLANTUML_PUBLIC_SERVER.)")
    log("     Do NOT use this backend for confidential architecture, credentials,")
    log("     customer data, or proprietary business logic.")
    log("")
    log("  → Trying public server (opt-in via --use-public-server)...")

    try:
        body = src.read_bytes()
        req = urllib.request.Request(
            server_url,
            data=body,
            method="POST",
            headers={"Content-Type": "text/plain"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = resp.read()
        output_file.write_bytes(payload)
    except (urllib.error.URLError, OSError, TimeoutError):
        log("  ✗ Public server failed — check network or try Docker/local JAR backend")
        return False

    ok = False
    if fmt == "svg":
        try:
            head = output_file.read_text(encoding="utf-8", errors="ignore")[:2048]
            ok = "<svg" in head
        except OSError:
            ok = False
    elif fmt == "txt":
        ok = output_file.stat().st_size > 0
    elif fmt == "png":
        ok = get_png_dimensions(output_file) is not None
    elif fmt == "pdf":
        try:
            with output_file.open("rb") as fh:
                ok = fh.read(4) == b"%PDF"
        except OSError:
            ok = False

    if ok:
        log("  ✓ Success (public server)")
        return True
    log("  ✗ Public server failed — check network or try Docker/local JAR backend")
    return False


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="generate_plantuml.py",
        description="Convert PlantUML source to SVG/PNG/PDF/TXT.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Backend priority (local-first):\n"
            "  1. Docker (plantuml/plantuml)   — preferred, fully local\n"
            "  2. Local plantuml.jar           — offline fallback (Java required)\n"
            "  3. Kroki public server          — OPT-IN ONLY via --use-public-server"
        ),
    )
    p.add_argument("input", help="Path to the .puml source file")
    p.add_argument("output_dir", nargs="?", default="./output", help="Output directory (default: ./output)")
    p.add_argument("--format", choices=("svg", "png", "pdf", "txt"), default="svg", help="Output format (default: svg)")
    p.add_argument("--cjk", action="store_true", help="Enable CJK font support")
    p.add_argument("--no-fix", action="store_true", help="Disable automatic aspect ratio correction")
    p.add_argument("--min-aspect", type=float, default=0.7, help="Min width/height ratio (default: 0.7)")
    p.add_argument("--max-aspect", type=float, default=1.4, help="Max width/height ratio (default: 1.4)")
    p.add_argument("--dark-mode", action="store_true", help="Also emit <basename>.dark.<fmt>")
    p.add_argument("--no-a4-check", action="store_true", help="Disable automatic A4 fit validation")
    p.add_argument("--min-font-pt", type=float, default=8.0, help="Min legible font size on A4 in pt (default: 8.0)")
    p.add_argument("--use-public-server", action="store_true", help="OPT-IN: render via Kroki public server")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        elog(f"ERROR: Input file not found: {input_path}")
        return 1

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    base = input_path.stem
    for legacy in (".plantuml", ".txt"):
        if base.endswith(legacy):
            base = base[: -len(legacy)]
    fmt = args.format
    output_file = output_dir / f"{base}.{fmt}"

    log(f"🖼️  Converting {input_path} → {output_file} (format: {fmt})")

    # ── CJK auto-detection notice ────────────────────────────────────────────
    cjk = args.cjk
    if not cjk and detect_cjk(input_path):
        log("")
        log("🔤 CJK (Chinese/Japanese/Korean) characters detected in input.")
        log("   These may not render correctly without CJK font support.")
        log("   Re-run with --cjk to enable CJK rendering, or install CJK fonts.")
        log("   Attempting to proceed anyway...")
        log("")

    # ── Prepare working copy ─────────────────────────────────────────────────
    tmpdir = Path(tempfile.gettempdir())
    work_copy = tmpdir / f"plantuml_src_{uuid.uuid4().hex}.puml"
    shutil.copy2(input_path, work_copy)
    sanitize_puml_source(work_copy)

    cjk_copy: Optional[Path] = None
    if cjk:
        log("🔤 CJK mode enabled: configuring CJK-compatible fonts")
        cjk_copy = prepare_puml_for_cjk(work_copy)
        try:
            work_copy.unlink()
        except OSError:
            pass
        work_copy = cjk_copy
        sanitize_puml_source(work_copy)

    render_ok = False
    fix_attempt = 0
    aspect_done = False
    a4_tried = False
    last_ok_src = work_copy

    try:
        while fix_attempt <= MAX_FIX_ATTEMPTS:
            attempt_ok = (
                convert_via_docker(work_copy, output_file, fmt, cjk)
                or convert_via_local(work_copy, output_file, fmt)
                or convert_via_server(work_copy, output_file, fmt, args.use_public_server)
            )
            if not attempt_ok:
                if render_ok and output_file.is_file():
                    log("  ⚠ Re-render failed; keeping the last successful output")
                    break
                log("")
                log("❌ All conversion methods failed.")
                log("   Install options (local, recommended for privacy):")
                log("   1. Docker: docker pull plantuml/plantuml:latest")
                log("   2. Java + JAR: download plantuml.jar from https://plantuml.com/download")
                log("   Or, to use the public Kroki server (uploads diagram to kroki.io):")
                log("   3. Re-run with --use-public-server (review the privacy notice first)")
                log("      Override the host with PLANTUML_PUBLIC_SERVER=<url> if self-hosting")
                return 1
            render_ok = True
            last_ok_src = work_copy

            if fmt in ("txt", "pdf"):
                break

            if not args.no_fix and not aspect_done:
                problem, _ = check_aspect_ratio(output_file, fmt, args.min_aspect, args.max_aspect)
                if problem is None:
                    log("  ⓘ Could not determine image dimensions; skipping aspect ratio check.")
                    aspect_done = True
                elif problem != "ok":
                    fix_attempt += 1
                    if fix_attempt > MAX_FIX_ATTEMPTS:
                        log(f"  ⚠ Maximum fix attempts ({MAX_FIX_ATTEMPTS}) reached. Manual adjustment may be needed.")
                        aspect_done = True
                    else:
                        fixed = fix_puml_aspect_ratio(work_copy, problem)
                        if not fixed:
                            log("  ✗ Auto-fix step failed; keeping current output.")
                            aspect_done = True
                        else:
                            if work_copy != input_path and work_copy.exists():
                                try:
                                    work_copy.unlink()
                                except OSError:
                                    pass
                            work_copy = fixed
                            log("  → Re-rendering with corrected layout...")
                            continue
                aspect_done = True

            if not args.no_a4_check and not a4_tried:
                fits, factor = check_a4_fit(output_file, fmt)
                if fits is None:
                    log("  ⓘ Could not determine image dimensions; skipping A4 check.")
                    break
                if not fits:
                    fix_attempt += 1
                    if fix_attempt > MAX_FIX_ATTEMPTS:
                        log(f"  ⚠ Maximum fix attempts ({MAX_FIX_ATTEMPTS}) reached; A4 fit may not hold.")
                        break
                    a4_fixed = fix_puml_a4_fit(work_copy, factor, args.min_font_pt)
                    if not a4_fixed:
                        log("  ✗ A4 auto-fit failed; using current diagram.")
                        a4_tried = True
                        break
                    if work_copy != input_path and work_copy.exists():
                        try:
                            work_copy.unlink()
                        except OSError:
                            pass
                    work_copy = a4_fixed
                    a4_tried = True
                    log("  → Re-rendering with A4-fit scale...")
                    continue

            break

        # ── Fix bare strokes in light SVG ────────────────────────────────────
        if render_ok and fmt == "svg":
            postprocess_svg_bare_strokes(output_file)

        # ── Dark-mode companion ──────────────────────────────────────────────
        dark_output: Optional[Path] = None
        if args.dark_mode and render_ok:
            dark_output = output_dir / f"{base}.dark.{fmt}"
            log("")
            log(f"🌙 Dark-mode variant requested: {dark_output}")
            if fmt == "svg":
                if postprocess_dark_svg(output_file, dark_output):
                    log("  ✓ Dark-mode SVG generated")
                else:
                    dark_output = None
            elif fmt == "png":
                if postprocess_dark_png(output_file, dark_output):
                    log("  ✓ Dark-mode PNG generated")
                else:
                    log("  ⚠ Dark-mode PNG requires ImageMagick (convert); dark variant skipped")
                    dark_output = None
            else:
                log("  ⚠ Dark-mode is only supported for svg and png output; skipping")
                dark_output = None

        # ── Report ───────────────────────────────────────────────────────────
        if render_ok:
            log("")
            log(f"✅ Output: {output_file}")
            print(str(output_file))
            if dark_output and dark_output.is_file():
                log(f"🌙 Dark: {dark_output}")
                print(str(dark_output))
            return 0
        return 1
    finally:
        # ── Cleanup temp files ───────────────────────────────────────────────
        for p in (work_copy, cjk_copy, last_ok_src):
            if p and p != input_path and Path(p).exists():
                try:
                    Path(p).unlink()
                except OSError:
                    pass


if __name__ == "__main__":
    sys.exit(main())