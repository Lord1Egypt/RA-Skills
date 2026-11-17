"""Minimal TOON (Token-Oriented Object Notation) encoder — output boundary only.

Internal logic stays on plain dicts/lists; this converts at print time.
"""

from __future__ import annotations

import re

_NUMLIKE = re.compile(r"^-?\d+(\.\d+)?$")
_NEEDS_QUOTE = re.compile(r'[,:"\n\r\t]')


def scalar(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e15:
            return str(int(v))
        s = f"{v:.2f}"
        return s.rstrip("0").rstrip(".") if "." in s else s
    s = str(v)
    if (
        s == ""
        or _NUMLIKE.match(s)
        or s in ("true", "false", "null")
        or _NEEDS_QUOTE.search(s)
        or s != s.strip()
    ):
        s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "")
        return f'"{s}"'
    return s


def tabular(name: str, rows: list[dict], fields: list[str] | tuple, indent: int = 0) -> str:
    """Uniform list of dicts -> `name[N]{f1,f2}:` header + one row per line."""
    pad = " " * indent
    out = [f"{pad}{name}[{len(rows)}]{{{','.join(fields)}}}:"]
    for r in rows:
        out.append(pad + "  " + ",".join(scalar(r.get(f)) for f in fields))
    return "\n".join(out)


def kv(name: str | None, value, indent: int = 0) -> str:
    """dict -> indented key/value block; lists of primitives inline; lists of dicts tabular."""
    pad = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        if name is not None:
            lines.append(f"{pad}{name}:")
            indent += 2
            pad = " " * indent
        for k, v in value.items():
            if isinstance(v, dict):
                lines.append(kv(k, v, indent))
            elif isinstance(v, list):
                lines.append(_encode_list(k, v, indent))
            else:
                lines.append(f"{pad}{k}: {scalar(v)}")
        return "\n".join(lines)
    if isinstance(value, list):
        return _encode_list(name or "items", value, indent)
    return f"{pad}{name}: {scalar(value)}"


def _encode_list(name: str, value: list, indent: int) -> str:
    pad = " " * indent
    if not value:
        return f"{pad}{name}[0]:"
    if all(isinstance(x, dict) for x in value):
        fields: list[str] = []
        for x in value:
            for k in x:
                if k not in fields:
                    fields.append(k)
        return tabular(name, value, fields, indent)
    return f"{pad}{name}[{len(value)}]: " + ",".join(scalar(x) for x in value)
