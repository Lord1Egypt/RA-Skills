#!/usr/bin/env python3
"""
_tz.py — reading a birthplace timezone argument, in one place.

bazi.py, ziwei.py, astro.py and synastry.py all take --tz, and each used to carry its own
copy of the parser. Two of them passed anything that wasn't a bare number straight to
zoneinfo, so a typo'd zone, `+05:30` or `UTC+8` ended in a traceback. None of them checked
a number, so `--tz 30` charted a birth thirty hours from Greenwich and `inf` crashed.
"""
import re
import sys

# The offsets in civil use run from UTC-12 (Baker Island) to UTC+14 (Kiritimati).
MIN_OFFSET_HOURS = -12.0
MAX_OFFSET_HOURS = 14.0

# +05:30, +0530, -5, UTC+8, GMT-3:30. The sign is required, so a bare "8:00" — which reads
# like a clock time — is never taken for an offset.
_WRITTEN_OFFSET = re.compile(r"(?:UTC|GMT)?\s*([+-])(\d{1,2})(?::?([0-5]\d))?", re.IGNORECASE)


def parse_tz(value):
    """A birthplace timezone: an IANA zone name, returned as the name, or a UTC offset,
    returned as hours (8, -5, 5.75, +05:30, +0545, UTC+8, GMT-3:30). Anything else raises
    ValueError with a message that names --tz."""
    text = str(value).strip()
    written = _WRITTEN_OFFSET.fullmatch(text)
    if written:
        sign = -1.0 if written.group(1) == "-" else 1.0
        hours = sign * (int(written.group(2)) + int(written.group(3) or 0) / 60.0)
    else:
        try:
            hours = float(text)
        except ValueError:
            hours = None
    if hours is not None:
        if not MIN_OFFSET_HOURS <= hours <= MAX_OFFSET_HOURS:    # refuses nan and inf too
            raise ValueError(
                f"--tz {text!r} is not a UTC offset in use anywhere: offsets run from "
                f"{MIN_OFFSET_HOURS:+g} to {MAX_OFFSET_HOURS:+g} hours")
        return hours
    try:
        from zoneinfo import ZoneInfo
        ZoneInfo(text)
    except Exception as e:      # ZoneInfoNotFoundError, ValueError, IsADirectoryError, ...
        raise ValueError(
            f"--tz must be an IANA zone name (Asia/Shanghai, Europe/Amsterdam) or a UTC "
            f"offset (8, -5, +05:30, UTC+8); got {text!r}") from e
    return text


def argv_with_offsets(flags, argv=None):
    """The command line with every `--tz -05:00` joined into `--tz=-05:00`.

    argparse takes a value that starts with a dash and isn't a plain negative number for
    a second option, and stops with "expected one argument" — so a western offset written
    the usual way was refused before the parser above ever saw it."""
    argv = list(sys.argv[1:] if argv is None else argv)
    out, i = [], 0
    while i < len(argv):
        value = argv[i + 1] if i + 1 < len(argv) else None
        if argv[i] in flags and value is not None and value.startswith("-") and _offset_like(value):
            out.append(f"{argv[i]}={value}")
            i += 2
        else:
            out.append(argv[i])
            i += 1
    return out


def _offset_like(text):
    if _WRITTEN_OFFSET.fullmatch(text.strip()):
        return True
    try:
        float(text)
    except ValueError:
        return False
    return True
