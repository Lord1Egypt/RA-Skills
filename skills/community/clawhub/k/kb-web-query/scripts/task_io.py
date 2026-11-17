import json
import re
import sys
from pathlib import Path


def read_payload(path=None):
    if path:
        raw = Path(path).read_bytes()
    else:
        raw = sys.stdin.buffer.read()
    if not raw.strip():
        return {}
    return json.loads(raw.decode("utf-8-sig", errors="replace"))


def read_json_file(path):
    raw = Path(path).read_bytes()
    if not raw.strip():
        return {}
    return json.loads(raw.decode("utf-8-sig", errors="replace"))




def read_json_file_lenient(path):
    raw = Path(path).read_bytes()
    if not raw.strip():
        return {}
    return parse_json_lenient(raw.decode("utf-8-sig", errors="replace"), str(path))


def parse_json_lenient(text, label="JSON"):
    clean = str(text or "").strip()
    candidates = []
    for candidate in [
        clean,
        strip_markdown_fence(clean),
        extract_json_document(strip_markdown_fence(clean)),
    ]:
        if candidate and candidate not in candidates:
            candidates.append(candidate)
        repaired = repair_common_json_issues(candidate)
        if repaired and repaired not in candidates:
            candidates.append(repaired)
        escaped = escape_control_chars_in_strings(repaired)
        if escaped and escaped not in candidates:
            candidates.append(escaped)

    last_error = None
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as exc:
            last_error = exc
    message = str(last_error) if last_error else "empty JSON content"
    snippet = clean[:240].replace("\n", "\\n")
    raise ValueError(f"{label} is not valid JSON: {message}; snippet={snippet}")


def strip_markdown_fence(text):
    clean = str(text or "").strip()
    if not clean.startswith("```"):
        return clean
    clean = re.sub(r"^```[A-Za-z0-9_-]*\s*", "", clean)
    clean = re.sub(r"\s*```$", "", clean)
    return clean.strip()


def extract_json_document(text):
    value = str(text or "").strip()
    starts = [(value.find("{"), "{", "}"), (value.find("["), "[", "]")]
    starts = [item for item in starts if item[0] >= 0]
    if not starts:
        return value
    start, open_char, close_char = min(starts, key=lambda item: item[0])
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(value)):
        char = value[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return value[start:index + 1]
    return value[start:]


def repair_common_json_issues(text):
    value = str(text or "").strip()
    if not value:
        return value
    value = re.sub(r",(\s*[}\]])", r"\1", value)
    value = re.sub(r'((?:true|false|null)|[}\]"]|-?\d+(?:\.\d+)?)\s*\n\s*("[-A-Za-z0-9_\u4e00-\u9fff]+":)', r"\1,\n\2", value)
    return value


def escape_control_chars_in_strings(text):
    value = str(text or "")
    result = []
    in_string = False
    escape = False
    for char in value:
        if in_string:
            if escape:
                result.append(char)
                escape = False
                continue
            if char == "\\":
                result.append(char)
                escape = True
                continue
            if char == '"':
                result.append(char)
                in_string = False
                continue
            if char == "\n":
                result.append("\\n")
                continue
            if char == "\r":
                result.append("\\r")
                continue
            if char == "\t":
                result.append("\\t")
                continue
            if ord(char) < 0x20:
                result.append(f"\\u{ord(char):04x}")
                continue
            result.append(char)
            continue
        result.append(char)
        if char == '"':
            in_string = True
    return "".join(result)


def write_json_file(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data or {}, ensure_ascii=False, indent=2), encoding="utf-8")


def envelope(result=None):
    base = {
        "success": True,
        "processedSources": [],
        "createdPages": [],
        "updatedPages": [],
        "archivedFiles": [],
        "skippedSources": [],
        "errors": [],
        "commitId": "",
    }
    base.update(result or {})
    return base


def write_result(path, result):
    data = envelope(result)
    write_json_file(path, data)
    return data


def print_json(data):
    sys.stdout.buffer.write((json.dumps(data or {}, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
