#!/usr/bin/env python3
"""依赖版本重复 / 冲突检查 —— 扫描 package.json 与 pubspec.yaml 的依赖声明。

纯标准库（json / re / argparse），不联网、不修改被检文件，产出确定可复现。
用于发现：同一包在 dependencies 与 devDependencies 重复声明、跨多包管理器文件的
版本约束冲突（monorepo 常见）。pubspec.yaml 用轻量行解析（stdlib 无 YAML 解析器），
仅支持单行的 `name: version` 依赖写法，复杂多行写法可能漏判（已在限制中说明）。

检测项：
  E1  package.json 中同一包同时出现在 dependencies 与 devDependencies
  E2  多个 package.json 中同一包版本约束不一致（冲突）
  E3  pubspec.yaml 中同一包同时出现在 dependencies 与 dev_dependencies
  E4  多个 pubspec.yaml 中同一包版本约束不一致（冲突）

用法:
  python3 scripts/check_dep_dupes.py --package-json package.json
  python3 scripts/check_dep_dupes.py --package-json app/package.json libs/foo/package.json
  python3 scripts/check_dep_dupes.py --pubspec pubspec.yaml
  python3 scripts/check_dep_dupes.py --package-json . --pubspec .   # 目录递归扫描
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "build", ".dart_tool", "Pods", "vendor"}


def expand_paths(paths, filename):
    """路径若是目录则递归收集该文件名（跳过依赖/构建目录）。"""
    out = []
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            for root, dirs, files in os.walk(pp):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                if filename in files:
                    out.append(Path(root) / filename)
        elif pp.is_file():
            out.append(pp)
    return out


def parse_npm(path: Path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    deps = dict(data.get("dependencies", {}))
    dev = dict(data.get("devDependencies", {}))
    return deps, dev


def parse_pubspec(path: Path):
    """轻量行解析：仅识别单行的 `name: version`。返回 (deps, dev_deps)。"""
    deps, dev = {}, {}
    in_deps = in_dev = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line == "dependencies:":
                in_deps, in_dev = True, False
                continue
            if line == "dev_dependencies:":
                in_dev, in_deps = True, False
                continue
            if line.endswith(":") and line != "dependencies:" and line != "dev_dependencies:":
                in_deps = in_dev = False
                continue
            if (in_deps or in_dev) and ":" in line:
                name, _, ver = line.partition(":")
                name, ver = name.strip(), ver.strip()
                if not name or name.startswith("#"):
                    continue
                # 多行值（值为空，下一行才是内容）跳过，避免误判为包名
                if ver == "":
                    continue
                if in_dev:
                    dev[name] = ver
                else:
                    deps[name] = ver
    return deps, dev


def main() -> int:
    ap = argparse.ArgumentParser(description="检查 npm / pubspec 依赖重复与版本冲突")
    ap.add_argument("--package-json", nargs="*", default=[], help="package.json 文件或目录")
    ap.add_argument("--pubspec", nargs="*", default=[], help="pubspec.yaml 文件或目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if not args.package_json and not args.pubspec:
        ap.error("至少需要 --package-json 或 --pubspec 之一")

    findings = []

    # ── npm ──────────────────────────────────────────────
    npm_files = expand_paths(args.package_json, "package.json")
    all_npm = {}
    for f in npm_files:
        try:
            deps, dev = parse_npm(f)
        except (json.JSONDecodeError, OSError) as e:
            findings.append({"severity": "error", "check": "npm 解析",
                             "detail": f"{f}: {e}"})
            continue
        # E1: 同文件重复
        for name in set(deps) & set(dev):
            findings.append({"severity": "error", "check": "npm 重复声明",
                             "detail": f"{f}: {name} 同时出现在 dependencies 与 devDependencies"})
        for name, ver in {**deps, **dev}.items():
            all_npm.setdefault(name, []).append((str(f), ver))
    # E2: 跨文件冲突
    for name, occ in all_npm.items():
        vers = {v for _, v in occ}
        if len(vers) > 1:
            where = "; ".join(f"{p}={v}" for p, v in occ)
            findings.append({"severity": "error", "check": "npm 版本冲突",
                             "detail": f"{name} 版本约束不一致: {where}"})

    # ── pubspec ──────────────────────────────────────────
    pub_files = expand_paths(args.pubspec, "pubspec.yaml")
    all_pub = {}
    for f in pub_files:
        try:
            deps, dev = parse_pubspec(f)
        except OSError as e:
            findings.append({"severity": "error", "check": "pubspec 解析",
                             "detail": f"{f}: {e}"})
            continue
        for name in set(deps) & set(dev):
            findings.append({"severity": "error", "check": "pubspec 重复声明",
                             "detail": f"{f}: {name} 同时出现在 dependencies 与 dev_dependencies"})
        for name, ver in {**deps, **dev}.items():
            all_pub.setdefault(name, []).append((str(f), ver))
    for name, occ in all_pub.items():
        vers = {v for _, v in occ}
        if len(vers) > 1:
            where = "; ".join(f"{p}={v}" for p, v in occ)
            findings.append({"severity": "error", "check": "pubspec 版本冲突",
                             "detail": f"{name} 版本约束不一致: {where}"})

    errors = [f for f in findings if f["severity"] == "error"]
    if args.json:
        print(json.dumps({"errors": len(errors), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        for f in findings:
            mark = "✗" if f["severity"] == "error" else "!"
            print(f"  [{mark}] {f['check']}: {f['detail']}")
        print(f"\n结果：{len(errors)} error")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
