#!/usr/bin/env python3
"""
pre-commit-config-validator — Validate .pre-commit-config.yaml files.

Checks structure, repository entries, hook definitions, local hooks,
and best practices. Pure Python stdlib (falls back to basic YAML parser
when PyYAML is unavailable).

Exit codes: 0 = pass, 1 = errors found, 2 = parse/input error
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KNOWN_TOP_LEVEL_KEYS = {
    "repos", "default_language_version", "default_stages", "ci",
    "minimum_pre_commit_version", "exclude", "fail_fast", "files",
}

KNOWN_HOOK_KEYS = {
    "id", "name", "entry", "language", "files", "exclude", "types",
    "types_or", "stages", "additional_dependencies", "args", "always_run",
    "pass_filenames", "require_serial", "minimum_pre_commit_version",
    "verbose", "log_file", "description",
}

KNOWN_STAGES = {
    "commit", "merge-commit", "push", "prepare-commit-msg", "commit-msg",
    "post-checkout", "post-commit", "post-merge", "post-rewrite", "manual",
    "pre-push", "pre-rebase", "pre-merge-commit",
}

KNOWN_LANGUAGES = {
    "python", "node", "ruby", "rust", "golang", "docker", "docker_image",
    "dotnet", "lua", "perl", "r", "swift", "system", "pygrep", "script",
    "fail",
}

META_HOOKS = {"check-hooks-apply", "check-useless-excludes"}

BRANCH_NAMES = {"main", "master", "develop", "dev", "trunk", "HEAD"}

SEMVER_RE = re.compile(r"^v?\d+\.\d+(\.\d+)?([a-zA-Z0-9._-]*)$")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")

# ---------------------------------------------------------------------------
# Minimal YAML parser (subset needed for pre-commit configs)
# ---------------------------------------------------------------------------

class YAMLParseError(Exception):
    pass


def _strip_comment(line: str) -> str:
    """Remove trailing comments, respecting quotes."""
    in_single = False
    in_double = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            return line[:i].rstrip()
    return line.rstrip()


def _unquote(val: str) -> str:
    val = val.strip()
    if len(val) >= 2:
        if (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'"):
            return val[1:-1]
    return val


def _indent_level(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_inline_list(val: str):
    """Parse [a, b, c] style inline list."""
    val = val.strip()
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        items = []
        for part in inner.split(","):
            items.append(_unquote(part.strip()))
        return items
    return None


def _parse_inline_mapping(val: str):
    """Parse {key: val, key: val} style inline mapping."""
    val = val.strip()
    if val.startswith("{") and val.endswith("}"):
        inner = val[1:-1].strip()
        if not inner:
            return {}
        result = {}
        for part in inner.split(","):
            if ":" in part:
                k, v = part.split(":", 1)
                result[k.strip()] = _unquote(v.strip())
        return result
    return None


def _coerce_value(val: str):
    """Coerce a scalar string to Python type."""
    if val in ("true", "True", "yes", "on"):
        return True
    if val in ("false", "False", "no", "off"):
        return False
    if val in ("null", "~", ""):
        return None
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


def _basic_yaml_parse(text: str):
    """
    Minimal YAML parser sufficient for .pre-commit-config.yaml files.
    Handles nested mappings, lists of scalars/mappings, quoted strings.
    """
    lines = text.split("\n")
    # Remove full-line comments and blank lines but track indices
    cleaned = []
    for line in lines:
        stripped = line.rstrip()
        lstripped = stripped.lstrip()
        if not lstripped or lstripped.startswith("#"):
            continue
        cleaned.append(_strip_comment(stripped))

    if not cleaned:
        return {}

    def parse_block(idx, base_indent):
        """Parse a block at a given indentation level, return (result, next_idx)."""
        if idx >= len(cleaned):
            return None, idx

        line = cleaned[idx]
        indent = _indent_level(line)
        content = line.strip()

        # Detect if this block is a list or mapping
        if content.startswith("- "):
            return parse_list(idx, indent)
        else:
            return parse_mapping(idx, indent)

    def parse_list(idx, base_indent):
        result = []
        while idx < len(cleaned):
            line = cleaned[idx]
            indent = _indent_level(line)
            if indent < base_indent:
                break
            if indent > base_indent:
                break
            content = line.strip()
            if not content.startswith("- "):
                break
            item_content = content[2:].strip()

            # List item is a key: value (start of mapping)
            if ":" in item_content and not item_content.startswith("["):
                # Could be inline scalar like "- id: foo"
                # Parse as a mapping starting from this item
                mapping = {}
                k, v = item_content.split(":", 1)
                k = k.strip()
                v = v.strip()
                if v:
                    inline_list = _parse_inline_list(v)
                    if inline_list is not None:
                        mapping[k] = inline_list
                    else:
                        mapping[k] = _coerce_value(_unquote(v))
                else:
                    # Value is a nested block
                    child_indent = indent + 2  # typical
                    if idx + 1 < len(cleaned):
                        child_indent = _indent_level(cleaned[idx + 1])
                    child, idx = parse_block(idx + 1, child_indent)
                    mapping[k] = child
                    # Continue reading sibling keys at same child_indent
                    # Actually, continue reading keys at the list-item child level
                idx += 1
                # Read more keys belonging to this list-item mapping
                item_child_indent = base_indent + 2
                if idx < len(cleaned):
                    next_indent = _indent_level(cleaned[idx])
                    if next_indent > base_indent:
                        item_child_indent = next_indent
                while idx < len(cleaned):
                    nline = cleaned[idx]
                    nindent = _indent_level(nline)
                    if nindent <= base_indent:
                        break
                    ncontent = nline.strip()
                    if ncontent.startswith("- ") and nindent == base_indent:
                        break
                    if ":" in ncontent and not ncontent.startswith("[") and not ncontent.startswith("-"):
                        nk, nv = ncontent.split(":", 1)
                        nk = nk.strip()
                        nv = nv.strip()
                        if nv:
                            inline_list = _parse_inline_list(nv)
                            if inline_list is not None:
                                mapping[nk] = inline_list
                            else:
                                mapping[nk] = _coerce_value(_unquote(nv))
                            idx += 1
                        else:
                            if idx + 1 < len(cleaned) and _indent_level(cleaned[idx + 1]) > nindent:
                                child, idx = parse_block(idx + 1, _indent_level(cleaned[idx + 1]))
                                mapping[nk] = child
                            else:
                                mapping[nk] = None
                                idx += 1
                    elif ncontent.startswith("- ") and nindent > base_indent:
                        # sub-list belonging to previous key? This is tricky.
                        # Re-parse as list
                        sub_list, idx = parse_list(idx, nindent)
                        # Attach to last key
                        if mapping:
                            last_key = list(mapping.keys())[-1]
                            if mapping[last_key] is None:
                                mapping[last_key] = sub_list
                            elif isinstance(mapping[last_key], list):
                                mapping[last_key].extend(sub_list)
                            else:
                                mapping[last_key] = sub_list
                        else:
                            idx += 1
                    else:
                        idx += 1
                result.append(mapping)
            elif item_content.startswith("["):
                inline = _parse_inline_list(item_content)
                result.append(inline if inline is not None else item_content)
                idx += 1
            elif item_content == "":
                # Nested block
                if idx + 1 < len(cleaned) and _indent_level(cleaned[idx + 1]) > base_indent:
                    child, idx = parse_block(idx + 1, _indent_level(cleaned[idx + 1]))
                    result.append(child)
                else:
                    result.append(None)
                    idx += 1
            else:
                result.append(_coerce_value(_unquote(item_content)))
                idx += 1

        return result, idx

    def parse_mapping(idx, base_indent):
        result = {}
        while idx < len(cleaned):
            line = cleaned[idx]
            indent = _indent_level(line)
            if indent < base_indent:
                break
            if indent > base_indent:
                # skip unexpected indentation
                idx += 1
                continue
            content = line.strip()
            if content.startswith("- "):
                break
            if ":" not in content:
                idx += 1
                continue
            k, v = content.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v:
                inline_list = _parse_inline_list(v)
                inline_map = _parse_inline_mapping(v)
                if inline_list is not None:
                    result[k] = inline_list
                elif inline_map is not None:
                    result[k] = inline_map
                else:
                    result[k] = _coerce_value(_unquote(v))
                idx += 1
            else:
                # Check for nested block
                if idx + 1 < len(cleaned) and _indent_level(cleaned[idx + 1]) > indent:
                    child, idx = parse_block(idx + 1, _indent_level(cleaned[idx + 1]))
                    result[k] = child
                else:
                    result[k] = None
                    idx += 1
        return result, idx

    result, _ = parse_block(0, _indent_level(cleaned[0]))
    return result


def load_yaml(text: str):
    """Load YAML text: try PyYAML first, fall back to basic parser."""
    try:
        import yaml  # noqa: F811
        return yaml.safe_load(text)
    except ImportError:
        pass
    except Exception as exc:
        raise YAMLParseError(f"PyYAML parse error: {exc}") from exc

    try:
        return _basic_yaml_parse(text)
    except Exception as exc:
        raise YAMLParseError(f"YAML parse error: {exc}") from exc


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------

class Severity:
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Diagnostic:
    __slots__ = ("rule", "severity", "message", "path")

    def __init__(self, rule: str, severity: str, message: str, path: str = ""):
        self.rule = rule
        self.severity = severity
        self.message = message
        self.path = path

    def to_dict(self):
        return {
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


# ---------------------------------------------------------------------------
# Validation rules
# ---------------------------------------------------------------------------

def check_structure(config, diags: list):
    """Structure rules (S1-S5)."""
    if not isinstance(config, dict):
        diags.append(Diagnostic("S1", Severity.ERROR, "Config root is not a mapping"))
        return

    if "repos" not in config:
        diags.append(Diagnostic("S2", Severity.ERROR, "Missing required top-level key 'repos'"))
        return

    if not isinstance(config["repos"], list):
        diags.append(Diagnostic("S3", Severity.ERROR, "'repos' must be a list"))
        return

    if len(config["repos"]) == 0:
        diags.append(Diagnostic("S4", Severity.WARNING, "'repos' list is empty"))

    unknown = set(config.keys()) - KNOWN_TOP_LEVEL_KEYS
    for k in sorted(unknown):
        diags.append(Diagnostic("S5", Severity.WARNING, f"Unknown top-level key: '{k}'"))


def check_repos(config, diags: list):
    """Repository entry rules (R1-R6)."""
    if not isinstance(config, dict) or not isinstance(config.get("repos"), list):
        return

    seen_urls = Counter()
    for i, entry in enumerate(config["repos"]):
        prefix = f"repos[{i}]"
        if not isinstance(entry, dict):
            diags.append(Diagnostic("R1", Severity.ERROR, f"{prefix}: entry is not a mapping"))
            continue

        repo = entry.get("repo")
        if repo is None:
            diags.append(Diagnostic("R1", Severity.ERROR, f"{prefix}: missing 'repo' key"))
            continue

        repo_str = str(repo)

        # Track for duplicate check
        if repo_str not in ("local", "meta"):
            seen_urls[repo_str] += 1

        # Rev checks for non-local, non-meta repos
        if repo_str not in ("local", "meta"):
            rev = entry.get("rev")
            if rev is None:
                diags.append(Diagnostic("R2", Severity.ERROR,
                    f"{prefix}: missing 'rev' for repo '{repo_str}'"))
            else:
                rev_str = str(rev)
                if rev_str in BRANCH_NAMES:
                    diags.append(Diagnostic("R5", Severity.WARNING,
                        f"{prefix}: 'rev' looks like a branch name '{rev_str}' "
                        "— use a tag or SHA for reproducibility"))
                elif not SHA_RE.match(rev_str) and not SEMVER_RE.match(rev_str):
                    diags.append(Diagnostic("R6", Severity.WARNING,
                        f"{prefix}: 'rev: {rev_str}' does not look like a "
                        "semver tag or commit SHA"))

        # Hooks list
        hooks = entry.get("hooks")
        if hooks is None:
            diags.append(Diagnostic("R3", Severity.ERROR,
                f"{prefix}: missing 'hooks' list"))
        elif not isinstance(hooks, list):
            diags.append(Diagnostic("R3", Severity.ERROR,
                f"{prefix}: 'hooks' must be a list"))
        elif len(hooks) == 0:
            diags.append(Diagnostic("R4", Severity.WARNING,
                f"{prefix}: 'hooks' list is empty"))

    # Duplicate repo URLs
    for url, count in seen_urls.items():
        if count > 1:
            diags.append(Diagnostic("B3", Severity.WARNING,
                f"Duplicate repo URL '{url}' appears {count} times"))


def check_hooks(config, diags: list):
    """Hook definition rules (H1-H6)."""
    if not isinstance(config, dict) or not isinstance(config.get("repos"), list):
        return

    for i, entry in enumerate(config["repos"]):
        if not isinstance(entry, dict):
            continue
        hooks = entry.get("hooks")
        if not isinstance(hooks, list):
            continue

        repo_str = str(entry.get("repo", ""))
        seen_ids = Counter()

        for j, hook in enumerate(hooks):
            prefix = f"repos[{i}].hooks[{j}]"
            if not isinstance(hook, dict):
                diags.append(Diagnostic("H1", Severity.ERROR,
                    f"{prefix}: hook entry is not a mapping"))
                continue

            hook_id = hook.get("id")
            if hook_id is None:
                diags.append(Diagnostic("H1", Severity.ERROR,
                    f"{prefix}: missing 'id'"))
            else:
                seen_ids[str(hook_id)] += 1

            # Unknown keys
            unknown = set(hook.keys()) - KNOWN_HOOK_KEYS
            for k in sorted(unknown):
                diags.append(Diagnostic("H3", Severity.WARNING,
                    f"{prefix}: unknown hook key '{k}'"))

            # Stages validation
            stages = hook.get("stages")
            if stages is not None:
                if not isinstance(stages, list):
                    diags.append(Diagnostic("H4", Severity.ERROR,
                        f"{prefix}: 'stages' must be a list"))
                else:
                    for s in stages:
                        if str(s) not in KNOWN_STAGES:
                            diags.append(Diagnostic("H4", Severity.ERROR,
                                f"{prefix}: invalid stage '{s}'"))

            # args must be list
            args = hook.get("args")
            if args is not None and not isinstance(args, list):
                diags.append(Diagnostic("H5", Severity.ERROR,
                    f"{prefix}: 'args' must be a list, got {type(args).__name__}"))

            # additional_dependencies must be list
            deps = hook.get("additional_dependencies")
            if deps is not None and not isinstance(deps, list):
                diags.append(Diagnostic("H6", Severity.ERROR,
                    f"{prefix}: 'additional_dependencies' must be a list"))

        # Duplicate hook IDs
        for hid, count in seen_ids.items():
            if count > 1:
                diags.append(Diagnostic("H2", Severity.WARNING,
                    f"repos[{i}]: duplicate hook id '{hid}' ({count} times)"))


def check_local_hooks(config, diags: list):
    """Local hook rules (L1-L3)."""
    if not isinstance(config, dict) or not isinstance(config.get("repos"), list):
        return

    for i, entry in enumerate(config["repos"]):
        if not isinstance(entry, dict):
            continue
        if str(entry.get("repo", "")) != "local":
            continue

        hooks = entry.get("hooks")
        if not isinstance(hooks, list):
            continue

        for j, hook in enumerate(hooks):
            if not isinstance(hook, dict):
                continue
            prefix = f"repos[{i}].hooks[{j}]"

            if "entry" not in hook:
                diags.append(Diagnostic("L1", Severity.ERROR,
                    f"{prefix}: local hook missing 'entry'"))

            if "language" not in hook:
                diags.append(Diagnostic("L2", Severity.ERROR,
                    f"{prefix}: local hook missing 'language'"))
            else:
                lang = str(hook["language"])
                if lang not in KNOWN_LANGUAGES:
                    diags.append(Diagnostic("L3", Severity.WARNING,
                        f"{prefix}: unknown language '{lang}'"))


def check_best_practices(config, diags: list):
    """Best practice rules (B1-B4)."""
    if not isinstance(config, dict):
        return

    # B4: fail_fast info
    if config.get("fail_fast") is True:
        diags.append(Diagnostic("B4", Severity.INFO,
            "'fail_fast: true' — may hide issues in later hooks"))

    if not isinstance(config.get("repos"), list):
        return

    for i, entry in enumerate(config["repos"]):
        if not isinstance(entry, dict):
            continue

        repo_str = str(entry.get("repo", ""))

        # B1: meta repo without useful hooks
        if repo_str == "meta":
            hooks = entry.get("hooks")
            if isinstance(hooks, list):
                hook_ids = {str(h.get("id", "")) for h in hooks if isinstance(h, dict)}
                if not hook_ids & META_HOOKS:
                    diags.append(Diagnostic("B1", Severity.WARNING,
                        f"repos[{i}]: repo 'meta' without check-hooks-apply "
                        "or check-useless-excludes"))

        # B2: rev without semver pattern (very old format)
        if repo_str not in ("local", "meta"):
            rev = entry.get("rev")
            if rev is not None:
                rev_str = str(rev)
                if not SEMVER_RE.match(rev_str) and not SHA_RE.match(rev_str) \
                        and rev_str not in BRANCH_NAMES:
                    diags.append(Diagnostic("B2", Severity.WARNING,
                        f"repos[{i}]: rev '{rev_str}' doesn't match "
                        "semver or SHA pattern"))


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

RULE_GROUPS = {
    "validate": [check_structure, check_repos, check_hooks, check_local_hooks, check_best_practices],
    "repos":    [check_structure, check_repos],
    "hooks":    [check_structure, check_hooks, check_local_hooks],
    "lint":     [check_best_practices],
}


def run_checks(config, command: str) -> list:
    diags = []
    for fn in RULE_GROUPS.get(command, RULE_GROUPS["validate"]):
        fn(config, diags)
    return diags


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

SEVERITY_ICON = {
    Severity.ERROR: "\u2716",
    Severity.WARNING: "\u26a0",
    Severity.INFO: "\u2139",
}


def format_text(diags: list, filepath: str) -> str:
    if not diags:
        return f"\u2714 {filepath}: all checks passed"
    lines = [f"--- {filepath} ---"]
    for d in diags:
        icon = SEVERITY_ICON.get(d.severity, " ")
        lines.append(f"  {icon} [{d.rule}] {d.severity}: {d.message}")
    counts = Counter(d.severity for d in diags)
    parts = []
    for sev in (Severity.ERROR, Severity.WARNING, Severity.INFO):
        if counts[sev]:
            parts.append(f"{counts[sev]} {sev}(s)")
    lines.append(f"  Total: {', '.join(parts)}")
    return "\n".join(lines)


def format_json(diags: list, filepath: str) -> str:
    return json.dumps({
        "file": filepath,
        "diagnostics": [d.to_dict() for d in diags],
        "counts": dict(Counter(d.severity for d in diags)),
    }, indent=2)


def format_summary(diags: list, filepath: str) -> str:
    counts = Counter(d.severity for d in diags)
    total = len(diags)
    if total == 0:
        return f"{filepath}: PASS (0 issues)"
    parts = []
    for sev in (Severity.ERROR, Severity.WARNING, Severity.INFO):
        if counts[sev]:
            parts.append(f"{counts[sev]} {sev}")
    return f"{filepath}: {total} issue(s) — {', '.join(parts)}"


FORMATTERS = {
    "text": format_text,
    "json": format_json,
    "summary": format_summary,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="precommit_validator",
        description="Validate .pre-commit-config.yaml files",
    )
    p.add_argument("command", choices=["validate", "repos", "hooks", "lint"],
                    help="Validation scope")
    p.add_argument("files", nargs="+", metavar="FILE",
                    help="YAML files to validate")
    p.add_argument("--format", choices=["text", "json", "summary"],
                    default="text", dest="fmt",
                    help="Output format (default: text)")
    p.add_argument("--strict", action="store_true",
                    help="Treat warnings as errors")
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    formatter = FORMATTERS[args.fmt]

    worst = 0  # 0=ok, 1=error, 2=parse error

    for filepath in args.files:
        path = Path(filepath)
        if not path.is_file():
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            worst = max(worst, 2)
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"Error reading {filepath}: {exc}", file=sys.stderr)
            worst = max(worst, 2)
            continue

        try:
            config = load_yaml(text)
        except YAMLParseError as exc:
            diags = [Diagnostic("S1", Severity.ERROR, str(exc))]
            print(formatter(diags, filepath))
            worst = max(worst, 2)
            continue

        diags = run_checks(config, args.command)

        has_errors = any(d.severity == Severity.ERROR for d in diags)
        has_warnings = any(d.severity == Severity.WARNING for d in diags)

        if has_errors:
            worst = max(worst, 1)
        elif has_warnings and args.strict:
            worst = max(worst, 1)

        print(formatter(diags, filepath))

    return worst


if __name__ == "__main__":
    sys.exit(main())
