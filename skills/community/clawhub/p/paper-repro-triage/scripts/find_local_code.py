#!/usr/bin/env python3
"""Find local source repositories before cloning or creating from-scratch implementations."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

INDICATORS = {
    "git": 8,
    "readme": 3,
    "requirements": 2,
    "pyproject": 2,
    "setup": 2,
    "train": 3,
    "eval": 2,
    "model": 2,
    "dataset": 2,
    "config": 2,
}


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", value.lower()).strip("-") or "paper"


def split_terms(value: str) -> list[str]:
    return [t for t in norm(value).split() if len(t) >= 2]


def run_origin(path: Path) -> str:
    if not (path / ".git").exists():
        return ""
    try:
        proc = subprocess.run(["git", "-C", str(path), "remote", "get-url", "origin"], text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10)
        return proc.stdout.strip() if proc.returncode == 0 else ""
    except Exception:
        return ""


def is_repo_like(path: Path) -> bool:
    if not path.is_dir():
        return False
    names = {p.name.lower() for p in path.iterdir() if p.exists()}
    if ".git" in names:
        return True
    if any(name.startswith("readme") for name in names):
        return True
    if any(name in names for name in ["requirements.txt", "pyproject.toml", "setup.py", "environment.yml", "environment.yaml"]):
        return True
    if any(name in names for name in ["src", "models", "model", "datasets", "data", "configs", "config"]):
        return True
    return False


def score_repo(path: Path, terms: list[str], repo_url: str = "") -> tuple[int, list[str], str]:
    score = 0
    reasons: list[str] = []
    name_norm = norm(path.name)
    for term in terms:
        if term in name_norm:
            score += 5
            reasons.append(f"目录名匹配：{term}")
    origin = run_origin(path)
    if repo_url and origin and origin.rstrip("/").lower() == repo_url.rstrip("/").lower():
        score += 30
        reasons.append("git origin 与目标 URL 一致")
    if (path / ".git").exists():
        score += INDICATORS["git"]
        reasons.append("包含 .git")
    for child in path.iterdir() if path.exists() else []:
        lower = child.name.lower()
        if lower.startswith("readme"):
            score += INDICATORS["readme"]
            reasons.append(f"包含 {child.name}")
        if lower.startswith("requirements") or lower.startswith("environment"):
            score += INDICATORS["requirements"]
            reasons.append(f"包含依赖文件 {child.name}")
        if lower == "pyproject.toml":
            score += INDICATORS["pyproject"]
            reasons.append("包含 pyproject.toml")
        if lower in {"src", "models", "model"}:
            score += INDICATORS["model"]
            reasons.append(f"包含模型/源码目录 {child.name}")
        if lower in {"datasets", "dataset", "data"}:
            score += INDICATORS["dataset"]
            reasons.append(f"包含数据目录 {child.name}")
        if lower in {"configs", "config"}:
            score += INDICATORS["config"]
            reasons.append(f"包含配置目录 {child.name}")
        if re.match(r"^(train|main|run|eval|test).*\.(py|ipynb|sh|cmd)$", lower):
            score += INDICATORS["train"]
            reasons.append(f"包含入口候选 {child.name}")
    return score, reasons, origin


def gather_roots(workspace: Path, paper_slug: str, extra_roots: list[str]) -> list[Path]:
    roots = [
        workspace / "paper-repro-workspace" / paper_slug / "main-code",
        workspace / "paper-repro-workspace" / paper_slug / "dataset-code",
        workspace / "paper-repro-workspace" / paper_slug / "local-code",
        workspace,
    ]
    env_roots = os.environ.get("PAPER_REPRO_LOCAL_CODE_ROOTS", "")
    for item in re.split(r"[;:]", env_roots):
        if item.strip():
            roots.append(Path(item.strip()))
    roots.extend(Path(r) for r in extra_roots)
    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        try:
            key = str(root.resolve())
        except Exception:
            key = str(root)
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def walk_candidates(root: Path, max_depth: int) -> list[Path]:
    out: list[Path] = []
    if not root.exists() or not root.is_dir():
        return out
    root = root.resolve()
    stack = [(root, 0)]
    while stack:
        path, depth = stack.pop()
        if path.name in {".git", "__pycache__", ".venv", "node_modules"}:
            continue
        if is_repo_like(path):
            out.append(path)
            if (path / ".git").exists() and path != root:
                continue
        if depth < max_depth:
            try:
                children = [p for p in path.iterdir() if p.is_dir()]
            except OSError:
                children = []
            stack.extend((child, depth + 1) for child in children)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Find local source code candidates")
    parser.add_argument("--name", action="append", default=[], help="paper, method, dataset, or repo name")
    parser.add_argument("--repo-url", default="")
    parser.add_argument("--paper-slug", default="paper")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--root", action="append", default=[])
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    paper_slug = safe_slug(args.paper_slug)
    terms: list[str] = []
    for name in args.name:
        terms.extend(split_terms(name))
    if args.repo_url:
        repo_tail = args.repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        terms.extend(split_terms(repo_tail))
    terms = sorted(set(terms))

    roots = gather_roots(Path(args.workspace), paper_slug, args.root)
    results = []
    seen: set[str] = set()
    for root in roots:
        for cand in walk_candidates(root, args.max_depth):
            key = str(cand.resolve())
            if key in seen:
                continue
            seen.add(key)
            score, reasons, origin = score_repo(cand, terms, args.repo_url)
            if score <= 0 and terms:
                continue
            results.append({
                "path": str(cand),
                "score": score,
                "origin": origin,
                "reasons": reasons,
            })
    results.sort(key=lambda r: r["score"], reverse=True)

    payload = {"script": "find_local_code.py", "terms": terms, "roots": [str(r) for r in roots], "results": results[:20]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("=== 执行脚本 ===")
        print("脚本：find_local_code.py")
        print(f"检索词：{', '.join(terms) if terms else '(无)'}")
        print("=== 本地源码候选 ===")
        if not results:
            print("未找到高相关本地源码候选。")
        for item in results[:20]:
            print(f"score={item['score']} path={item['path']}")
            if item["origin"]:
                print(f"  origin={item['origin']}")
            for reason in item["reasons"][:8]:
                print(f"  - {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
