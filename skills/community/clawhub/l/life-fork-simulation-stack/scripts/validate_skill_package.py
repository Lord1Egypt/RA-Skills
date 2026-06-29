#!/usr/bin/env python3
"""Run package-level checks before publishing or uploading the skill."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/life-fork-grammar.md",
    "references/archetype-tension-axes.md",
    "references/life-archetype-library.md",
    "references/archetype-composer.md",
    "references/event-shock-engine.md",
    "references/life-scene-library.md",
    "references/anti-generic-writing-rules.md",
    "references/magic-score-rubric.md",
    "templates/life-fork-simulation-report.md",
    "templates/delivery-pack.md",
    "examples/real-dialogue-flows.md",
    "examples/html-render-fixture.md",
    "examples/low-information-report.md",
    "examples/magic-score-regression.md",
    "scripts/render_html_report.py",
    "scripts/validate_dialogue_event_agent_flow.py",
    "scripts/validate_html_first_skill.py",
    "scripts/validate_magic_score.py",
    "scripts/validate_report_specificity.py",
    "scripts/validate_report_structure.py",
    "scripts/validate_skill_package.py",
]

VALIDATOR_SCRIPTS = [
    "validate_dialogue_event_agent_flow.py",
    "validate_html_first_skill.py",
    "validate_magic_score.py",
]

MAX_EXAMPLE_FILES = 8


def joined(parts: tuple[str, ...]) -> str:
    return "".join(parts)


DISALLOWED_EXAMPLE_FILENAMES = {
    joined(("meeting", "-", "silence", ".md")),
    joined(("invisible", "-", "work", ".md")),
    joined(("repeated", "-", "overcommitment", ".md")),
}

DISALLOWED_REFERENCE_FILENAMES = {
    joined(("decision", "-", "variables", ".md")),
    joined(("demo", "-", "topic", "-", "playbook", ".md")),
}


FORBIDDEN_TEXT_TERMS = [
    joined(("不", "是")),
    joined(("而", "是")),
    joined(("而", "非")),
    joined(("P", "D", "F")),
    joined(("P", "D", "F", " Snapshot")),
    joined(("H", "T", "M", "L", " Report")),
    joined(("Ch", "rome")),
    joined(("cups", "filter")),
    joined(("print", "-to", "-", "p", "d", "f")),
    joined(("--", "p", "d", "f")),
    joined(("小", "红", "书")),
    joined(("抖", "音")),
    joined(("口", "播")),
    joined(("传", "播", "资", "产")),
    joined(("质", "量", "评", "分", "与", "回", "写", "记", "录")),
    joined(("使", "用", "到", "的", "时", "代", "事", "件")),
    joined(("依", "据", "摘", "要")),
    joined(("事", "件", "来", "源", "：")),
    joined(("人", "生", "线")),
    joined(("平", "行", "宇", "宙")),
    joined(("平", "行", "人", "生")),
    joined(("路", "径", "反", "事", "实")),
    joined(("变", "量", "表")),
    joined(("复", "现", "条", "件")),
    joined(("隐", "性", "变", "量")),
    joined(("work", "around")),
    joined(("大", "量", "变", "量")),
    joined(("个", "人", "变", "量")),
    joined(("每", "条", "路", "径")),
    joined(("每", "条", "路")),
    joined(("那", "条", "路")),
    joined(("未", "选", "择", "路", "径", "必", "须")),
    joined(("结", "构", "化", "输", "入", "变", "量")),
    joined(("输", "入", "变", "量", "模", "板")),
    joined(("多", "路", "径", "推", "演")),
    joined(("低", "置", "信", "度")),
    joined(("低", "材", "料")),
    joined(("低", "信", "息")),
    joined(("每", "条", "线")),
    joined(("当", "前", "置", "信", "度")),
    joined(("报", "告", "置", "信", "度")),
    joined(("当", "前", "材", "料", "：")),
    joined(("当", "前", "材", "料", "充", "分", "度", "：", "低")),
    joined(("低", " / ", "中", " / ", "高")),
    joined(("离", "线", "快", "照")),
    joined(("多", " Agent ", "深", "度", "模", "拟")),
    joined(("内", "部", "张", "力", "轴", "识", "别")),
    joined(("内", "部", "原", "型", "识", "别")),
    joined(("3", " 个", "真", "实", "动", "作")),
    joined(("三", "种", "结", "果", "的", "细", "解", "释")),
    joined(("默", "认", "展", "开", "区", "只", "依", "赖", "分", "叉", "图")),
    joined(("当", "前", "材", "料", "充", "分", "度")),
]

OLD_PATH_TERMS = [
    joined(("p", "d", "f", "-ready", "-delivery")),
    joined(("render", "_", "p", "d", "f", "_ready", "_report")),
    joined(("validate", "_", "p", "d", "f", "_report", "_structure")),
    "__MACOSX",
    "/._",
]

OPENAI_REQUIRED_TERMS = [
    'display_name: "人生岔路模拟栈"',
    'short_description: "用事件冲击和三种结果，把如果当年问题复盘成可保存报告"',
    "$life-fork-simulation-stack",
    "HTML 用户报告",
    "我不想填表",
    "材料有限版",
    "事件冲击卡",
    "30 天验证实验",
    "allow_implicit_invocation: true",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def package_files() -> list[Path]:
    ignored_parts = {".git", "__pycache__"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def check_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def check_openai_yaml(errors: list[str]) -> None:
    path = ROOT / "agents" / "openai.yaml"
    if not path.is_file():
        errors.append("agents/openai.yaml missing")
        return
    text = read_text(path)
    for term in OPENAI_REQUIRED_TERMS:
        if term not in text:
            errors.append(f"agents/openai.yaml missing term: {term}")
    for term in FORBIDDEN_TEXT_TERMS:
        if term in text:
            errors.append(f"agents/openai.yaml contains blocked public term: {term}")


def check_text_terms(errors: list[str]) -> None:
    for path in package_files():
        if path.suffix.lower() not in {".md", ".py", ".yaml", ".yml", ".txt"}:
            continue
        relative = path.relative_to(ROOT)
        text = read_text(path)
        for term in FORBIDDEN_TEXT_TERMS:
            if term in text:
                errors.append(f"{relative} contains blocked text term: {term}")


def check_path_terms(errors: list[str]) -> None:
    for path in package_files():
        normalized = path.relative_to(ROOT).as_posix()
        for term in OLD_PATH_TERMS:
            if term in normalized:
                errors.append(f"old path term remains: {normalized}")


def check_example_scope(errors: list[str]) -> None:
    example_dir = ROOT / "examples"
    if not example_dir.is_dir():
        errors.append("examples directory missing")
        return
    example_files = sorted(path.name for path in example_dir.glob("*.md"))
    if len(example_files) > MAX_EXAMPLE_FILES:
        errors.append(f"too many example files: {len(example_files)} > {MAX_EXAMPLE_FILES}")
    for filename in sorted(DISALLOWED_EXAMPLE_FILENAMES):
        if filename in example_files:
            errors.append(f"legacy behavior example remains: examples/{filename}")


def check_reference_scope(errors: list[str]) -> None:
    reference_dir = ROOT / "references"
    if not reference_dir.is_dir():
        errors.append("references directory missing")
        return
    reference_files = {path.name for path in reference_dir.glob("*.md")}
    for filename in sorted(DISALLOWED_REFERENCE_FILENAMES):
        if filename in reference_files:
            errors.append(f"legacy reference remains: references/{filename}")


def check_readme_listing(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if not readme.is_file():
        errors.append("README.md missing")
        return
    text = read_text(readme)
    skipped = {"README.md", ".gitignore"}
    for path in package_files():
        if path.name in skipped:
            continue
        if path.name not in text:
            relative = path.relative_to(ROOT)
            errors.append(f"README.md directory listing missing file: {relative}")


def check_python_compatibility(errors: list[str]) -> None:
    annotation_union = re.compile(r"(?:->|:)\s*[A-Za-z_][A-Za-z0-9_\[\], .]*\s\|\s(?:None|[A-Za-z_])")
    for path in (ROOT / "scripts").glob("*.py"):
        text = read_text(path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith(("if ", "elif ", "while ")):
                continue
            if annotation_union.search(line):
                relative = path.relative_to(ROOT)
                errors.append(f"{relative}:{line_number} uses Python 3.10 union type syntax")


def check_script_registration(errors: list[str]) -> None:
    required = set(REQUIRED_FILES)
    for path in sorted(SCRIPTS.glob("*.py")):
        relative = path.relative_to(ROOT).as_posix()
        if relative not in required:
            errors.append(f"script file is not registered in REQUIRED_FILES: {relative}")


def run_validators(errors: list[str]) -> None:
    for script_name in VALIDATOR_SCRIPTS:
        script_path = SCRIPTS / script_name
        if not script_path.is_file():
            errors.append(f"validator missing: {script_name}")
            continue
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode != 0:
            output = result.stdout.strip() or "no output"
            errors.append(f"{script_name} failed:\n{output}")


def check_zip(zip_path: Path, errors: list[str]) -> None:
    if not zip_path.is_file():
        errors.append(f"zip file missing: {zip_path}")
        return
    try:
        with zipfile.ZipFile(zip_path) as archive:
            bad_file = archive.testzip()
            if bad_file:
                errors.append(f"zip corrupt member: {bad_file}")
            names = archive.namelist()
    except zipfile.BadZipFile as exc:
        errors.append(f"zip cannot be opened: {exc}")
        return

    required_members = [
        f"life-fork-simulation-stack/{relative}"
        for relative in REQUIRED_FILES
    ]
    for member in required_members:
        if member not in names:
            errors.append(f"zip missing member: {member}")

    for name in names:
        for term in OLD_PATH_TERMS:
            if term in name:
                errors.append(f"zip contains old or hidden path: {name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the skill package.")
    parser.add_argument("--zip", type=Path, help="Optional zip file to validate.")
    parser.add_argument("--skip-subvalidators", action="store_true", help="Skip bundled validator scripts.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    check_required_files(errors)
    check_openai_yaml(errors)
    check_text_terms(errors)
    check_path_terms(errors)
    check_example_scope(errors)
    check_reference_scope(errors)
    check_readme_listing(errors)
    check_python_compatibility(errors)
    check_script_registration(errors)
    if not args.skip_subvalidators:
        run_validators(errors)
    if args.zip:
        check_zip(args.zip, errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
