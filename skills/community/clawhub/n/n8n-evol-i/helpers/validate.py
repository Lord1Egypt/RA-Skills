#!/usr/bin/env python3
"""Structural validation for a workflow template or generated JSON."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.placeholder import validator as placeholder_validator


_JS_PLACEHOLDER_RE = re.compile(r"\{\{(?:INTERPOLATE_|@)js:([^}]+)\}\}")
_PY_PLACEHOLDER_RE = re.compile(r"\{\{(?:INTERPOLATE_|@)py:([^}]+)\}\}")
_JS_TRAILER_REQUIRED = 'if (typeof module !== "undefined")'
_PRIMITIVE_MARKER = "// @n8n-evol-I:primitive"

_JS_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_JS_TOP_LEVEL_KEYWORDS = ("function", "async function", "module.exports", "exports.")
_JS_TRAILER_PREFIX = 'if (typeof module !== "undefined")'

_PY_TOP_LEVEL_KEYWORDS = ("def ", "async def ", "import ", "from ")


def _walk_js_line(line: str, start_depth: int) -> int:
    """Walk a JS line char-by-char, tracking brace depth while ignoring strings + // comments."""
    depth = start_depth
    i = 0
    n = len(line)
    in_string: str | None = None  # quote char that opened the active string
    while i < n:
        c = line[i]
        if in_string:
            if c == "\\":
                i += 2
                continue
            if c == in_string:
                in_string = None
        else:
            if c in ('"', "'", "`"):
                in_string = c
            elif c == "/" and i + 1 < n and line[i + 1] == "/":
                break  # rest of the line is a // comment
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
        i += 1
    return depth


def _js_top_level_allowed(stripped: str) -> bool:
    """Is this stripped, non-blank, depth-0 JS line one of the allowed top-level shapes?"""
    if stripped.startswith("//"):
        return True
    if stripped.startswith("*") or stripped.startswith("/*"):
        # Block-comment fragments (after stripping); treat residual fragments as benign.
        return True
    if stripped.startswith(_JS_TRAILER_PREFIX):
        return True
    if stripped.startswith("function ") or stripped.startswith("function("):
        return True
    if stripped.startswith("async function "):
        return True
    if stripped.startswith("module.exports") or stripped.startswith("exports."):
        return True
    return False


def _js_top_level_violations(text: str) -> list[tuple[int, str]]:
    """Return [(line_no, excerpt), ...] for every JS line that introduces non-function code at depth 0."""
    text = _JS_BLOCK_COMMENT_RE.sub("", text)
    violations: list[tuple[int, str]] = []
    depth = 0
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if depth == 0 and stripped and not _js_top_level_allowed(stripped):
            violations.append((line_no, stripped[:80]))
        depth = _walk_js_line(line, depth)
    return violations


def _py_top_level_allowed(stripped: str) -> bool:
    """Is this stripped, non-blank, column-0 Python line one of the allowed top-level shapes?"""
    if stripped.startswith("#"):
        return True
    for kw in _PY_TOP_LEVEL_KEYWORDS:
        if stripped.startswith(kw):
            return True
    return False


def _py_top_level_violations(text: str) -> list[tuple[int, str]]:
    """Return [(line_no, excerpt), ...] for every column-0 Python line that introduces code outside def/import.

    The first non-blank, non-comment line may be a module-level docstring (a triple-quoted string
    literal); it is consumed without violation. Bare strings anywhere else at top-level are
    violations.
    """
    lines = text.splitlines()
    skip_until = _consume_module_docstring(lines)

    violations: list[tuple[int, str]] = []
    in_triple: str | None = None  # '"""' or "'''" if currently inside a multi-line string, else None
    for idx, line in enumerate(lines):
        line_no = idx + 1
        if idx < skip_until:
            continue
        if in_triple is not None:
            if in_triple in line:
                in_triple = None
            continue
        stripped = line.strip()
        if not stripped:
            continue
        # Detect a triple-quote opener that doesn't close on the same line.
        for quote in ('"""', "'''"):
            if stripped.startswith(quote):
                rest = stripped[len(quote):]
                if quote not in rest:
                    in_triple = quote
                # Either way, this line is a string expression at top level — reject it.
                indent = len(line) - len(line.lstrip(" \t"))
                if indent == 0:
                    violations.append((line_no, stripped[:80]))
                break
        else:
            indent = len(line) - len(line.lstrip(" \t"))
            if indent == 0 and not _py_top_level_allowed(stripped):
                violations.append((line_no, stripped[:80]))
    return violations


def _consume_module_docstring(lines: list[str]) -> int:
    """Return the index of the first line AFTER any leading module docstring.

    Skips leading blank/comment lines. If the first real line opens with a triple-quoted string,
    consumes through the matching closer and returns the index past it. Otherwise returns 0.
    """
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        break
    if i >= len(lines):
        return 0
    first = lines[i].strip()
    for quote in ('"""', "'''"):
        if first.startswith(quote):
            rest = first[len(quote):]
            if quote in rest:
                return i + 1
            j = i + 1
            while j < len(lines):
                if quote in lines[j]:
                    return j + 1
                j += 1
            return j
    return 0


