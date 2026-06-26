#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import zipfile
from pathlib import Path


def unzip(zip_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(out_dir)
    children = [p for p in out_dir.iterdir()]
    if len(children) == 1 and children[0].is_dir():
        return children[0]
    return out_dir


def clone_repo(repo_url: str, out_dir: Path) -> Path:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", repo_url, str(out_dir)], check=True)
    return out_dir


def find_modules(root: Path) -> list[str]:
    modules = []
    for p in root.rglob("pom.xml"):
        modules.append(str(p.parent.relative_to(root)) if p.parent != root else ".")
    return sorted(set(modules))


def project_name(root: Path) -> str:
    return root.name or "java-maven-project"


def limited_reason(mode: str, modules: list[str]) -> str:
    if modules:
        return ""
    if mode == "zip":
        return "未识别到 pom.xml，可能 ZIP 不是完整 Maven 项目、解压层级异常，或源码缺失。"
    return "未识别到 pom.xml，可能仓库不是 Maven 项目、拉取内容不完整，或目录层级异常。"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["zip", "git"], required=True)
    ap.add_argument("--input", required=True, help="zip path or git repo url")
    ap.add_argument("--work", required=True, help="working directory under temp")
    ap.add_argument("--json", required=True, help="output json summary")
    args = ap.parse_args()

    work = Path(args.work).resolve()
    json_path = Path(args.json).resolve()

    try:
        if args.mode == "zip":
            root = unzip(Path(args.input).resolve(), work)
        else:
            root = clone_repo(args.input, work)
        modules = find_modules(root)
        summary = {
            "ok": True,
            "mode": args.mode,
            "input": args.input,
            "root": str(root),
            "projectName": project_name(root),
            "modules": modules,
            "moduleCount": len(modules),
            "scanLimited": len(modules) == 0,
            "limitedReason": limited_reason(args.mode, modules),
        }
    except Exception as e:
        summary = {
            "ok": False,
            "mode": args.mode,
            "input": args.input,
            "root": "",
            "projectName": "java-maven-project",
            "modules": [],
            "moduleCount": 0,
            "scanLimited": True,
            "limitedReason": f"项目输入处理失败：{e}",
            "error": str(e),
        }

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
