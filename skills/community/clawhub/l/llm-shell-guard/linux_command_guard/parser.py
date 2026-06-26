from __future__ import annotations

import shlex
from dataclasses import dataclass

SHELL_PUNCTUATION = "|&;()<>"
DANGEROUS_OPERATORS = {
    ";",
    "&&",
    "||",
    "|",
    ">",
    ">>",
    "<",
    "<<",
    "<<<",
    "2>",
    "2>>",
    "&>",
    "<&",
    ">&",
}


@dataclass(frozen=True)
class ParsedCommand:
    raw: str
    tokens: tuple[str, ...]
    base_command: str | None


def tokenize(command: str) -> tuple[str, ...]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=SHELL_PUNCTUATION)
    lexer.whitespace_split = True
    lexer.commenters = ""
    return tuple(token for token in lexer)


def parse_command(command: str) -> ParsedCommand:
    tokens = tokenize(command)
    base = next((token for token in tokens if token.strip()), None)
    return ParsedCommand(raw=command, tokens=tokens, base_command=base)


def has_dangerous_operator(tokens: tuple[str, ...]) -> bool:
    if any(token in DANGEROUS_OPERATORS for token in tokens):
        return True

    # shlex may split multi-char operators into repeated punctuation tokens
    joined = " ".join(tokens)
    operator_snippets = ("&&", "||", ">>", "<<", "<<<", "|", ";")
    return any(op in joined for op in operator_snippets)


def has_command_substitution(command: str) -> bool:
    return "$()" in command or "$(" in command or "`" in command
