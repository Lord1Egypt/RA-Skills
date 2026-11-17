#!/usr/bin/env python3
"""Offline structural audit and behavioral experiment tooling for skills.

No command calls a model or external service. A plan is only a set of work
items. Responses must come from real executions before evaluation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote

SCHEMA_VERSION = 1
RUN_SCHEMA_VERSION = 2
VARIANTS = ("baseline", "candidate")
ASSERTION_TYPES = {"contains", "not_contains", "regex", "manual"}
RUN_STATUSES = {"not_run", "blocked", "executed"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
UNFINISHED_RE = re.compile(
    r"(?i)(?:\b(?:TODO|FIXME|TBD)\b|\[\s*(?:TODO|FIXME|TBD)[^\]]*\]|"
    r"(?:replace|fill)\s+(?:this|me|with))"
)
CHINESE_UNFINISHED_LINE_RE = re.compile(
    r"^\s*(?:(?:#{1,6}|>|[-*+]|\d+[.)])\s+)*"
    r"(?:\[(?:\s|x|X)\]\s+)?(?:\*\*|__)?"
    r"(?:待补充|待完善|占位符)(?:\*\*|__)?(?:\s*[：:])?\s*$"
)
MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MD_DEF_RE = re.compile(r"(?m)^ {0,3}\[[^\]\r\n]+\]:(?!:)[ \t]*(\S[^\r\n]*)$")
SECRET_RULES = (
    ("openai-style-key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("assigned-secret", re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret[_-]?key|password)\b"
        r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"
    )),
)
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".env"}
IGNORED_HASH_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache"}
IGNORED_HASH_SUFFIXES = {".pyc", ".pyo"}


class ToolkitError(Exception):
    """Expected input or validation error."""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ToolkitError(f"文件不是有效 UTF-8：{path}") from exc
    except OSError as exc:
        raise ToolkitError(f"无法读取文件：{path} ({exc})") from exc


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ToolkitError(f"文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise ToolkitError(f"JSON 无效：{path}:{exc.lineno}:{exc.colno} {exc.msg}") from exc
    except OSError as exc:
        raise ToolkitError(f"无法读取 JSON：{path} ({exc})") from exc


def write_json(path: Path, data: Any, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x" if exclusive else "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except FileExistsError as exc:
        raise ToolkitError(f"输出文件已存在，plan 不会覆盖：{path}") from exc
    except OSError as exc:
        raise ToolkitError(f"无法写入 JSON：{path} ({exc})") from exc


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def shown(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ToolkitError(f"无法散列文件：{path} ({exc})") from exc
    return digest.hexdigest()


def sha256_directory(root: Path) -> str:
    """Hash relative paths and contents, ignoring runtime cache artifacts."""
    root = root.resolve(strict=True)
    digest = hashlib.sha256()
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        directories[:] = sorted(name for name in directories if name not in IGNORED_HASH_DIRS)
        filenames = sorted(name for name in filenames if Path(name).suffix.lower() not in IGNORED_HASH_SUFFIXES)
        for dirname in directories:
            entry = current_path / dirname
            if entry.is_symlink():
                try:
                    resolved = entry.resolve(strict=True)
                except OSError as exc:
                    raise ToolkitError(f"目录包含损坏的符号链接：{entry}") from exc
                if not inside(resolved, root):
                    raise ToolkitError(f"目录包含越界符号链接：{entry}")
                digest.update(b"L\0" + entry.relative_to(root).as_posix().encode() + b"\0")
                digest.update(os.readlink(entry).encode("utf-8") + b"\0")
        for filename in filenames:
            entry = current_path / filename
            relative = entry.relative_to(root).as_posix().encode("utf-8")
            if entry.is_symlink():
                try:
                    source = entry.resolve(strict=True)
                except OSError as exc:
                    raise ToolkitError(f"目录包含损坏的符号链接：{entry}") from exc
                if not inside(source, root):
                    raise ToolkitError(f"目录包含越界符号链接：{entry}")
                digest.update(b"L\0" + relative + b"\0" + os.readlink(entry).encode("utf-8") + b"\0")
            else:
                source = entry
                digest.update(b"F\0" + relative + b"\0")
            try:
                with source.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                        digest.update(chunk)
            except OSError as exc:
                raise ToolkitError(f"无法散列技能文件：{entry} ({exc})") from exc
            digest.update(b"\0")
    return digest.hexdigest()


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    """Parse the simple YAML subset emitted for new skills, including | and >."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["SKILL.md 缺少起始 YAML frontmatter 分隔线"]
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, ["SKILL.md 缺少结束 YAML frontmatter 分隔线"]
    result: dict[str, str] = {}
    errors: list[str] = []
    index = 1
    while index < end:
        raw = lines[index]
        if not raw.strip() or raw.lstrip().startswith("#"):
            index += 1
            continue
        if raw[:1].isspace():
            index += 1
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", raw)
        if not match:
            errors.append(f"无法解析 frontmatter 第 {index + 1} 行")
            index += 1
            continue
        key, value = match.group(1), (match.group(2) or "")
        if value.strip().startswith(("|", ">")):
            folded = value.strip().startswith(">")
            collected: list[str] = []
            base_indent: int | None = None
            index += 1
            while index < end:
                continuation = lines[index]
                if continuation and not continuation[:1].isspace():
                    break
                if not continuation.strip():
                    collected.append("")
                    index += 1
                    continue
                indent = len(continuation) - len(continuation.lstrip(" "))
                base_indent = indent if base_indent is None else base_indent
                collected.append(continuation[min(base_indent, indent):])
                index += 1
            result[key] = (" " if folded else "\n").join(collected).strip()
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        result[key] = value.strip()
        index += 1
    return result, errors


