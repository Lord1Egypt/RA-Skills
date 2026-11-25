#!/usr/bin/env python3
"""按示例帧及交互文案重做 Noto Serif SC 与 Latin Modern 的 WOFF2 子集。"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("template", "origami-ellipse", "vector-p-norm")
PUNCTUATION = set("，。、；：？！“”‘’（）《》〈〉…—·　∞±×÷≤≥−∑√∈∉²¹′″₁₂")


def visible_chars(files: list[Path]) -> set[str]:
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    text = re.sub(r"<svg\b[\s\S]*?</svg>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return set(text) | PUNCTUATION


def subset_font(source: Path, output: Path, chars: set[str], weight: int | None = None) -> None:
    font = TTFont(source)
    if weight is not None and "fvar" in font:
        font = instantiateVariableFont(font, {"wght": weight}, inplace=False)
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    sub = subset.Subsetter(options=options)
    sub.populate(unicodes={ord(char) for char in chars})
    sub.subset(font)
    output.parent.mkdir(parents=True, exist_ok=True)
    font.flavor = "woff2"
    font.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="给示例课件重做字体子集")
    parser.add_argument("--target", required=True, choices=TARGETS)
    parser.add_argument("--noto-font", type=Path, default=Path(os.getenv("LEVERMATH_NOTO_FONT", "C:/Windows/Fonts/NotoSerifSC-VF.ttf")))
    parser.add_argument("--latin-font", type=Path, default=Path(os.getenv("LEVERMATH_LATIN_FONT", "D:/texlive/2025/texmf-dist/fonts/opentype/public/lm/lmroman10-regular.otf")))
    args = parser.parse_args()
    if args.target == "template":
        project = ROOT
        source_files = sorted((ROOT / "templates/basic/frames").glob("*.html"))
        source_files += [ROOT / "src/main.ts", ROOT / "src/engine/deck.ts"]
        target = ROOT / "templates/basic/assets/fonts"
    else:
        project = ROOT / "examples" / args.target
        source_files = sorted(project.glob("frames/*.html")) + sorted(project.glob("interactive/*.ts"))
        source_files += [ROOT / "src/engine/deck.ts"]
        target = project / "assets/fonts"
    source_files = [path for path in source_files if path.exists()]
    if not source_files:
        parser.error("找不到课件源码")
    for source in (args.noto_font, args.latin_font):
        if not source.exists():
            parser.error(f"找不到字体源：{source}；请用 --noto-font 或 --latin-font 指定路径")
    chars = visible_chars(source_files)
    subset_font(args.noto_font, target / "notoserifsc-subset.woff2", chars, weight=400)
    if args.target == "vector-p-norm":
        subset_font(args.noto_font, target / "notoserifsc-bold-subset.woff2", chars, weight=700)
    subset_font(args.latin_font, target / "lmroman-subset.woff2", chars)
    print(f"{args.target}：扫描 {len(source_files)} 个文件，覆盖 {len(chars)} 个字符；字体已写到 {target}")


if __name__ == "__main__":
    main()
