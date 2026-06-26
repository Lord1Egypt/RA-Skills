#!/usr/bin/env python3
"""Inspect repository files and identify likely data processing code."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

KEYWORDS = [
    "dataset", "dataloader", "data_loader", "datamodule", "preprocess", "prepare",
    "process", "processing", "transform", "augment", "crop", "resize", "split",
    "annotation", "label", "metadata", "extract", "feature", "frames", "tokenize",
    "download", "convert", "benchmark", "loader", "sampler",
]
CODE_EXTS = {".py", ".ipynb", ".sh", ".cmd", ".ps1", ".yaml", ".yml", ".json", ".txt", ".md"}
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "dist", "build"}
DEF_RE = re.compile(r"^\s*(class|def)\s+([A-Za-z_][A-Za-z0-9_]*)")
SECTION_RE = re.compile(r"^#{1,4}\s+(.+)")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_text(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except Exception:
        return ""


def score_path(path: Path, text: str) -> tuple[int, list[str]]:
    lower_path = str(path).lower().replace("\\", "/")
    lower_text = text.lower()
    score = 0
    reasons: list[str] = []
    for kw in KEYWORDS:
        if kw in lower_path:
            score += 5
            reasons.append(f"路径包含 {kw}")
        count = lower_text.count(kw)
        if count:
            score += min(count, 5)
    if "torch.utils.data" in lower_text:
        score += 12
        reasons.append("包含 torch.utils.data")
    if "class " in text and "dataset" in lower_text:
        score += 8
        reasons.append("可能定义 Dataset 类")
    if "if __name__" in lower_text and any(k in lower_text for k in ["preprocess", "prepare", "dataset", "data"]):
        score += 5
        reasons.append("可能是可执行数据处理脚本")
    return score, reasons


def extract_symbols(text: str, limit: int = 20) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        m = DEF_RE.match(line)
        if m:
            out.append(f"{m.group(1)} {m.group(2)}")
        if len(out) >= limit:
            break
    return out


def extract_readme_sections(path: Path, text: str) -> list[str]:
    lines = text.splitlines()
    sections: list[str] = []
    capture = False
    buf: list[str] = []
    title = ""
    for line in lines:
        m = SECTION_RE.match(line)
        if m:
            if capture and buf:
                sections.append(title + "\n" + "\n".join(buf[:20]))
            title = line
            capture = any(k in m.group(1).lower() for k in ["data", "dataset", "preprocess", "prepare", "download", "training", "benchmark"])
            buf = []
        elif capture:
            buf.append(line)
    if capture and buf:
        sections.append(title + "\n" + "\n".join(buf[:20]))
    return sections[:6]


def main() -> int:
    parser = argparse.ArgumentParser(description="Locate data processing code in a repository")
    parser.add_argument("repo_path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_path)
    if not root.exists():
        print(f"错误：路径不存在：{root}")
        return 2

    candidates = []
    readme_sections = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in CODE_EXTS:
            continue
        text = read_text(path)
        score, reasons = score_path(path, text)
        if path.name.lower().startswith("readme"):
            readme_sections.extend({"file": rel(path, root), "section": s} for s in extract_readme_sections(path, text))
        if score >= 6:
            candidates.append({
                "path": rel(path, root),
                "score": score,
                "reasons": reasons[:8],
                "symbols": extract_symbols(text),
            })
    candidates.sort(key=lambda x: x["score"], reverse=True)
    payload = {"script": "inspect_repo_data_processing.py", "repo_path": str(root), "candidates": candidates[:50], "readme_sections": readme_sections[:10]}

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("=== 执行脚本 ===")
        print("脚本：inspect_repo_data_processing.py")
        print(f"仓库路径：{root}")
        print("\n=== 数据处理代码候选 ===")
        if not candidates:
            print("未定位到明显数据处理代码候选。")
        for item in candidates[:30]:
            print(f"score={item['score']} file={item['path']}")
            for r in item["reasons"]:
                print(f"  - {r}")
            if item["symbols"]:
                print(f"  symbols: {', '.join(item['symbols'][:12])}")
        print("\n=== README 数据相关章节候选 ===")
        if not readme_sections:
            print("未定位到 README 数据相关章节。")
        for sec in readme_sections[:6]:
            print(f"--- {sec['file']} ---")
            print(sec["section"][:1200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
