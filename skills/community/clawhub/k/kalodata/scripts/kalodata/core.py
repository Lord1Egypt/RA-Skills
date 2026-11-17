"""Command framework: declarative flags, strict parsing, per-command help.

Unknown flags are rejected loudly (exit 2) with the command's valid flags
inlined so the agent self-corrects in one turn. `--help` and `--json` are
always allowed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .errors import UsageError


@dataclass
class Flag:
    name: str  # "--range"
    help: str = ""
    kind: str = "str"  # str | int | flag | multi
    default: Any = None
    choices: tuple | None = None
    metavar: str | None = None
    renamed_from: tuple = ()  # old names -> targeted hint instead of generic list

    @property
    def dest(self) -> str:
        return self.name.lstrip("-").replace("-", "_")


JSON_FLAG = Flag("--json", "output raw JSON instead of TOON", kind="flag", default=False)


@dataclass
class Command:
    path: str  # e.g. "product rank"
    summary: str
    handler: Callable  # handler(cfg, opts, args) -> int
    flags: list[Flag] = field(default_factory=list)
    positional: str | None = None  # metavar for positional args
    pos_min: int = 0
    pos_max: int | None = 0  # None = unlimited
    examples: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not any(f.name == "--json" for f in self.flags):
            self.flags.append(JSON_FLAG)

    def flag(self, name: str) -> Flag | None:
        for f in self.flags:
            if f.name == name:
                return f
        return None

    def usage(self) -> str:
        parts = [f"kalo {self.path}"]
        if self.positional:
            suffix = "..." if self.pos_max is None else ""
            wrap = (lambda s: s) if self.pos_min else (lambda s: f"[{s}]")
            parts.append(wrap(f"<{self.positional}>{suffix}"))
        if self.flags:
            parts.append("[flags]")
        return " ".join(parts)


def parse_args(cmd: Command, tokens: list[str]) -> tuple[dict, list[str]]:
    known = {f.name: f for f in cmd.flags}
    renames = {old: f for f in cmd.flags for old in f.renamed_from}
    opts: dict[str, Any] = {}
    for f in cmd.flags:
        opts[f.dest] = list(f.default) if isinstance(f.default, list) else f.default
    opts["help"] = False
    pos: list[str] = []

    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "--help" or t == "-h":
            opts["help"] = True
            i += 1
            continue
        if t.startswith("--"):
            name, eq, inline = t.partition("=")
            f = known.get(name)
            if f is None:
                if name in renames:
                    raise UsageError(
                        f"{name} was renamed; use {renames[name].name} instead",
                        [f"usage: {cmd.usage()}"],
                    )
                valid = ", ".join(sorted(known))
                raise UsageError(
                    f"unknown flag {name} for `{cmd.path}`",
                    [f"valid flags for `{cmd.path}`: {valid} (--help always allowed)"],
                )
            if f.kind == "flag":
                if eq:
                    raise UsageError(f"{name} takes no value", [f"usage: {cmd.usage()}"])
                opts[f.dest] = True
                i += 1
                continue
            if eq:
                raw = inline
            else:
                i += 1
                if i >= len(tokens):
                    raise UsageError(f"{name} requires a value", [f"usage: {cmd.usage()}"])
                raw = tokens[i]
            if f.choices and raw not in f.choices:
                raise UsageError(
                    f"invalid value '{raw}' for {name}",
                    [f"valid values: {', '.join(f.choices)}"],
                )
            if f.kind == "int":
                try:
                    raw = int(raw)
                except ValueError:
                    raise UsageError(f"{name} expects an integer, got '{raw}'") from None
            if f.kind == "multi":
                opts[f.dest] = (opts[f.dest] or []) + [raw]
            else:
                opts[f.dest] = raw
            i += 1
            continue
        if t.startswith("-") and t != "-":
            valid = ", ".join(sorted(known))
            raise UsageError(
                f"unknown flag {t} for `{cmd.path}` (long flags only)",
                [f"valid flags for `{cmd.path}`: {valid} (--help always allowed)"],
            )
        pos.append(t)
        i += 1

    if not opts["help"]:
        if len(pos) < cmd.pos_min:
            hint = [f"usage: {cmd.usage()}"]
            if cmd.examples:
                hint.append(f"example: {cmd.examples[0]}")
            raise UsageError(f"`{cmd.path}` requires <{cmd.positional}>", hint)
        if cmd.pos_max is not None and len(pos) > cmd.pos_max:
            raise UsageError(
                f"`{cmd.path}` takes at most {cmd.pos_max} argument(s), got {len(pos)}",
                [f"usage: {cmd.usage()}"],
            )
    return opts, pos


def command_help(cmd: Command) -> str:
    lines = [f"usage: {cmd.usage()}", cmd.summary, ""]
    if cmd.flags:
        lines.append("flags:")
        for f in cmd.flags:
            if f.kind == "flag":
                head = f"  {f.name}"
            else:
                mv = f.metavar or ("|".join(f.choices) if f.choices else f.dest.upper())
                head = f"  {f.name} <{mv}>"
            desc = f.help
            if f.default not in (None, False, []):
                desc += f" (default {f.default})"
            lines.append(f"{head:<34} {desc}".rstrip())
    if cmd.examples:
        lines.append("")
        lines.append("examples:")
        lines.extend(f"  {e}" for e in cmd.examples)
    return "\n".join(lines)
