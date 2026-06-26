#!/usr/bin/env python3
"""Build the reusable static reader for paper-code-joint-analysis outputs."""

from __future__ import annotations

import argparse
import shutil
import urllib.request
from pathlib import Path


REQUIRED_FILES = [
    "analysis_bundle.json",
    "paper_reading_report.md",
    "paper_questions_for_code.md",
    "paper_code_crosswalk.md",
    "experiment_joint_reading.md",
    "implementation_omissions.md",
    "diagrams.md",
    "modify_method_guide.md",
    "validation_report.md",
]

KATEX_FONT_BASE_URL = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/fonts"
KATEX_FONTS = [
    ("KaTeX_AMS", "normal", 400, "KaTeX_AMS-Regular"),
    ("KaTeX_Caligraphic", "normal", 700, "KaTeX_Caligraphic-Bold"),
    ("KaTeX_Caligraphic", "normal", 400, "KaTeX_Caligraphic-Regular"),
    ("KaTeX_Fraktur", "normal", 700, "KaTeX_Fraktur-Bold"),
    ("KaTeX_Fraktur", "normal", 400, "KaTeX_Fraktur-Regular"),
    ("KaTeX_Main", "normal", 700, "KaTeX_Main-Bold"),
    ("KaTeX_Main", "italic", 700, "KaTeX_Main-BoldItalic"),
    ("KaTeX_Main", "italic", 400, "KaTeX_Main-Italic"),
    ("KaTeX_Main", "normal", 400, "KaTeX_Main-Regular"),
    ("KaTeX_Math", "italic", 700, "KaTeX_Math-BoldItalic"),
    ("KaTeX_Math", "italic", 400, "KaTeX_Math-Italic"),
    ("KaTeX_SansSerif", "normal", 700, "KaTeX_SansSerif-Bold"),
    ("KaTeX_SansSerif", "italic", 400, "KaTeX_SansSerif-Italic"),
    ("KaTeX_SansSerif", "normal", 400, "KaTeX_SansSerif-Regular"),
    ("KaTeX_Script", "normal", 400, "KaTeX_Script-Regular"),
    ("KaTeX_Size1", "normal", 400, "KaTeX_Size1-Regular"),
    ("KaTeX_Size2", "normal", 400, "KaTeX_Size2-Regular"),
    ("KaTeX_Size3", "normal", 400, "KaTeX_Size3-Regular"),
    ("KaTeX_Size4", "normal", 400, "KaTeX_Size4-Regular"),
    ("KaTeX_Typewriter", "normal", 400, "KaTeX_Typewriter-Regular"),
]


def copytree_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def find_vendor(analysis_dir: Path, explicit: str | None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    candidates.extend([
        analysis_dir / "site" / "vendor",
        analysis_dir.parent / "site" / "vendor",
        analysis_dir.parent.parent / "site" / "vendor",
        Path.cwd() / "site" / "vendor",
    ])
    for candidate in candidates:
        if (candidate / "mermaid.min.js").exists() or (candidate / "katex" / "katex.min.js").exists():
            return candidate
    return None


def katex_font_face_css() -> str:
    rules = []
    for family, style, weight, stem in KATEX_FONTS:
        rules.append(
            f'@font-face{{font-family:"{family}";font-style:{style};font-weight:{weight};'
            f'src:url(fonts/{stem}.woff2) format("woff2")}}'
        )
    return "".join(rules)


def install_katex_fonts(katex_dir: Path, base_url: str) -> int:
    if not katex_dir.exists():
        raise FileNotFoundError(f"KaTeX directory not found: {katex_dir}")

    fonts_dir = katex_dir / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    base = base_url.rstrip("/")
    for _, _, _, stem in KATEX_FONTS:
        target = fonts_dir / f"{stem}.woff2"
        if target.exists() and target.stat().st_size > 0:
            continue
        request = urllib.request.Request(
            f"{base}/{target.name}",
            headers={"User-Agent": "paper-code-joint-analysis-reader-builder"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            target.write_bytes(response.read())
        downloaded += 1

    css_path = katex_dir / "katex.min.css"
    css = css_path.read_text(encoding="utf-8")
    if "@font-face" not in css:
        css_path.write_text(katex_font_face_css() + css, encoding="utf-8")
    return downloaded


def main() -> int:
    parser = argparse.ArgumentParser(description="Build static reader from analysis_bundle.json and Markdown artifacts.")
    parser.add_argument("analysis_dir", help="Directory containing analysis_bundle.json and companion Markdown files.")
    parser.add_argument("--out", default=None, help="Output site directory. Defaults to <analysis_dir>/site.")
    parser.add_argument("--vendor-source", default=None, help="Optional directory containing mermaid.min.js and/or katex/.")
    parser.add_argument(
        "--install-katex-fonts",
        action="store_true",
        help="Download KaTeX WOFF2 fonts into the generated site for full local formula typography.",
    )
    parser.add_argument(
        "--katex-font-base-url",
        default=KATEX_FONT_BASE_URL,
        help="Base URL for KaTeX WOFF2 font downloads. Defaults to the bundled KaTeX version.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing site directory.")
    args = parser.parse_args()

    analysis_dir = Path(args.analysis_dir).resolve()
    if not analysis_dir.exists():
        raise SystemExit(f"analysis_dir does not exist: {analysis_dir}")
    missing = [name for name in REQUIRED_FILES if not (analysis_dir / name).exists()]
    if missing:
        raise SystemExit("missing required analysis files: " + ", ".join(missing))

    skill_dir = Path(__file__).resolve().parents[1]
    template = skill_dir / "assets" / "reader-template"
    out_dir = Path(args.out).resolve() if args.out else analysis_dir / "site"
    if out_dir.exists() and args.force:
        shutil.rmtree(out_dir)
    elif out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"output directory exists and is not empty: {out_dir}; use --force")
    copytree_contents(template, out_dir)

    vendor = find_vendor(analysis_dir, args.vendor_source)
    if vendor:
        vendor_out = out_dir / "vendor"
        vendor_out.mkdir(parents=True, exist_ok=True)
        if vendor.resolve() != vendor_out.resolve():
            if (vendor / "mermaid.min.js").exists():
                shutil.copy2(vendor / "mermaid.min.js", vendor_out / "mermaid.min.js")
            if (vendor / "katex").exists():
                target = vendor_out / "katex"
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(vendor / "katex", target)

    installed_fonts = None
    if args.install_katex_fonts:
        try:
            installed_fonts = install_katex_fonts(out_dir / "vendor" / "katex", args.katex_font_base_url)
        except Exception as exc:
            raise SystemExit(f"failed to install KaTeX fonts: {exc}") from exc

    print(f"reader: {out_dir / 'index.html'}")
    if vendor:
        print(f"vendor: {vendor}")
    else:
        print("vendor: not found; reader will use formula/diagram fallbacks")
    if installed_fonts is not None:
        print(f"katex_fonts: installed {installed_fonts} new WOFF2 files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
