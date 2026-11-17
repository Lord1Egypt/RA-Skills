#!/usr/bin/env python3
"""校验 iterate-skill 相关文件。

用法：
    python scripts/validate.py decisions <path-to-.iterate_decisions.md> [<dimensions-dir>]
    python scripts/validate.py config <path-to-iterate.config.yaml> [<schema-path> [<dimensions-dir>]]
    python scripts/validate.py dimensions <path-to-config/dimensions>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_DECISION_SECTIONS = [
    "Atomic Fixes (Direct)",
    "Architectural Fixes (Approved + Executed)",
    "Architectural Fixes (Deferred to Next Round)",
    "AI Important Decisions",
    "Validation",
]

CONFLICT_MARKERS = ["<<<<<<<", "=======", ">>>>>>>"]

# Canonical shell-chaining metacharacters rejected in command bodies and
# whitelist entries. Shared (via this module) with iterate_cli.doctor and
# iterate_cli.personalize — the exact character set is locked by tests and
# must NOT be changed without updating all three modules together.
_COMMAND_METACHARS = set(';|&$`><\r\n\\#*?~"\'\u007b\u007d()[]')

DEFAULT_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "config" / "config.schema.json"


# Where per-dimension default focus prompts live, used to catch off-catalog
# scope redefinitions that merely parrot a preset prompt instead of writing an
# independent rationale.
DEFAULT_DIMENSIONS_DIR = Path(__file__).resolve().parent.parent / "config" / "dimensions"


def validate_decisions(path: Path, dimensions_dir: Path | None = None) -> list[str]:
    """校验 .iterate_decisions.md 格式是否合规。

    Args:
        path: Path to the decision log.
        dimensions_dir: Optional dir of ``<dim>.yaml`` files whose ``focus``
            text is used to detect off-catalog scope redefinitions that just
            copy the default prompt. Defaults to ``config/dimensions``.
    """
    errors: list[str] = []
    resolved_dimensions_dir = dimensions_dir or DEFAULT_DIMENSIONS_DIR

    if not path.exists():
        errors.append(f"File not found: {path}")
        return errors

    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"Cannot read file: {exc}")
        return errors

    for marker in CONFLICT_MARKERS:
        if marker in content:
            errors.append(f"Unresolved git conflict marker found: {marker}")

    for section in REQUIRED_DECISION_SECTIONS:
        if section not in content:
            errors.append(f"Missing section: {section}")

    # Tolerate the em-dash "—", a hyphen, or no separator after the round
    # header so minor typographic drift in the log template does not cause a
    # false "no round headers" failure.
    round_headers = re.findall(r"^## Round (\d+|\{N\})(?:[\s\u2014-]+|$)", content, re.MULTILINE)
    if not round_headers:
        errors.append("No round headers found (expected '## Round N — ...')")

    errors.extend(_validate_scope_redefinitions(content, resolved_dimensions_dir))

    return errors


# Header title of the optional off-catalog scope-redefinition table block.
_REDEFINITION_HEADER = "### Scope Dimension Redefinition (on-the-fly)"
_ORIGIN_MARKERS = ["**Origin scope:**", "Origin scope:"]

_HEADER_SPLIT_RE = re.compile(r"\s*\|\s*")


def _load_dimension_focuses(dimensions_dir: Path) -> dict[str, str]:
    """Map dimension id -> normalized default focus text."""
    focuses: dict[str, str] = {}
    if not dimensions_dir.is_dir():
        return focuses
    for yaml_file in sorted(dimensions_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, yaml.YAMLError):
            continue
        if isinstance(data, dict) and isinstance(data.get("focus"), str):
            focuses[yaml_file.stem] = _normalize_focus(data["focus"])
    return focuses


def _normalize_focus(text: str) -> str:
    """Whitespace/case/punctuation-insensitive comparison key for a prompt."""
    return " ".join(text.split()).strip().rstrip(".,").lower()


def _sections_for_redefinition(content: str) -> list[str]:
    """Extract every block under a Scope Dimension Redefinition header."""
    blocks: list[str] = []
    for match in re.finditer(rf"^{re.escape(_REDEFINITION_HEADER)}\s*$", content, re.MULTILINE):
        start = match.end()
        # Cut at the next markdown header of equal or higher level. ``start`` is
        # an offset into ``content`` (match.end()), so slice from ``start``
        # directly; the previous ``content[match.start():][start:]`` double
        # counted the offset because the second ``[start:]`` applied to the
        # already-shortened substring, potentially skipping a block-internal
        # header and letting the block bleed past its intended end.
        stop = len(content)
        for hmm in re.finditer(r"^## |^### ", content[start:], re.MULTILINE):
            stop = start + hmm.start()
            break
        blocks.append(content[match.start():stop])
    return blocks


def _validate_scope_redefinitions(content: str, dimensions_dir: Path) -> list[str]:
    """Check off-catalog scope redefinition records carry an independent reason.

    The block (only present when an off-catalog scope was redefined on the
    fly) must state an Origin scope, list at least one dimension row, and give
    every dimension a non-empty "Independent reason" that is not just a copy of
    that dimension's default ``focus`` prompt. This machine check backs the
    SKILL.md Phase 0 rule that forbids lazily recycling the preset dimensions.
    """
    errors: list[str] = []
    if _REDEFINITION_HEADER not in content:
        return errors

    focuses = _load_dimension_focuses(dimensions_dir)

    for block in _sections_for_redefinition(content):
        if not any(marker in block for marker in _ORIGIN_MARKERS):
            errors.append(
                f"{_REDEFINITION_HEADER}: missing 'Origin scope:' line "
                "(must name the redefined scope)"
            )
        origin_matches = [m for m in _ORIGIN_MARKERS if m in block]
        for marker in origin_matches:
            rest = block.split(marker, 1)[1].splitlines()
            if not rest or not rest[0].strip():
                errors.append(f"{_REDEFINITION_HEADER}: empty Origin scope")

        # Find a table header row mentioning Dimension and Reason.
        table_header_idx = None
        for i, line in enumerate(block.splitlines()):
            cells = [c.strip() for c in _HEADER_SPLIT_RE.split(line.strip())[1:-1]]
            if len(cells) >= 2 and any(c.lower() == "dimension" for c in cells) and any(
                "reason" in c.lower() for c in cells
            ):
                table_header_idx = i
                break
        if table_header_idx is None:
            errors.append(
                f"{_REDEFINITION_HEADER}: expected a table with 'Dimension' and "
                "'Independent reason' columns"
            )
            continue

        rows = 0
        for line in block.splitlines()[table_header_idx + 1 :]:
            if not line.strip().startswith("|") or set(line.replace("|", "").strip()) <= {"-", ":", " "}:
                continue  # skip the |---| separator and non-row lines
            cells = [c.strip() for c in _HEADER_SPLIT_RE.split(line.strip())[1:-1]]
            if len(cells) < 2:
                continue
            rows += 1
            dim, reason = cells[0], cells[1]
            if not dim:
                errors.append(f"{_REDEFINITION_HEADER}: row #{rows} has an empty dimension")
                continue
            if not reason:
                errors.append(f"{_REDEFINITION_HEADER}: row '#{rows}' for '{dim}' has no reason")
                continue
            default = focuses.get(dim)
            if default and _normalize_focus(reason) == default:
                errors.append(
                    f"{_REDEFINITION_HEADER}: reason for '{dim}' merely copies its default "
                    "focus prompt — write an independent scope-specific rationale"
                )
        if rows == 0:
            errors.append(
                f"{_REDEFINITION_HEADER}: section declares a redefinition but lists no dimension rows"
            )

    return errors


def load_schema(schema_path: Path) -> dict[str, Any]:
    """加载 JSON Schema 文件。

    Raises:
        FileNotFoundError: 若 schema 文件不存在。
        ValueError: 若 schema 文件内容不是合法 JSON，或不是 UTF-8 编码。
    """
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    try:
        text = schema_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        # A schema saved as GBK/Latin-1 is a real condition a user hits, not a
        # crash: report it as a schema problem so the caller degrades the same
        # way it does for malformed JSON, instead of dumping a traceback.
        raise ValueError(
            f"Schema file {schema_path} is not valid UTF-8: {exc}"
        ) from exc
    except OSError as exc:
        raise ValueError(f"Schema file {schema_path} could not be read: {exc}") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in schema file {schema_path}: {exc}") from exc


def validate_config_against_schema(
    config: dict[str, Any], schema: dict[str, Any]
) -> list[str]:
    """使用 jsonschema 校验配置。"""
    try:
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError
    except ImportError as exc:  # pragma: no cover - dependency guard
        return [f"jsonschema is required for schema validation: {exc}"]

    errors: list[str] = []
    try:
        validator = Draft202012Validator(schema)
        for error in validator.iter_errors(config):
            path = "/".join(str(part) for part in error.path) or "<root>"
            errors.append(f"Schema error at {path}: {error.message}")
    except SchemaError as exc:
        # A structurally invalid schema (bad $defs/$ref or wrong types in the
        # schema itself) would otherwise crash with an uncaught traceback.
        errors.append(f"Invalid JSON Schema (schema file itself is broken): {exc}")
    except Exception as exc:  # noqa: BLE001 - jsonschema wraps unresolved $ref lazily in non-SchemaError types
        # jsonschema raises unresolvable $ref/$def references as a wrapping
        # (non-SchemaError) error, surfaced lazily *during* iteration — the
        # broken-schema diagnostic must swallow those too, not crash.
        errors.append(f"Invalid JSON Schema (schema file itself is broken): {exc}")
    return errors


def command_is_whitelisted(command: str, whitelist: list[str]) -> bool:
    """检查命令是否以白名单中的某个前缀开头，并且前缀后必须是空白或字符串结尾。

    同时拒绝命令本体中的 shell 链接元字符（分号、竖线、与号、美元符、反引号
    换行等），防止 ``pytest tests/; rm -rf /`` 这类以白名单前缀开头、后缀拼接
    恶意命令的方式绕过白名单。

    命令所需的常用字符（字母、数字、下划线、连字符、点、斜杠、空格、``@``/``:``
    及 flag 常见字符如 ``-`` ``=``）一律放行；仅对真正的元字符强制拒绝。
    """
    stripped = command.strip()
    # Reject any shell-chaining metacharacter anywhere in the command body.
    for ch in stripped:
        if ch in _COMMAND_METACHARS:
            return False
    for prefix in whitelist:
        # Guard against non-string entries (e.g. a stray int in a hand-edited
        # command_whitelist): skip them instead of crashing on len()/startswith.
        if not isinstance(prefix, str):
            continue
        if stripped == prefix:
            return True
        if (
            len(stripped) > len(prefix)
            and stripped.startswith(prefix)
            and stripped[len(prefix)].isspace()
        ):
            return True
    return False


def whitelist_rejection_reason(command: str, whitelist: list[str]) -> str:
    """解释 ``command`` 被白名单拒绝的原因，用于错误消息。

    只改进诊断信息，不改变 ``command_is_whitelisted`` 的判定（字符集由
    ``_COMMAND_METACHARS`` 固定，tests 锁定其与 doctor/personalize 三方同步）。
    """
    stripped = command.strip()
    for ch in stripped:
        if ch in _COMMAND_METACHARS:
            return "contains shell metacharacters"
    if not whitelist:
        return "no whitelist prefixes are configured"
    return "no whitelist prefix matches"


def validate_command_whitelist(config: dict[str, Any]) -> list[str]:
    """校验 validation.commands / invariants.commands 中的命令是否安全。

    同时校验白名单条目本身不含 shell 特殊字符（; | & $ ` 等），
    避免恶意白名单条目绕过前缀匹配。

    白名单是配置期校验用的可选字段（schema 非必填、doctor 按可选处理，
    运行时只信任 validation.commands）：
    - **元字符安全网恒生效**：无论是否配置 command_whitelist，validation 与
      invariants 的命令一律拒绝 shell 链式元字符（与 doctor 一致）。
    - 未配置 command_whitelist：跳过白名单前缀匹配，元字符安全网仍生效。
    - 已配置：必须是非空列表，条目须安全，且每条 validation.commands /
      invariants.commands 必须以白名单前缀匹配。
    """
    errors: list[str] = []
    validation = config.get("validation", {})

    if not isinstance(validation, dict):
        errors.append("validation must be a mapping")
        return errors

    whitelist = validation.get("command_whitelist")
    commands_by_module = validation.get("commands", {})

    # Standalone metachar safety net — ALWAYS runs, independent of the optional
    # whitelist (mirrors iterate_cli.doctor._check_commands_metachars). A config
    # without command_whitelist must still reject shell-chaining metacharacters,
    # so a hand-edited config cannot smuggle chained commands into executable
    # validation/invariant commands.
    errors.extend(_check_metachars(commands_by_module, "validation"))
    invariants = config.get("invariants")
    if isinstance(invariants, dict) and invariants.get("commands") is not None:
        errors.extend(_check_metachars(invariants.get("commands"), "invariants"))

    if whitelist is None:
        # 白名单未配置：视为可选，跳过白名单前缀匹配；元字符安全网（上方）
        # 仍然生效（与 doctor/schema 一致）。
        return errors

    if not isinstance(whitelist, list) or not whitelist:
        errors.append("validation.command_whitelist must be a non-empty list")
        return errors

    if not isinstance(commands_by_module, dict):
        errors.append("validation.commands must be a mapping")
        return errors

    # Validate whitelist entries: only allow alphanumeric, dash, underscore,
    # dot, and space (for multi-word commands like "npm run").
    # This prevents shell metacharacter injection via whitelist entries.
    _WHITELIST_ENTRY_PATTERN = re.compile(r"^[A-Za-z0-9_. -]+$")
    # Keep only the entries that survive the safety check so commands are only
    # matched against trustworthy prefixes; bad entries are reported and dropped.
    safe_whitelist: list[str] = []
    for idx, entry in enumerate(whitelist):
        # Strip before BOTH the syntax check and the prefix match, mirroring
        # iterate_cli.doctor._check_whitelist_compliance: " pytest " is
        # syntactically valid but never prefix-matches a real command
        # un-stripped, so the two gates used to reach opposite verdicts for
        # one config (doctor: compliant / validate.py: rejects everything).
        stripped = entry.strip() if isinstance(entry, str) else entry
        if isinstance(entry, str) and stripped and _WHITELIST_ENTRY_PATTERN.match(stripped):
            safe_whitelist.append(stripped)
        elif isinstance(entry, str) and _WHITELIST_ENTRY_PATTERN.match(entry):
            # Space-only entry: syntactically valid, but an empty prefix would
            # make every command "whitelisted" — reject instead of trusting it.
            errors.append(
                f"validation.command_whitelist[{idx}] is empty after stripping: {entry!r}"
            )
        else:
            errors.append(
                f"validation.command_whitelist[{idx}] contains unsafe characters: {entry!r}"
            )

    errors.extend(
        _validate_commands_section(commands_by_module, safe_whitelist, "validation")
    )
    # v3.0 defensive mode: invariants.commands must share the SAME config-time
    # safety baseline (design §6). Absent/malformed invariants is tolerated here
    # (schema covers its structure); a malformed invariants.commands mapping is
    # still checked when it is a dict.
    if isinstance(invariants, dict) and invariants.get("commands") is not None:
        errors.extend(
            _validate_commands_section(
                invariants.get("commands"), safe_whitelist, "invariants"
            )
        )

    return errors


def _check_metachars(commands_by_module: Any, section: str) -> list[str]:
    """Reject any configured command containing shell-chaining metacharacters.

    This is the standalone safety net for configs without a
    ``command_whitelist``: metacharacters that allow command chaining
    (``;`` ``|`` ``&`` ``$`` ...) are rejected regardless of any whitelist, so
    a hand-edited config cannot smuggle side effects into the executable
    validation/invariant commands. Shared semantics with
    ``iterate_cli.doctor._check_commands_metachars``.

    Args:
        commands_by_module: A ``commands`` mapping from a config section.
        section: Config section label for error messages (``validation`` /
            ``invariants``).

    Returns:
        A list of human-readable validation errors (empty when all pass).
    """
    errors: list[str] = []
    if not isinstance(commands_by_module, dict):
        return errors
    for module, cmds in commands_by_module.items():
        if not isinstance(cmds, list):
            continue
        for idx, command in enumerate(cmds):
            if isinstance(command, str) and any(ch in _COMMAND_METACHARS for ch in command):
                errors.append(
                    f"{section}.commands.{module}[{idx}] contains shell metacharacter(s): {command!r}"
                )
    return errors


def _validate_commands_section(
    commands_by_module: Any, safe_whitelist: list[str], section: str
) -> list[str]:
    """Validate a per-module command mapping against the safe whitelist.

    Shared by ``validation.commands`` and (v3.0) ``invariants.commands`` so both
    go through the same config-time safety baseline: commands must be lists of
    strings and every command must match a whitelist prefix (when the whitelist
    is configured).

    Args:
        commands_by_module: The ``commands`` mapping from a config section.
        safe_whitelist: Whitelist entries that survived the metacharacter check.
        section: Config section label for error messages (``validation`` /
            ``invariants``).

    Returns:
        A list of human-readable validation errors (empty when all pass).
    """
    errors: list[str] = []
    if not isinstance(commands_by_module, dict):
        return errors
    for module, commands in commands_by_module.items():
        if not isinstance(commands, list):
            errors.append(f"{section}.commands.{module} must be a list")
            continue
        for idx, command in enumerate(commands):
            if not isinstance(command, str):
                errors.append(f"{section}.commands.{module}[{idx}] must be a string")
                continue
            if not command_is_whitelisted(command, safe_whitelist):
                reason = whitelist_rejection_reason(command, safe_whitelist)
                errors.append(
                    f"{section}.commands.{module}[{idx}] is not in command_whitelist: "
                    f"{command!r} ({reason})"
                )
    return errors


DIMENSION_REQUIRED_FIELDS = ["name", "name_en", "priority", "focus"]
DIMENSION_PRIORITY_VALUES = {"critical", "high", "medium", "low"}


def validate_dimensions(path: Path) -> list[str]:
    """校验 config/dimensions/*.yaml 每个维度文件格式是否合规。"""
    errors: list[str] = []

    if not path.exists():
        errors.append(f"Directory not found: {path}")
        return errors

    if not path.is_dir():
        errors.append(f"Path is not a directory: {path}")
        return errors

    yaml_files = sorted(path.glob("*.yaml"))
    if not yaml_files:
        errors.append("No dimension YAML files found")
        return errors

    for file_path in yaml_files:
        try:
            data = yaml.safe_load(file_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"Invalid YAML in {file_path.name}: {exc}")
            continue
        except (OSError, UnicodeDecodeError) as exc:
            # A non-UTF-8 or otherwise unreadable file must be reported as an
            # error, not crash the whole validation run with a traceback.
            errors.append(f"Could not read {file_path.name}: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{file_path.name} must be a YAML mapping")
            continue

        for field in DIMENSION_REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"{file_path.name} missing required field: {field}")
                continue
            if not isinstance(data[field], str):
                errors.append(f"{file_path.name} field {field} must be a string")
                continue
            if field == "priority" and data[field] not in DIMENSION_PRIORITY_VALUES:
                errors.append(
                    f"{file_path.name} field priority must be one of "
                    f"{sorted(DIMENSION_PRIORITY_VALUES)}, got {data[field]!r}"
                )

    return errors


def validate_dimension_sets(
    config: dict[str, Any], schema_path: Path | None = None
) -> list[str]:
    """校验 dimension_sets 段的语义一致性。

    检查：
    - 每个命名集必须是 mapping，含非空 ``dimensions`` 列表且维度在 schema enum 内。
    - ``focus`` 的键必须是该集 ``dimensions`` 中的维度（否则是死配置）。
    - 集名只能含字母/数字/下划线/点/连字符（与 schema propertyNames、TOC 锚点安全一致）。

    ``schema_path`` must be the same schema ``validate_config`` was given:
    the enum used to be loaded from the repo default even when the caller
    validated against a custom schema, so a custom dimension was reported as
    unknown. ``None`` keeps the default-schema behaviour for direct callers.
    """
    errors: list[str] = []
    raw = config.get("dimension_sets")
    if raw is None:
        return errors
    if not isinstance(raw, dict):
        errors.append("dimension_sets must be a mapping")
        return errors

    enum = _dimension_enum_from_schema(load_schema_or_none(schema_path))
    for name, spec in raw.items():
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            errors.append(f"dimension_sets key {name!r} must only contain letters, digits, underscore, dot, dash")
            continue
        if not isinstance(spec, dict):
            errors.append(f"dimension_sets.{name} must be a mapping")
            continue
        dims = spec.get("dimensions")
        if not isinstance(dims, list) or not dims:
            errors.append(f"dimension_sets.{name}.dimensions must be a non-empty list")
            dims = []
        if not all(isinstance(d, str) for d in dims):
            errors.append(f"dimension_sets.{name}.dimensions must be a list of strings")
        if enum is not None:
            for d in dims:
                if isinstance(d, str) and d not in enum:
                    errors.append(f"dimension_sets.{name}.dimensions has unknown dimension {d!r}")
        seen = {d for d in dims if isinstance(d, str)}
        focus = spec.get("focus")
        if focus is not None:
            if not isinstance(focus, dict):
                errors.append(f"dimension_sets.{name}.focus must be a mapping")
            else:
                for dim, text in focus.items():
                    if dim not in seen:
                        errors.append(f"dimension_sets.{name}.focus[{dim}] references a dimension not in this set")
                    if not isinstance(text, str) or not text.strip():
                        errors.append(f"dimension_sets.{name}.focus[{dim}] must be a non-empty string")
    return errors


def load_schema_or_none(schema_path: Path | None = None) -> dict[str, Any] | None:
    """Load a schema, returning None on any failure (validation best-effort)."""
    try:
        return load_schema(schema_path or DEFAULT_SCHEMA_PATH)
    except (FileNotFoundError, ValueError):
        return None


def _dimension_enum_from_schema(schema: dict[str, Any]) -> set[str] | None:
    """从 JSON Schema 中提取 dimensions 的允许取值。

    支持两种写法：
    - inline enum: {"items": {"type": "string", "enum": [...]}}
    - $ref: {"items": {"$ref": "#/$defs/dimension"}}，从 $defs 解析。
    """
    try:
        items = schema["properties"]["dimensions"]["items"]
        # Inline enum.
        enum = items.get("enum")
        if isinstance(enum, list):
            return set(enum)
        # $ref to $defs/dimension.
        ref = items.get("$ref", "")
        if ref == "#/$defs/dimension":
            defs = schema.get("$defs") or {}
            dim_def = defs.get("dimension") or {}
            ref_enum = dim_def.get("enum")
            if isinstance(ref_enum, list):
                return set(ref_enum)
    except (KeyError, TypeError):
        pass
    return None


def validate_dimension_consistency(
    dimensions_dir: Path, expected_keys: set[str]
) -> list[str]:
    """校验 dimensions 目录中的文件与 schema enum 一一对应。"""
    errors: list[str] = []

    if not dimensions_dir.exists():
        errors.append(f"Dimension directory not found: {dimensions_dir}")
        return errors

    actual_keys = {p.stem for p in dimensions_dir.glob("*.yaml")}
    missing_files = expected_keys - actual_keys
    extra_files = actual_keys - expected_keys

    for key in sorted(missing_files):
        errors.append(f"Missing dimension file for schema enum value: {key}")
    for key in sorted(extra_files):
        errors.append(f"Unexpected dimension file not in schema enum: {key}")

    return errors


def validate_personalization_consistency(config: dict[str, Any]) -> list[str]:
    """校验 personalization 段的语义一致性。

    检查：
    - fix_priority_order 中的维度应出现在 dimensions 列表中（启用的维度才有意义）。
    - dimension_focus 中的维度应出现在 dimensions 列表中。
    - known_intentional 中的维度应出现在 dimensions 列表中。
    """
    errors: list[str] = []

    personalization = config.get("personalization") or {}
    if not isinstance(personalization, dict):
        return errors

    # Non-list / non-string entries must not reach `set()`: an unhashable
    # member (nested list/dict from a hand edit) raised TypeError out of the
    # consistency checker, and a scalar string was iterated into a set of
    # single characters, producing junk "not in enabled dimensions" errors.
    # The JSON-schema pass already reports the structural problem; here we
    # only cross-check the entries that are actually dimension names.
    raw_dims = config.get("dimensions")
    if not isinstance(raw_dims, list):
        return errors
    enabled_dims = {d for d in raw_dims if isinstance(d, str)}
    if not enabled_dims:
        return errors

    # fix_priority_order: dimensions should be in enabled dimensions.
    fix_priority = personalization.get("fix_priority_order") or []
    if isinstance(fix_priority, list):
        for idx, dim in enumerate(fix_priority):
            if isinstance(dim, str) and dim not in enabled_dims:
                errors.append(
                    f"personalization.fix_priority_order[{idx}] dimension '{dim}' "
                    f"is not in enabled dimensions {sorted(enabled_dims)}"
                )

    # dimension_focus: dimensions should be in enabled dimensions.
    dim_focus = personalization.get("dimension_focus") or []
    if isinstance(dim_focus, list):
        for idx, item in enumerate(dim_focus):
            if isinstance(item, dict):
                dim = item.get("dimension", "")
                if dim and dim not in enabled_dims:
                    errors.append(
                        f"personalization.dimension_focus[{idx}] dimension '{dim}' "
                        f"is not in enabled dimensions {sorted(enabled_dims)}"
                    )

    # known_intentional: dimensions should be in enabled dimensions.
    known_intentional = personalization.get("known_intentional") or []
    if isinstance(known_intentional, list):
        for idx, item in enumerate(known_intentional):
            if isinstance(item, dict):
                dim = item.get("dimension", "")
                if dim and dim not in enabled_dims:
                    errors.append(
                        f"personalization.known_intentional[{idx}] dimension '{dim}' "
                        f"is not in enabled dimensions {sorted(enabled_dims)}"
                    )

    return errors


def validate_config(
    path: Path, schema_path: Path | None = None, dimensions_dir: Path | None = None
) -> list[str]:
    """校验 iterate.config.yaml 格式、schema 与白名单。"""
    errors: list[str] = []

    if not path.exists():
        errors.append(f"File not found: {path}")
        return errors

    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        # Reported in-band like every other config problem. Uncaught, a
        # config saved in a non-UTF-8 encoding (GBK/Shift-JIS/Latin-1) killed
        # the whole validation run with a traceback instead of naming the file.
        errors.append(f"Configuration is not valid UTF-8: {path} ({exc})")
        return errors
    except yaml.YAMLError as exc:
        errors.append(f"Invalid YAML: {exc}")
        return errors
    except OSError as exc:
        errors.append(f"Configuration could not be read: {path} ({exc})")
        return errors

    if not isinstance(config, dict):
        errors.append("Configuration must be a YAML mapping")
        return errors

    # Graceful degradation when the schema file is missing or malformed (mirrors
    # iterate_cli.doctor._load_config_schema): report the failure instead of
    # raising, and skip the schema-dependent passes while still running the
    # independent checks (whitelist / personalization / dimensions).
    try:
        schema = load_schema(schema_path or DEFAULT_SCHEMA_PATH)
    except FileNotFoundError as exc:
        errors.append(f"schema file missing: {exc}")
        schema = None
    except ValueError as exc:
        errors.append(f"invalid schema JSON: {exc}")
        schema = None

    if schema is not None:
        errors.extend(validate_config_against_schema(config, schema))
    errors.extend(validate_command_whitelist(config))
    errors.extend(validate_personalization_consistency(config))
    errors.extend(validate_dimension_sets(config, schema_path))

    resolved_dimensions_dir = dimensions_dir or (path.parent / "dimensions")
    if dimensions_dir is not None and not resolved_dimensions_dir.exists():
        # An explicitly requested directory that does not exist is a caller
        # error, not a reason to silently skip the cross-consistency checks:
        # a typo'd path used to produce a green run that validated nothing.
        errors.append(f"Dimension directory not found: {resolved_dimensions_dir}")
    elif resolved_dimensions_dir.exists():
        errors.extend(validate_dimensions(resolved_dimensions_dir))
        if schema is not None:
            expected_keys = _dimension_enum_from_schema(schema)
            if expected_keys is not None:
                errors.extend(
                    validate_dimension_consistency(resolved_dimensions_dir, expected_keys)
                )

    return errors


def print_errors(source: str, errors: list[str]) -> None:
    """统一输出错误信息到 stderr。"""
    print(f"Validation failed for {source}", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    # Force UTF-8 before emitting anything: validation messages and config
    # values routinely carry CJK/Unicode (a dimension name, a Chinese comment
    # quoted in an error), and a locale-encoded stdout (Windows cp1252, or a
    # POSIX LANG=en_US.ISO-8859-1) raises UnicodeEncodeError and aborts the
    # check with a traceback instead of a verdict. Best-effort: streams that
    # refuse to be reconfigured are left alone.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError, AttributeError):
            continue

    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 2:
        print(__doc__, file=sys.stderr)
        # Usage error → 2, matching the exit-code contract (1 = business
        # failure/"validation found problems", 2 = the invocation itself is
        # wrong and retrying without fixing it is pointless).
        return 2

    command, target_str = args[0], args[1]
    target = Path(target_str)

    if command == "decisions":
        dimensions_dir = Path(args[2]) if len(args) > 2 else None
        errors = validate_decisions(target, dimensions_dir)
    elif command == "config":
        schema_path = Path(args[2]) if len(args) > 2 else None
        dimensions_dir = Path(args[3]) if len(args) > 3 else None
        if dimensions_dir is None:
            # When no explicit dimensions dir is given, the dimension
            # cross-consistency checks silently fall back to
            # <config-dir>/dimensions (usually absent). Surface that instead
            # of letting the checks be silently skipped.
            fallback = target.parent / "dimensions"
            if not fallback.exists():
                print(
                    "note: dimension validation skipped — no dimensions dir found "
                    f"at {fallback} (pass it as the 4th argument)",
                    file=sys.stderr,
                )
        errors = validate_config(target, schema_path, dimensions_dir)
    elif command == "dimensions":
        errors = validate_dimensions(target)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return 2

    if errors:
        print_errors(str(target), errors)
        return 1

    print(f"Validation passed: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