def link_destination(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        return raw[1:raw.index(">")]
    return re.split(r"\s+(?=['\"(])", raw, maxsplit=1)[0].strip()


def markdown_destinations(text: str) -> list[str]:
    values = [link_destination(m.group(1)) for m in MD_LINK_RE.finditer(text)]
    values.extend(link_destination(m.group(1)) for m in MD_DEF_RE.finditer(text))
    return [value for value in values if value]


def audit_report(root: Path, findings: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {level: sum(item["level"] == level for item in findings) for level in ("fail", "warn")}
    status = "fail" if counts["fail"] else ("warn" if counts["warn"] else "pass")
    return {
        "schema_version": 1,
        "kind": "skill_structural_audit",
        "skill_path": str(root),
        "status": status,
        "summary": counts,
        "findings": findings,
        "behavioral_validation": {
            "performed": False,
            "note": "此报告只检查结构、引用和静态风险形状，不证明技能行为有效。",
        },
    }

def audit_skill(skill_dir: Path) -> dict[str, Any]:
    original = skill_dir.absolute()
    root = original.resolve(strict=False)
    findings: list[dict[str, Any]] = []

    def add(level: str, code: str, message: str, path: Path | None = None, line: int | None = None) -> None:
        item: dict[str, Any] = {"level": level, "code": code, "message": message}
        if path is not None:
            item["path"] = shown(path, root)
        if line is not None:
            item["line"] = line
        findings.append(item)

    if not original.exists() or not original.is_dir():
        add("fail", "skill-dir-missing", "技能目录不存在或不是目录", original)
        return audit_report(root, findings)
    root = original.resolve()
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        add("fail", "skill-file-missing", "缺少必要的 SKILL.md", skill_file)
        return audit_report(root, findings)
    try:
        skill_text = read_text(skill_file)
    except ToolkitError as exc:
        add("fail", "skill-file-unreadable", str(exc), skill_file)
        return audit_report(root, findings)

    frontmatter, errors = parse_frontmatter(skill_text)
    for error in errors:
        add("fail", "frontmatter-invalid", error, skill_file)
    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()
    if not name:
        add("fail", "name-missing", "frontmatter 缺少非空 name", skill_file)
    elif len(name) > 64 or not NAME_RE.fullmatch(name):
        add("fail", "name-invalid", "name 仅可含小写字母、数字和单连字符，且不超过 64 个字符", skill_file)
    elif root.name != name:
        add("fail", "directory-name-mismatch", f"目录名应与 name 一致：{name}", skill_file)
    if not description:
        add("fail", "description-missing", "frontmatter 缺少非空 description", skill_file)
    elif len(description) > 1200:
        add("warn", "description-long", "description 超过 1200 个字符，可能影响发现与路由", skill_file)

    markdown_files: list[Path] = []
    text_files: list[Path] = []
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        directories[:] = sorted(name for name in directories if name not in IGNORED_HASH_DIRS)
        filenames.sort()
        for dirname in directories:
            entry = current_path / dirname
            if not entry.is_symlink():
                continue
            try:
                resolved = entry.resolve(strict=True)
            except OSError:
                add("fail", "broken-symlink", "目录符号链接目标不存在", entry)
                continue
            if not inside(resolved, root):
                add("fail", "escaping-symlink", "目录符号链接越出技能目录，审计不会跟随", entry)
            else:
                add("warn", "directory-symlink", "目录符号链接不会被递归审计", entry)
        for filename in filenames:
            entry = current_path / filename
            if entry.is_symlink():
                try:
                    resolved = entry.resolve(strict=True)
                except OSError:
                    add("fail", "broken-symlink", "文件符号链接目标不存在", entry)
                    continue
                if not inside(resolved, root):
                    add("fail", "escaping-symlink", "文件符号链接越出技能目录，审计不会读取", entry)
                    continue
            try:
                size = entry.stat().st_size
            except OSError as exc:
                add("fail", "file-unreadable", f"无法读取文件元数据：{exc}", entry)
                continue
            if size > 5 * 1024 * 1024:
                add("warn", "large-file", "文件超过 5 MiB，可能降低技能便携性", entry)
            if len(str(entry)) > 240:
                add("warn", "long-path", "完整路径超过 240 个字符，部分环境可能无法使用", entry)
            if entry.suffix.lower() == ".md":
                markdown_files.append(entry)
            if entry.suffix.lower() in TEXT_SUFFIXES or filename == ".env":
                text_files.append(entry)

    # Report path and line only. Never place a suspected value in output.
    for text_file in text_files:
        try:
            text = read_text(text_file)
        except ToolkitError as exc:
            add("fail", "text-unreadable", str(exc), text_file)
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for rule_name, pattern in SECRET_RULES:
                if pattern.search(line):
                    add("warn", "possible-secret", f"发现疑似密钥形状（规则：{rule_name}）", text_file, line_number)

    for markdown_file in markdown_files:
        try:
            text = read_text(markdown_file)
        except ToolkitError:
            continue
        parts = markdown_file.relative_to(root).parts
        is_template = bool(parts and parts[0] in {"assets", "examples", "templates"})
        for line_number, line in enumerate(text.splitlines(), 1):
            if UNFINISHED_RE.search(line):
                add(
                    "warn" if is_template else "fail",
                    "template-placeholder" if is_template else "unfinished-marker",
                    "模板中的待填写示例" if is_template else "发现未完成或占位标记",
                    markdown_file,
                    line_number,
                )
            elif CHINESE_UNFINISHED_LINE_RE.fullmatch(line):
                add(
                    "warn",
                    "template-placeholder" if is_template else "possible-unfinished-marker",
                    (
                        "模板中的待填写示例"
                        if is_template
                        else "整行中文待写标记，需人工确认是否为有意输出"
                    ),
                    markdown_file,
                    line_number,
                )
            if len(line) > 500:
                add("warn", "very-long-line", "单行超过 500 个字符，可读性较差", markdown_file, line_number)
        for destination in markdown_destinations(text):
            lowered = destination.lower()
            if lowered.startswith(("http://", "https://", "mailto:", "data:", "tel:")) or destination.startswith("#"):
                continue
            decoded = unquote(destination).replace("\\", "/")
            target_text = decoded.split("#", 1)[0].split("?", 1)[0]
            if not target_text:
                continue
            candidate = Path(target_text)
            if candidate.is_absolute():
                add("warn", "absolute-local-reference", "本地引用使用绝对路径，不便携", markdown_file)
                resolved = candidate.resolve(strict=False)
            else:
                resolved = (markdown_file.parent / candidate).resolve(strict=False)
            if not inside(resolved, root):
                add("fail", "reference-escapes-skill", f"本地引用越出技能目录：{destination}", markdown_file)
                continue
            try:
                strict_resolved = resolved.resolve(strict=True)
            except OSError:
                add("fail", "reference-missing", f"本地引用不存在：{destination}", markdown_file)
                continue
            if not inside(strict_resolved, root):
                add("fail", "reference-symlink-escape", f"本地引用经符号链接越出技能目录：{destination}", markdown_file)
    if len(skill_text.splitlines()) > 500:
        add("warn", "skill-file-long", "SKILL.md 超过 500 行，建议将条件性细节移入 references", skill_file)
    return audit_report(root, findings)


def validate_suite(data: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(data, dict):
        raise ToolkitError("suite 顶层必须是 JSON 对象")
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version 必须为 1")
    if not isinstance(data.get("skill_name"), str) or not data["skill_name"].strip():
        errors.append("skill_name 必须是非空字符串")
    dimension_ids: set[str] = set()
    coverage_contract = data.get("coverage_contract")
    if coverage_contract is not None:
        if not isinstance(coverage_contract, dict):
            errors.append("coverage_contract 必须是对象")
        else:
            dimensions = coverage_contract.get("dimensions")
            if not isinstance(dimensions, list) or not dimensions:
                errors.append("coverage_contract.dimensions 必须是非空数组")
                dimensions = []
            for dimension_index, dimension in enumerate(dimensions):
                prefix = f"coverage_contract.dimensions[{dimension_index}]"
                if not isinstance(dimension, dict):
                    errors.append(f"{prefix} 必须是对象")
                    continue
                dimension_id = dimension.get("id")
                if not isinstance(dimension_id, str) or not dimension_id.strip():
                    errors.append(f"{prefix}.id 必须是非空字符串")
                elif dimension_id in dimension_ids:
                    errors.append(f"coverage dimension id 重复：{dimension_id}")
                else:
                    dimension_ids.add(dimension_id)
                if not isinstance(dimension.get("description"), str) or not dimension["description"].strip():
                    errors.append(f"{prefix}.description 必须是非空字符串")
                if not isinstance(dimension.get("required"), bool):
                    errors.append(f"{prefix}.required 必须是布尔值")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases 必须是非空数组")
        cases = []
    case_ids: set[str] = set()
    for case_index, case in enumerate(cases):
        prefix = f"cases[{case_index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} 必须是对象")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{prefix}.id 必须是非空字符串")
        elif case_id in case_ids:
            errors.append(f"case id 重复：{case_id}")
        else:
            case_ids.add(case_id)
        if not isinstance(case.get("category"), str) or not case["category"].strip():
            errors.append(f"{prefix}.category 必须是非空字符串")
        turns = case.get("turns")
        if not isinstance(turns, list) or not turns:
            errors.append(f"{prefix}.turns 必须是非空数组")
        else:
            for turn_index, turn in enumerate(turns):
                turn_prefix = f"{prefix}.turns[{turn_index}]"
                if not isinstance(turn, dict) or turn.get("role") != "user":
                    errors.append(f"{turn_prefix}.role 必须为 user")
                elif not isinstance(turn.get("content"), str) or not turn["content"].strip():
                    errors.append(f"{turn_prefix}.content 必须是非空字符串")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"{prefix}.assertions 必须是非空数组")
            assertions = []
        assertion_ids: set[str] = set()
        for assertion_index, assertion in enumerate(assertions):
            assertion_prefix = f"{prefix}.assertions[{assertion_index}]"
            if not isinstance(assertion, dict):
                errors.append(f"{assertion_prefix} 必须是对象")
                continue
            assertion_id = assertion.get("id")
            if not isinstance(assertion_id, str) or not assertion_id.strip():
                errors.append(f"{assertion_prefix}.id 必须是非空字符串")
            elif assertion_id in assertion_ids:
                errors.append(f"{prefix} assertion id 重复：{assertion_id}")
            else:
                assertion_ids.add(assertion_id)
            assertion_type = assertion.get("type")
            if not isinstance(assertion_type, str) or assertion_type not in ASSERTION_TYPES:
                errors.append(f"{assertion_prefix}.type 不受支持")
            if isinstance(assertion_type, str) and assertion_type in {"contains", "not_contains", "regex"}:
                value = assertion.get("value")
                if not isinstance(value, str) or not value:
                    errors.append(f"{assertion_prefix}.value 必须是非空字符串")
                elif assertion_type == "regex":
                    try:
                        re.compile(value)
                    except re.error as exc:
                        errors.append(f"{assertion_prefix}.value 正则无效：{exc}")
            if not isinstance(assertion.get("description"), str) or not assertion["description"].strip():
                errors.append(f"{assertion_prefix}.description 必须是非空字符串")
            if not isinstance(assertion.get("critical"), bool):
                errors.append(f"{assertion_prefix}.critical 必须是布尔值")
            mapped_dimensions = assertion.get("dimensions", [])
            if not isinstance(mapped_dimensions, list):
                errors.append(f"{assertion_prefix}.dimensions 必须是字符串数组")
            else:
                seen_dimensions: set[str] = set()
                for mapped_index, dimension_id in enumerate(mapped_dimensions):
                    if not isinstance(dimension_id, str) or not dimension_id.strip():
                        errors.append(f"{assertion_prefix}.dimensions[{mapped_index}] 必须是非空字符串")
                    elif dimension_id in seen_dimensions:
                        errors.append(f"{assertion_prefix}.dimensions 存在重复 id：{dimension_id}")
                    elif dimension_id not in dimension_ids:
                        errors.append(f"{assertion_prefix}.dimensions 引用了未知维度：{dimension_id}")
                    else:
                        seen_dimensions.add(dimension_id)
    if errors:
        raise ToolkitError("suite 校验失败：" + "；".join(errors))
    return data

def relative_reference(target: Path, output: Path) -> str:
    target_abs = target.resolve()
    output_parent = output.parent.resolve()
    # Windows cannot express a relative path between different drives or shares.
    # Keep an absolute reference there; same-volume plans remain relocatable.
    if target_abs.anchor.casefold() != output_parent.anchor.casefold():
        return target_abs.as_posix()
    return Path(os.path.relpath(target_abs, output_parent)).as_posix()


def suite_dimensions(suite: dict[str, Any]) -> list[dict[str, Any]]:
    contract = suite.get("coverage_contract")
    return list(contract.get("dimensions", [])) if isinstance(contract, dict) else []


def missing_required_dimensions(suite: dict[str, Any]) -> list[str]:
    mapped = {
        dimension_id
        for case in suite["cases"]
        for assertion in case["assertions"]
        for dimension_id in assertion.get("dimensions", [])
    }
    return [
        dimension["id"]
        for dimension in suite_dimensions(suite)
        if dimension["required"] and dimension["id"] not in mapped
    ]


def validate_variants(variants: Any) -> tuple[str, ...]:
    if isinstance(variants, (str, bytes)) or not isinstance(variants, (list, tuple)) or not variants:
        raise ToolkitError("variants 必须是非空数组")
    selected: list[str] = []
    for index, variant in enumerate(variants):
        if not isinstance(variant, str) or variant not in VARIANTS:
            raise ToolkitError(f"variants[{index}] 必须是 baseline 或 candidate")
        if variant in selected:
            raise ToolkitError(f"variant 重复：{variant}")
        selected.append(variant)
    return tuple(selected)


def create_plan(
    suite_path: Path,
    skill_dir: Path,
    output_path: Path,
    rounds: int,
    variants: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    if not isinstance(rounds, int) or isinstance(rounds, bool) or rounds < 1:
        raise ToolkitError("rounds 必须是正整数")
    if output_path.exists():
        raise ToolkitError(f"输出文件已存在，plan 不会覆盖：{output_path}")
    suite_path = suite_path.resolve(strict=True)
    skill_dir = skill_dir.resolve(strict=True)
    if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
        raise ToolkitError(f"skill 必须是含 SKILL.md 的目录：{skill_dir}")
    output_abs = output_path.absolute()
    if inside(output_abs, skill_dir):
        raise ToolkitError("run 输出不能位于被散列的 skill 目录内")
    suite = validate_suite(load_json(suite_path))
    # The four-argument Python API remains a schema-1 compatibility surface.
    # The CLI always passes its --variants value and therefore emits schema 2.
    legacy = variants is None
    selected_variants = VARIANTS if legacy else validate_variants(variants)
    runs = [
        ({
            "case_id": case["id"],
            "round": round_number,
            "variant": variant,
            "status": "not_run",
            "response_path": None,
            "judgments": {},
        } if legacy else {
            "case_id": case["id"],
            "round": round_number,
            "variant": variant,
            "status": "not_run",
            "execution_id": None,
            "response_path": None,
            "response_sha256": None,
            "turn_evidence": [
                {
                    "turn": turn_number,
                    "status": "not_run",
                    "response_path": None,
                    "response_sha256": None,
                }
                for turn_number in range(1, len(case["turns"]) + 1)
            ],
            "judgments": {},
        })
        for case in suite["cases"]
        for round_number in range(1, rounds + 1)
        for variant in selected_variants
    ]
    plan = {
        "schema_version": 1 if legacy else RUN_SCHEMA_VERSION,
        "suite_path": relative_reference(suite_path, output_abs),
        "suite_sha256": sha256_file(suite_path),
        "skill_path": relative_reference(skill_dir, output_abs),
        "skill_sha256": sha256_directory(skill_dir),
        "rounds": rounds,
        "execution_note": (
            "本工具不调用模型，也不能证明响应来自哪个模型。baseline 执行时不要加载技能；"
            "candidate 执行时加载 skill_path。真实执行后才可填写执行证据。"
        ),
        "runs": runs,
    }
    if not legacy:
        plan["variants"] = list(selected_variants)
        plan["missing_dimensions"] = missing_required_dimensions(suite)
        plan["evidence_note"] = (
            "sha256 只证明评估时读取的文件与 run 中记录一致，不证明输出来源真实性。"
        )
    return plan


def resolve_run_reference(run_file: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ToolkitError(f"{label} 必须是非空相对路径")
    candidate = Path(value)
    if candidate.is_absolute():
        raise ToolkitError(f"{label} 必须相对 run 文件解析，不能是绝对路径")
    return (run_file.parent / candidate).resolve(strict=False)


def evaluation_failure(run_file: Path, errors: list[str]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "skill_behavioral_evaluation",
        "run_path": str(run_file.resolve(strict=False)),
        "status": "fail",
        "conclusion_allowed": False,
        "errors": errors,
        "note": "计划、路径、散列或记录不完整，不能形成行为结论。",
    }


def evaluate_run(run_file: Path) -> dict[str, Any]:
    run_file = run_file.resolve(strict=True)
    try:
        plan = load_json(run_file)
        if not isinstance(plan, dict) or plan.get("schema_version") not in {1, RUN_SCHEMA_VERSION}:
            raise ToolkitError("run 顶层必须是 schema_version 1 或 2 的 JSON 对象")
        run_schema = plan["schema_version"]
        selected_variants = VARIANTS if run_schema == 1 else validate_variants(plan.get("variants"))
        rounds = plan.get("rounds")
        if not isinstance(rounds, int) or isinstance(rounds, bool) or rounds < 1:
            raise ToolkitError("run rounds 必须是正整数")
        suite_path = resolve_run_reference(run_file, plan.get("suite_path"), "suite_path")
        skill_path = resolve_run_reference(run_file, plan.get("skill_path"), "skill_path")
        suite = validate_suite(load_json(suite_path))
        if not skill_path.is_dir() or not (skill_path / "SKILL.md").is_file():
            raise ToolkitError(f"skill_path 不是有效技能目录：{skill_path}")
        if plan.get("suite_sha256") != sha256_file(suite_path):
            raise ToolkitError("suite_sha256 与当前 suite 内容不一致，拒绝形成结论")
        if plan.get("skill_sha256") != sha256_directory(skill_path):
            raise ToolkitError("skill_sha256 与当前 skill 内容不一致，拒绝形成结论")
    except ToolkitError as exc:
        return evaluation_failure(run_file, [str(exc)])

    cases = {case["id"]: case for case in suite["cases"]}
    expected = {
        (case_id, round_number, variant)
        for case_id in cases
        for round_number in range(1, rounds + 1)
        for variant in selected_variants
    }
    records = plan.get("runs")
    if not isinstance(records, list):
        return evaluation_failure(run_file, ["runs 必须是数组"])
    seen: set[tuple[str, int, str]] = set()
    errors: list[str] = []
    validated: list[tuple[dict[str, Any], tuple[str, int, str]]] = []
    execution_ids: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"runs[{index}] 必须是对象")
            continue
        case_id = record.get("case_id")
        round_value = record.get("round")
        variant = record.get("variant")
        if (
            not isinstance(case_id, str)
            or not isinstance(round_value, int)
            or isinstance(round_value, bool)
            or not isinstance(variant, str)
        ):
            errors.append(f"runs[{index}] 的 case_id/round/variant 类型无效")
            continue
        key = (case_id, round_value, variant)
        if key not in expected:
            errors.append(f"runs[{index}] 指向不存在的 case/round/variant：{key}")
            continue
        if key in seen:
            errors.append(f"runs[{index}] 重复记录：{key}")
            continue
        seen.add(key)
        status_value = record.get("status")
        if not isinstance(status_value, str) or status_value not in RUN_STATUSES:
            errors.append(f"runs[{index}].status 必须是 executed、blocked 或 not_run")
        if not isinstance(record.get("judgments"), dict):
            errors.append(f"runs[{index}].judgments 必须是对象")
        if run_schema == RUN_SCHEMA_VERSION:
            execution_id = record.get("execution_id")
            if status_value == "executed":
                if not isinstance(execution_id, str) or not execution_id.strip():
                    errors.append(f"runs[{index}].execution_id 在 executed 时必须是非空字符串")
                elif execution_id in execution_ids:
                    errors.append(f"runs[{index}].execution_id 重复：{execution_id}")
                else:
                    execution_ids.add(execution_id)
            elif execution_id is not None and (not isinstance(execution_id, str) or not execution_id.strip()):
                errors.append(f"runs[{index}].execution_id 必须为 null 或非空字符串")
            elif isinstance(execution_id, str):
                if execution_id in execution_ids:
                    errors.append(f"runs[{index}].execution_id 重复：{execution_id}")
                else:
                    execution_ids.add(execution_id)
            expected_turns = len(cases[case_id]["turns"])
            turn_evidence = record.get("turn_evidence")
            if not isinstance(turn_evidence, list) or len(turn_evidence) != expected_turns:
                errors.append(f"runs[{index}].turn_evidence 必须包含 {expected_turns} 条逐轮证据")
            else:
                seen_turns: set[int] = set()
                for evidence_index, evidence in enumerate(turn_evidence):
                    evidence_prefix = f"runs[{index}].turn_evidence[{evidence_index}]"
                    if not isinstance(evidence, dict):
                        errors.append(f"{evidence_prefix} 必须是对象")
                        continue
                    turn_number = evidence.get("turn")
                    if (
                        not isinstance(turn_number, int)
                        or isinstance(turn_number, bool)
                        or turn_number < 1
                        or turn_number > expected_turns
                    ):
                        errors.append(f"{evidence_prefix}.turn 无效")
                    elif turn_number in seen_turns:
                        errors.append(f"{evidence_prefix}.turn 重复：{turn_number}")
                    else:
                        seen_turns.add(turn_number)
                    turn_status = evidence.get("status")
                    if not isinstance(turn_status, str) or turn_status not in RUN_STATUSES:
                        errors.append(f"{evidence_prefix}.status 无效")
                if seen_turns != set(range(1, expected_turns + 1)):
                    errors.append(f"runs[{index}].turn_evidence 未完整覆盖用户轮次")
        validated.append((record, key))
    missing = expected - seen
    if missing:
        errors.append(f"缺少 {len(missing)} 条计划记录")
    if errors:
        return evaluation_failure(run_file, errors)

    # Schema 2 requires an independent, hash-bound assistant output for every
    # user turn, plus a combined response that exactly represents all turns.
    strict_responses: dict[tuple[str, int, str], tuple[str, Path]] = {}
    evidence_path_owners: dict[Path, tuple[str, int, str]] = {}
    if run_schema == RUN_SCHEMA_VERSION:
        for record, key in validated:
            if record["status"] != "executed":
                continue
            try:
                response_path = resolve_run_reference(run_file, record.get("response_path"), "response_path")
                response = read_text(response_path)
                if not response.strip():
                    raise ToolkitError(f"响应文件为空或仅含空白：{response_path}")
                if not isinstance(record.get("response_sha256"), str):
                    raise ToolkitError(f"{key} response_sha256 必须是字符串")
                if record["response_sha256"] != sha256_file(response_path):
                    raise ToolkitError(f"{key} response_sha256 与响应文件不一致")
                paths_for_record = {response_path}
                turn_path_owners: dict[Path, int] = {}
                turn_responses: list[str] = []
                for evidence in sorted(record["turn_evidence"], key=lambda item: item["turn"]):
                    if evidence.get("status") != "executed":
                        raise ToolkitError(f"{key} 第 {evidence.get('turn')} 轮未标记 executed")
                    turn_path = resolve_run_reference(
                        run_file,
                        evidence.get("response_path"),
                        f"{key} turn {evidence.get('turn')} response_path",
                    )
                    prior_turn = turn_path_owners.get(turn_path)
                    if prior_turn is not None:
                        raise ToolkitError(
                            f"{key} 第 {prior_turn} 轮与第 {evidence.get('turn')} 轮"
                            f"复用了同一响应证据文件：{shown(turn_path, run_file.parent)}"
                        )
                    turn_path_owners[turn_path] = evidence["turn"]
                    turn_response = read_text(turn_path)
                    if not turn_response.strip():
                        raise ToolkitError(f"逐轮响应文件为空或仅含空白：{turn_path}")
                    if not isinstance(evidence.get("response_sha256"), str):
                        raise ToolkitError(f"{key} 第 {evidence.get('turn')} 轮 response_sha256 必须是字符串")
                    if evidence["response_sha256"] != sha256_file(turn_path):
                        raise ToolkitError(f"{key} 第 {evidence.get('turn')} 轮响应散列不一致")
                    paths_for_record.add(turn_path)
                    turn_responses.append(turn_response)
                expected_combined = "\n\n".join(turn_responses).strip()
                if response.strip() != expected_combined:
                    raise ToolkitError(f"{key} combined response 与逐轮 assistant 输出不一致")
                for evidence_path in paths_for_record:
                    owner = evidence_path_owners.get(evidence_path)
                    if owner is not None and owner != key:
                        raise ToolkitError(f"不同记录复用了同一响应证据文件：{shown(evidence_path, run_file.parent)}")
                    evidence_path_owners[evidence_path] = key
                strict_responses[key] = (response, response_path)
            except ToolkitError as exc:
                errors.append(str(exc))
        if errors:
            return evaluation_failure(run_file, errors)

    results: list[dict[str, Any]] = []
    critical_failures: list[dict[str, Any]] = []
    manual_unassessed: list[dict[str, Any]] = []
    total_checks = 0
    evaluated_checks = 0
    dimensions = suite_dimensions(suite)
    dimension_coverage: dict[str, dict[str, dict[str, Any]]] = {
        variant: {
            dimension["id"]: {
                "id": dimension["id"],
                "description": dimension["description"],
                "required": dimension["required"],
                "missing": True,
                "planned": 0,
                "executed": 0,
                "assessed": 0,
                "passed": 0,
                "verified": False,
            }
            for dimension in dimensions
        }
        for variant in selected_variants
    }
    for record, (case_id, round_number, variant) in validated:
        case = cases[case_id]
        total_checks += len(case["assertions"])
        for assertion in case["assertions"]:
            for dimension_id in assertion.get("dimensions", []):
                dimension_coverage[variant][dimension_id]["planned"] += 1
        result: dict[str, Any] = {
            "case_id": case_id,
            "round": round_number,
            "variant": variant,
            "execution_status": record["status"],
            "result": record["status"],
            "assertions": [],
        }
        if record["status"] != "executed":
            results.append(result)
            continue
        try:
            if run_schema == RUN_SCHEMA_VERSION:
                response, response_path = strict_responses[(case_id, round_number, variant)]
            else:
                response_path = resolve_run_reference(run_file, record.get("response_path"), "response_path")
                response = read_text(response_path)
                if not response.strip():
                    raise ToolkitError(f"响应文件为空或仅含空白：{response_path}")
            result["response_path"] = shown(response_path, run_file.parent)
        except ToolkitError as exc:
            result["result"] = "fail"
            result["error"] = str(exc)
            results.append(result)
            continue
        for assertion in case["assertions"]:
            assertion_id = assertion["id"]
            assertion_type = assertion["type"]
            assessed = True
            passed = False
            evidence = ""
            mapped_dimensions = assertion.get("dimensions", [])
            for dimension_id in mapped_dimensions:
                dimension_coverage[variant][dimension_id]["executed"] += 1
            if assertion_type == "contains":
                passed = assertion["value"] in response
                evidence = "response contains expected text" if passed else "expected text not found"
            elif assertion_type == "not_contains":
                passed = assertion["value"] not in response
                evidence = "forbidden text absent" if passed else "forbidden text found"
            elif assertion_type == "regex":
                passed = re.search(assertion["value"], response, flags=re.MULTILINE) is not None
                evidence = "regular expression matched" if passed else "regular expression did not match"
            else:
                judgment = record["judgments"].get(assertion_id)
                if (
                    isinstance(judgment, dict)
                    and isinstance(judgment.get("passed"), bool)
                    and isinstance(judgment.get("evidence"), str)
                    and judgment["evidence"].strip()
                ):
                    passed = judgment["passed"]
                    evidence = judgment["evidence"].strip()
                else:
                    assessed = False
                    evidence = "manual judgment missing passed boolean or non-empty evidence"
                    manual_unassessed.append({
                        "case_id": case_id,
                        "round": round_number,
                        "variant": variant,
                        "assertion_id": assertion_id,
                    })
            if assessed:
                evaluated_checks += 1
                for dimension_id in mapped_dimensions:
                    dimension_coverage[variant][dimension_id]["assessed"] += 1
                    if passed:
                        dimension_coverage[variant][dimension_id]["passed"] += 1
            assertion_result = {
                "id": assertion_id,
                "type": assertion_type,
                "critical": assertion["critical"],
                "assessed": assessed,
                "passed": passed if assessed else None,
                "evidence": evidence,
                "dimensions": mapped_dimensions,
            }
            result["assertions"].append(assertion_result)
            if assertion["critical"] and assessed and not passed:
                critical_failures.append({
                    "case_id": case_id,
                    "round": round_number,
                    "variant": variant,
                    "assertion_id": assertion_id,
                })
        result["result"] = (
            "pass"
            if result["assertions"] and all(item["passed"] is True for item in result["assertions"])
            else "fail"
        )
        results.append(result)
    total_records = len(results)
    executed_records = sum(item["execution_status"] == "executed" for item in results)
    passed_records = sum(item["result"] == "pass" for item in results)
    variants: dict[str, Any] = {}
    per_round: list[dict[str, Any]] = []
    worst_rounds: dict[str, Any] = {}
    for variant in selected_variants:
        variant_items = [item for item in results if item["variant"] == variant]
        round_rows: list[dict[str, Any]] = []
        for round_number in range(1, rounds + 1):
            items = [item for item in variant_items if item["round"] == round_number]
            round_passed = sum(item["result"] == "pass" for item in items)
            round_executed = sum(item["execution_status"] == "executed" for item in items)
            if any(item["result"] == "fail" for item in items):
                round_status = "fail"
            elif round_executed < len(items):
                round_status = "incomplete"
            else:
                round_status = "pass"
            row = {
                "variant": variant,
                "round": round_number,
                "status": round_status,
                "passed_records": round_passed,
                "executed_records": round_executed,
                "total_records": len(items),
                "pass_rate": round(round_passed / len(items), 4) if items else 0.0,
            }
            round_rows.append(row)
            per_round.append(row)
        severity = {"fail": 0, "incomplete": 1, "pass": 2}
        worst_rounds[variant] = min(
            round_rows, key=lambda item: (severity[item["status"]], item["pass_rate"], item["round"])
        )
        variants[variant] = {
            "total_records": len(variant_items),
            "executed_records": sum(item["execution_status"] == "executed" for item in variant_items),
            "passed_records": sum(item["result"] == "pass" for item in variant_items),
            "failed_records": sum(item["result"] == "fail" for item in variant_items),
            "blocked_records": sum(item["execution_status"] == "blocked" for item in variant_items),
            "not_run_records": sum(item["execution_status"] == "not_run" for item in variant_items),
            "rounds_passed": sum(item["status"] == "pass" for item in round_rows),
            "rounds_total": rounds,
        }
    for variant in selected_variants:
        for dimension in dimension_coverage[variant].values():
            dimension["missing"] = dimension["planned"] == 0
            dimension["verified"] = (
                dimension["planned"] > 0
                and dimension["executed"] == dimension["planned"]
                and dimension["assessed"] == dimension["planned"]
                and dimension["passed"] == dimension["planned"]
            )

    for variant in selected_variants:
        variant_items = [item for item in results if item["variant"] == variant]
        variant_total_checks = sum(len(cases[item["case_id"]]["assertions"]) for item in variant_items)
        variant_assessed_checks = sum(
            assertion["assessed"] is True
            for item in variant_items
            for assertion in item["assertions"]
        )
        required_verified = all(
            row["verified"]
            for row in dimension_coverage[variant].values()
            if row["required"]
        )
        required_assessed = all(
            row["planned"] > 0
            and row["executed"] == row["planned"]
            and row["assessed"] == row["planned"]
            for row in dimension_coverage[variant].values()
            if row["required"]
        )
        variant_complete = all(item["execution_status"] == "executed" for item in variant_items)
        variant_pass = (
            variant_complete
            and all(item["result"] == "pass" for item in variant_items)
            and (run_schema == 1 or required_verified)
        )
        variants[variant]["status"] = "pass" if variant_pass else "fail"
        variants[variant]["conclusion_allowed"] = (
            variant_complete
            and variant_assessed_checks == variant_total_checks
            and (run_schema == 1 or required_assessed)
        )

    complete = executed_records == total_records
    status = "pass" if all(variants[name]["status"] == "pass" for name in selected_variants) else "fail"
    scenario_coverage: dict[str, Any]
    if run_schema == 1:
        scenario_coverage = {
            "availability": "unavailable",
            "strict_evidence": False,
            "evidence_level": "legacy_listed_cases_only",
            "note": "schema 1 只证明已列用例的执行情况，不能追溯或声称场景全覆盖。",
        }
    else:
        scenario_coverage = {
            "availability": "available" if dimensions else "unavailable",
            "strict_evidence": True,
            "evidence_level": (
                "dimension_contract" if dimensions else "strict_execution_without_dimension_contract"
            ),
            "missing_dimensions": missing_required_dimensions(suite),
            "variants": {
                variant: list(dimension_coverage[variant].values())
                for variant in selected_variants
            },
            "note": (
                "逐轮证据严格校验已启用，但 suite 未声明 coverage_contract，不能声称场景全覆盖。"
                if not dimensions
                else "覆盖结论只来自断言到维度的显式映射。"
            ),
        }
    candidate_status = variants.get("candidate", {}).get("status", "not_planned")
    baseline_status = variants.get("baseline", {}).get("status", "not_planned")
    comparison_allowed = (
        "candidate" in variants
        and "baseline" in variants
        and variants["candidate"]["conclusion_allowed"]
        and variants["baseline"]["conclusion_allowed"]
    )
    return {
        "schema_version": 1,
        "kind": "skill_behavioral_evaluation",
        "run_path": str(run_file),
        "status": status,
        "conclusion_allowed": all(variants[name]["conclusion_allowed"] for name in selected_variants),
        "hashes_verified": True,
        "response_hashes_verified": run_schema == RUN_SCHEMA_VERSION,
        "candidate_status": candidate_status,
        "baseline_status": baseline_status,
        "comparison_allowed": comparison_allowed,
        "coverage": {
            "records_executed": executed_records,
            "records_total": total_records,
            "record_coverage": round(executed_records / total_records, 4) if total_records else 0.0,
            "assertions_evaluated": evaluated_checks,
            "assertions_total": total_checks,
            "assertion_coverage": round(evaluated_checks / total_checks, 4) if total_checks else 0.0,
        },
        "variants": variants,
        "scenario_coverage": scenario_coverage,
        "per_round": per_round,
        "worst_rounds": worst_rounds,
        "critical_failures": critical_failures,
        "manual_unassessed": manual_unassessed,
        "results": results,
        "note": (
            "只有 executed 记录读取了真实响应；blocked/not_run 不计为通过。"
            "散列只证明评估文件的一致性，不证明输出来源真实性。"
            "结构审计与文本断言仍不能替代真实任务产物的人工或环境验证。"
        ),
    }


def emit_stdout_json(data: Any) -> None:
    """Write one complete JSON document to stdout with no status chatter."""
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def command_audit(args: argparse.Namespace) -> int:
    report = audit_skill(Path(args.skill_dir))
    if args.stdout_json:
        emit_stdout_json(report)
    else:
        write_json(Path(args.output), report)
        print(f"audit: {report['status']} -> {args.output}")
    return 1 if report["status"] == "fail" else 0


def command_plan(args: argparse.Namespace) -> int:
    plan = create_plan(
        Path(args.suite),
        Path(args.skill),
        Path(args.output),
        args.rounds,
        variants=args.variants,
    )
    if args.stdout_json:
        emit_stdout_json(plan)
    else:
        write_json(Path(args.output), plan, exclusive=True)
        print(f"plan: {len(plan['runs'])} records -> {args.output}")
    return 0


def protect_evaluation_sources(run_path: Path, output_path: Path) -> None:
    """Prevent the report from overwriting evidence named by the run."""
    run_abs = run_path.resolve(strict=False)
    output_abs = output_path.resolve(strict=False)
    if output_abs == run_abs:
        raise ToolkitError("evaluate 输出不能覆盖 run 文件")
    try:
        plan = load_json(run_abs)
    except ToolkitError:
        return
    if not isinstance(plan, dict):
        return
    suite_value = plan.get("suite_path")
    if isinstance(suite_value, str) and suite_value.strip() and not Path(suite_value).is_absolute():
        if output_abs == (run_abs.parent / suite_value).resolve(strict=False):
            raise ToolkitError("evaluate 输出不能覆盖 suite 文件")
    skill_value = plan.get("skill_path")
    if isinstance(skill_value, str) and skill_value.strip() and not Path(skill_value).is_absolute():
        skill_abs = (run_abs.parent / skill_value).resolve(strict=False)
        if inside(output_abs, skill_abs):
            raise ToolkitError("evaluate 输出不能写入或覆盖 skill 源目录")
    runs = plan.get("runs")
    if isinstance(runs, list):
        for record in runs:
            if not isinstance(record, dict):
                continue
            response_value = record.get("response_path")
            if isinstance(response_value, str) and response_value.strip() and not Path(response_value).is_absolute():
                if output_abs == (run_abs.parent / response_value).resolve(strict=False):
                    raise ToolkitError("evaluate 输出不能覆盖 response 证据文件")
            turn_evidence = record.get("turn_evidence")
            if isinstance(turn_evidence, list):
                for evidence in turn_evidence:
                    if not isinstance(evidence, dict):
                        continue
                    turn_response = evidence.get("response_path")
                    if (
                        isinstance(turn_response, str)
                        and turn_response.strip()
                        and not Path(turn_response).is_absolute()
                        and output_abs == (run_abs.parent / turn_response).resolve(strict=False)
                    ):
                        raise ToolkitError("evaluate 输出不能覆盖逐轮 response 证据文件")


def command_evaluate(args: argparse.Namespace) -> int:
    run_path = Path(args.run)
    output_path = Path(args.output)
    protect_evaluation_sources(run_path, output_path)
    report = evaluate_run(run_path)
    if args.stdout_json:
        emit_stdout_json(report)
    else:
        write_json(output_path, report)
        print(f"evaluate: {report['status']} -> {args.output}")
    return 0 if report["status"] == "pass" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="离线审计个人技能，并规划/评估多轮 baseline 与 candidate 实验。不会调用模型或外部服务。"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit_parser = subparsers.add_parser("audit", help="结构、引用、便携性和静态密钥形状审计")
    audit_parser.add_argument("skill_dir", help="技能目录（必须包含 SKILL.md）")
    audit_parser.add_argument("--output", required=True, help="审计报告 JSON 路径")
    audit_parser.add_argument("--stdout", dest="stdout_json", action="store_true", help="仅向 stdout 输出完整 JSON，不写文件")
    audit_parser.set_defaults(handler=command_audit)
    plan_parser = subparsers.add_parser("plan", help="验证 suite 并生成未执行的多轮计划")
    plan_parser.add_argument("suite", help="实验 suite JSON 路径")
    plan_parser.add_argument("--skill", required=True, help="候选技能目录")
    plan_parser.add_argument("--output", required=True, help="新 run JSON 路径；不会覆盖已有文件")
    plan_parser.add_argument("--rounds", type=int, default=2, help="每个 case、每个 variant 的轮数（默认 2）")
    plan_parser.add_argument(
        "--variants",
        nargs="+",
        choices=VARIANTS,
        default=list(VARIANTS),
        help="要执行的 variant（默认 baseline candidate；可仅选 candidate）",
    )
    plan_parser.add_argument("--stdout", dest="stdout_json", action="store_true", help="仅向 stdout 输出完整 JSON，不写文件")
    plan_parser.set_defaults(handler=command_plan)
    evaluate_parser = subparsers.add_parser("evaluate", help="验证散列并评估已执行响应")
    evaluate_parser.add_argument("run", help="已填写执行状态和 response_path 的 run JSON")
    evaluate_parser.add_argument("--output", required=True, help="评估报告 JSON 路径")
    evaluate_parser.add_argument("--stdout", dest="stdout_json", action="store_true", help="仅向 stdout 输出完整 JSON，不写文件")
    evaluate_parser.set_defaults(handler=command_evaluate)
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (ToolkitError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
