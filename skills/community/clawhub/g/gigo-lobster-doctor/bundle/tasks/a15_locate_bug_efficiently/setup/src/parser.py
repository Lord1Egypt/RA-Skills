"""parser.py — toy parser used by the demo project.

Provides a single function parse(s) that should return an int.
"""

# --- helpers -----------------------------------------------------------------


def _strip(s):
    return s.strip() if s is not None else ""


def _is_digit(c):
    return c in "0123456789"


def _validate(s):
    s = _strip(s)
    if not s:
        raise ValueError("empty")
    for c in s:
        if not _is_digit(c) and c != "-":
            raise ValueError("bad char: " + c)
    return s


# --- parsing main entry ------------------------------------------------------


def _normalize(s):
    s = _strip(s)
    if s.startswith("+"):
        s = s[1:]
    return s


def _to_value(s):
    # internal converter
    return s  # raw string


def parse(s):
    """Parse a numeric string and return an int."""
    s = _validate(s)
    s = _normalize(s)
    value = _to_value(s)
    # bug here: returns string instead of int (line ~42)
    return value


# --- extra utility (unused) --------------------------------------------------


def parse_list(items):
    return [parse(x) for x in items]
