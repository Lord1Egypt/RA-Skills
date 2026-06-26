#!/usr/bin/env python3
"""Detect bare imperative sentences with implicit/elided subjects.

Catches patterns like:
  "Fix"           -> bare_verb (no object at all)
  "Make good"     -> verb_adjective (verb + adjective, no noun object)
  "Clean up"      -> verb_adjective (phrasal verb, no object)
  "Make beautiful" -> verb_adjective

Does NOT flag:
  "Fix the bug"       -> has explicit object (determiner present)
  "Add tests"         -> has explicit noun object
  "Make a component"  -> has explicit object (article present)
"""

import re
import sys

IMPERATIVE_VERBS = {
    "add", "adjust", "align", "build", "center", "change", "check", "clean",
    "clear", "complete", "convert", "create", "debug", "delete", "deploy",
    "design", "do", "finish", "fix", "format", "get", "implement", "improve",
    "lint", "make", "merge", "move", "optimize", "pull", "push", "put",
    "refactor", "remove", "rename", "reset", "restart", "revert", "run",
    "set", "ship", "simplify", "start", "stop", "style", "test", "transform",
    "tweak", "undo", "update", "upgrade", "wrap",
}

ADJECTIVES = {
    "accessible", "async", "beautiful", "best", "better", "big", "bigger",
    "brief", "clean", "cleaner", "clear", "concise", "consistent", "correct",
    "dry", "dynamic", "easy", "easier", "efficient", "elegant", "fast",
    "faster", "fastest", "functional", "good", "longer", "maintainable",
    "modular", "nice", "parallel", "performant", "prettier", "pretty",
    "proper", "readable", "responsive", "reusable", "right", "robust",
    "safe", "safer", "secure", "sequential", "short", "shorter", "simple",
    "simpler", "simplest", "slow", "slower", "small", "smaller", "solid",
    "stable", "testable", "typed", "working",
}

FILLER = {"and", "or", "but", "yet", "more", "less", "very", "really",
          "super", "too", "much", "up", "out", "off", "over", "away"}

DETERMINERS = {"a", "an", "the", "my", "our", "your", "his", "her", "their", "its"}


def detect(msg):
    msg = msg.strip()
    if not msg:
        return "none"

    if any(c in msg for c in "\"'`(){}[]"):
        return "none"

    words = re.findall(r"\w+", msg.lower())
    if not words or len(words) > 8:
        return "none"

    if words[0] not in IMPERATIVE_VERBS:
        return "none"

    if len(words) == 1:
        return "bare_verb"

    rest = words[1:]

    if any(w in DETERMINERS for w in rest):
        return "none"

    allowed = ADJECTIVES | FILLER
    if all(w in allowed for w in rest):
        return "verb_adjective"

    return "none"


if __name__ == "__main__":
    print(detect(sys.stdin.read()))
