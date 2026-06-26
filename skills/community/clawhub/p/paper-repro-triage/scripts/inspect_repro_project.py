#!/usr/bin/env python3
"""Inspect a generated reproduction project without installing dependencies or training."""
from __future__ import annotations

import argparse
import py_compile
from pathlib import Path

REQUIRED = [
    "README.md",
    "repro-docs/repro-notes.md",
    "repro-docs/evidence-map.md",
    "repro-docs/paper-spec.yaml",
    "repro-docs/requirements.txt",
    "config.py",
    "main.py",
    "run.py",
    "data/__init__.py",
    "data/dataset.py",
    "data/preprocess.py",
    "models/__init__.py",
    "models/model.py",
    "engine/__init__.py",
    "engine/train.py",
    "engine/evaluate.py",
    "utils/__init__.py",
    "utils/common.py",
    "utils/metrics.py",
]

FORBIDDEN_DEFAULTS = [
    "configs/default.yaml",
    "configs/debug.yaml",
    "configs/ablation.yaml",
    "losses/paper_loss.py",
    "loss.py",
    "scripts/train.sh",
    "scripts/eval.sh",
    "scripts/train.cmd",
    "scripts/eval.cmd",
]


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect generated concise repro project")
    parser.add_argument("project_path")
    args = parser.parse_args()

    root = Path(args.project_path)
    print("=== 执行脚本 ===")
    print("脚本：inspect_repro_project.py")
    print(f"工程路径：{root}")

    if not root.exists():
        print("错误：工程路径不存在。")
        return 2

    print("\n=== 必需文件检查 ===")
    missing = []
    for rel in REQUIRED:
        path = root / rel
        if path.exists():
            print(f"OK {rel}")
        else:
            print(f"MISSING {rel}")
            missing.append(rel)

    print("\n=== 不应默认生成的旧结构检查 ===")
    forbidden_found = []
    for rel in FORBIDDEN_DEFAULTS:
        path = root / rel
        if path.exists():
            print(f"FOUND_OLD_STRUCTURE {rel}")
            forbidden_found.append(rel)
        else:
            print(f"OK_ABSENT {rel}")

    print("\n=== Python 静态编译检查 ===")
    compile_errors = []
    for path in sorted(root.rglob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
            print(f"OK {path.relative_to(root)}")
        except Exception as exc:
            print(f"FAIL {path.relative_to(root)}: {exc}")
            compile_errors.append(str(path.relative_to(root)))

    print("\n=== TODO / ASSUMPTION / NotImplementedError 统计 ===")
    markers = {"TODO": 0, "ASSUMPTION": 0, "NotImplementedError": 0}
    marker_files = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".py", ".md", ".yaml", ".yml", ".txt"}:
            text = read(path)
            counts = {k: text.count(k) for k in markers}
            if any(counts.values()):
                marker_files.append((str(path.relative_to(root)).replace("\\", "/"), counts))
                for k, v in counts.items():
                    markers[k] += v
    for k, v in markers.items():
        print(f"{k}: {v}")
    for file, counts in marker_files[:50]:
        parts = ", ".join(f"{k}={v}" for k, v in counts.items() if v)
        print(f"- {file}: {parts}")

    print("\n=== 结论 ===")
    if missing or compile_errors or forbidden_found:
        print("状态：部分通过")
        if missing:
            print("缺失文件：" + ", ".join(missing))
        if compile_errors:
            print("编译失败：" + ", ".join(compile_errors))
        if forbidden_found:
            print("发现旧结构：" + ", ".join(forbidden_found))
        return 1
    print("状态：通过静态检查。未安装依赖，未下载数据，未运行训练。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