def _validate_code_node(
    node: dict,
    index: int,
    workspace: Path | None,
) -> list[str]:
    """Return discipline errors for a single n8n-nodes-base.code node (template only)."""
    errors: list[str] = []
    name = node.get("name", f"node[{index}]")
    params = node.get("parameters", {}) or {}

    lang = params.get("language", "javascript")
    if lang == "python":
        code_field_name = "pythonCode"
        ext = "py"
        placeholder_re = _PY_PLACEHOLDER_RE
        test_filename = lambda stem: f"test_{stem}.py"
    else:
        code_field_name = "jsCode"
        ext = "js"
        placeholder_re = _JS_PLACEHOLDER_RE
        test_filename = lambda stem: f"{stem}.test.js"

    code_field = params.get(code_field_name, "")
    if code_field.lstrip().startswith(_PRIMITIVE_MARKER):
        return []  # primitive — exempt from pure-function discipline
    if not code_field:
        errors.append(f"node '{name}': {code_field_name} is empty or missing")
        return errors

    m = placeholder_re.search(code_field)
    if not m:
        errors.append(
            f"node '{name}': no {{{{@{ext}:...}}}} placeholder found in {code_field_name}. "
            f"Extract the pure function to n8n-functions/{ext}/<name>.{ext} and add the placeholder."
        )
        return errors

    if workspace is None:
        return errors

    rel_path = m.group(1).strip()
    fn_file = workspace / rel_path
    if not fn_file.exists():
        errors.append(f"node '{name}': referenced file not found: {rel_path}")
        return errors

    fn_stem = fn_file.stem

    fn_text = fn_file.read_text(encoding="utf-8")

    if ext == "js":
        if _JS_TRAILER_REQUIRED not in fn_text:
            errors.append(
                f"node '{name}': {rel_path} missing required export trailer "
                f'`if (typeof module !== "undefined") module.exports = {{ <fnName> }};` — '
                "without it, n8n-functions-tests/<name>.test.js cannot import the function."
            )
        for line_no, excerpt in _js_top_level_violations(fn_text):
            errors.append(
                f"node '{name}': {rel_path} contains top-level code outside function declarations "
                f"(line {line_no}: {excerpt!r}). Pure-function files must declare functions only — "
                "n8n-glue belongs in the Code-node body, not the file."
            )
    else:
        for line_no, excerpt in _py_top_level_violations(fn_text):
            errors.append(
                f"node '{name}': {rel_path} contains top-level code outside function declarations "
                f"(line {line_no}: {excerpt!r}). Pure-function files must declare functions only — "
                "n8n-glue belongs in the Code-node body, not the file."
            )

    test_file = workspace / "n8n-functions-tests" / test_filename(fn_stem)
    if not test_file.exists():
        errors.append(
            f"node '{name}': missing test file {test_file.relative_to(workspace)}. "
            "Create it before deploying."
        )

    return errors


def validate_workflow_json(
    text: str,
    source: str = "template",
    workspace: Path | None = None,
) -> tuple[bool, list[str]]:
    """Run structural REST validation. Returns (is_valid, errors)."""
    errors: list[str] = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return (False, [f"JSON parse error: {e}"])

    if not isinstance(data, dict):
        return (False, ["top-level value is not a JSON object"])

    if "nodes" not in data:
        errors.append("missing top-level 'nodes' key")
    elif not isinstance(data["nodes"], list):
        errors.append("'nodes' must be a list")
    else:
        for i, node in enumerate(data["nodes"]):
            if not isinstance(node, dict):
                errors.append(f"node {i} is not an object")
                continue
            for required in ("name", "type", "parameters"):
                if required not in node:
                    errors.append(f"node {i} missing '{required}'")

    if "connections" not in data:
        errors.append("missing top-level 'connections' key")
    elif not isinstance(data["connections"], dict):
        errors.append("'connections' must be an object keyed by node name")

    if source == "template":
        if "pinData" in data and data["pinData"]:
            errors.append("template contains pinData (forbidden in templates)")

        for i, node in enumerate(data.get("nodes", [])):
            if not isinstance(node, dict):
                continue
            ntype = node.get("type", "")
            name = node.get("name", f"node[{i}]")
            if ntype == "n8n-nodes-base.function":
                errors.append(
                    f"node '{name}': n8n-nodes-base.function is deprecated and forbidden; "
                    "use n8n-nodes-base.code"
                )
                continue
            if ntype == "n8n-nodes-base.code":
                errors.extend(_validate_code_node(node, i, workspace))

    if source == "built":
        residuals = placeholder_validator.check_residuals(text)
        if residuals:
            errors.append(f"residual placeholders in built JSON: {residuals}")

    return (len(errors) == 0, errors)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--env", default=None)
    parser.add_argument("--source", choices=("built", "template"), default=None,
                        help="Default: 'built' if --env given, else 'template'")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    source = args.source or ("built" if args.env else "template")

    if source == "built":
        if not args.env:
            print("ERROR: --source built requires --env", file=sys.stderr)
            sys.exit(2)
        path = ws / "n8n-build" / args.env / f"{args.workflow_key}.generated.json"
    else:
        path = ws / "n8n-workflows-template" / f"{args.workflow_key}.template.json"

    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    valid, errors = validate_workflow_json(text, source=source, workspace=ws)
    print(json.dumps({"valid": valid, "source": source, "path": str(path), "errors": errors}, indent=2))
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
