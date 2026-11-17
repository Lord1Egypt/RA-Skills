#!/usr/bin/env python3
"""Iterate skill CLI.

Inspired by ui-ux-pro-max-skill's uipro-cli, this script installs the skill
into AI assistants' skills directories and provides helpers to manage the
project-level iterate.config.yaml.

Usage:
    python scripts/install.py --ai trae --target /path/to/project
    python scripts/install.py install --ai all --target /path/to/project
    python scripts/install.py config --init --target /path/to/project
    python scripts/install.py config --set goal="Improve code quality"
    python scripts/install.py config --set dimensions='[correctness, security]'
    python scripts/install.py config --interactive
    python scripts/install.py uninstall --ai trae --target /path/to/project --yes
    python scripts/install.py validate --target /path/to/project
    python scripts/install.py update --ai trae --target /path/to/project --token ghp_xxx
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import hmac
import http.client
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zlib
from collections.abc import Callable
from pathlib import Path

import yaml

# Type alias for the input callable used across interactive prompts so tests
# can inject mock responses without touching stdin.
InputFunc = Callable[[str], str]

# --- Lightweight TUI helpers (skills.sh style) -----------------------------
# install.py runs as a standalone script (often before iterate_cli is pip
# installed), so we cannot hard-depend on iterate_cli.tui. We try to import
# rich for nicer output and gracefully fall back to plain print when rich is
# unavailable. All output is funneled through these helpers so the install /
# update / uninstall / config flows share a consistent visual style with the
# iterate CLI commands.
try:
    from rich.console import Console
    from rich.theme import Theme
    _THEME = Theme({
        "iterate.primary": "bold cyan",
        "iterate.success": "green",
        "iterate.error": "bold red",
        "iterate.warning": "yellow",
        "iterate.hint": "dim",
        "iterate.title": "bold cyan",
        "iterate.label": "bold",
    })
    # Respect FORCE_COLOR like other CLI tools; default to auto-detect (TTY).
    _force_color = os.environ.get("FORCE_COLOR", "")
    if _force_color in ("", "0", "false", "False"):
        _force_terminal = None
    else:
        _force_terminal = True
    _CONSOLE = Console(theme=_THEME, force_terminal=_force_terminal)
    _ERR_CONSOLE = Console(theme=_THEME, stderr=True, force_terminal=_force_terminal)
    _RICH_AVAILABLE = True
except ImportError:
    _CONSOLE = None
    _ERR_CONSOLE = None
    _RICH_AVAILABLE = False


def _escape_markup(text: str) -> str:
    """Escape ``text`` so rich renders it literally instead of as markup.

    rich treats ``[...]`` as a style tag and drops it from the output. Any
    user-influenced string (a target path, an HTTP status, a file name) can
    legitimately contain square brackets, so it must be escaped before being
    embedded in a styled template. Returns ``text`` unchanged when rich is
    unavailable (plain ``print`` needs no escaping).
    """
    if not _RICH_AVAILABLE:
        return text
    from rich.markup import escape as _rich_escape

    return _rich_escape(text)


def _tui_print(message: str, *, style: str = "", stderr: bool = False) -> None:
    """Print a styled message, falling back to plain print without rich."""
    if not _RICH_AVAILABLE:
        if stderr:
            print(message, file=sys.stderr)
        else:
            print(message)
        return
    console = _ERR_CONSOLE if stderr else _CONSOLE
    if style:
        # Escape the MESSAGE, never the style: rich parses `[...]` as markup,
        # so a path like `C:\\[build]\\skill` or an error text containing
        # `[404]` was silently swallowed as a (nonexistent) style tag and
        # vanished from the output — the operator lost the very detail the
        # line was there to convey.
        console.print(f"[{style}]{_escape_markup(message)}[/]")
    else:
        console.print(_escape_markup(message))


def _intro(title: str, subtitle: str = "") -> None:
    """skills.sh-style intro banner."""
    _tui_print("")
    _tui_print(f"◆ {title}", style="iterate.primary")
    if subtitle:
        _tui_print(f"  {subtitle}", style="iterate.hint")
    _tui_print("")


def _success(message: str) -> None:
    """Success line with check mark."""
    _tui_print(f"✓ {message}", style="iterate.success")


def _error(message: str) -> None:
    """Error line to stderr with cross mark."""
    _tui_print(f"✗ {message}", style="iterate.error", stderr=True)


def _warning(message: str) -> None:
    """Warning line."""
    _tui_print(f"⚠  {message}", style="iterate.warning")


def _hint(message: str) -> None:
    """Dim hint line."""
    _tui_print(message, style="iterate.hint")


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences for width calculation.

    Matches any CSI sequence (``ESC [`` + params + final byte) — not just the
    SGR color codes ``[0-9;]*m``. Cursor moves (``A/B/C/D/G``), erase
    operations (``J/K``) and other final bytes are all stripped so the visible
    width of a line is measured against the actual text the terminal renders.
    """
    import re

    return re.sub(r"\x1b\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]", "", text)


def _wcwidth_display_cols(text: str) -> int:
    """Number of terminal display columns a plain string occupies.

    Wide (CJK) characters count as two columns; ANSI/control sequences and
    zero-width characters contribute nothing. Kept minimal and dependency-free
    so the arrow-menu redraw can align cursor rewinds with the real line
    wrapping the terminal performs.
    """
    total = 0
    for char in text:
        code = ord(char)
        if code == 0:
            continue
        # Narrow: ASCII printable + C0 control width 0.
        if code < 0x20 or (0x7F <= code < 0xA0):
            continue
        # Wide/East-Asian ambiguous handled as wide when fullwidth combining.
        if code >= 0x1100 and (
            (0x1100 <= code <= 0x115F)
            or (0x2E80 <= code <= 0xA4CF)
            or (0xAC00 <= code <= 0xD7A3)
            or (0xF900 <= code <= 0xFAFF)
            or (0xFE30 <= code <= 0xFE4F)
            or (0xFF00 <= code <= 0xFF60)
            or (0xFFE0 <= code <= 0xFFE6)
            or (0x20000 <= code <= 0x3FFFD)
        ):
            total += 2
        else:
            total += 1
    return total


def _physical_row_count(lines: list[str], terminal_cols: int) -> int:
    """Total terminal rows the given logical lines occupy after wrapping.

    ``lines`` may still contain ANSI escapes (colors/emphasis); each line is
    stripped to its visible text and its display width divided by the terminal
    width, rounded up. Row count never drops below the number of lines.
    """
    if terminal_cols <= 0:
        return max(1, len(lines))
    rows = 0
    for line in lines:
        visible = _strip_markup(_strip_ansi(line))
        cols = _wcwidth_display_cols(visible)
        rows += max(1, -(-cols // terminal_cols))
    return rows


def _terminal_columns() -> int:
    """Current terminal width in columns (falls back to 80 on error)."""
    try:
        import shutil

        size = shutil.get_terminal_size((80, 24))
        return size.columns or 80
    except OSError:
        return 80


def _strip_markup(text: str) -> str:
    """Remove rich markup tags for the plain-text fallback."""
    import re

    return re.sub(r"\[/?[a-zA-Z0-9_\-:. ]*\]", "", text)


def _display_width(text: str) -> int:
    """Terminal display columns of ``text`` (wide/CJK glyphs count as 2).

    ``len()`` counts *characters*, but a CJK ideograph occupies two terminal
    columns, so a frame padded with ``len()`` sits too close to the right edge
    and its border glyphs shift. Mirrors ``iterate_cli.tui._display_width`` —
    duplicated because this script must run before the skill is installed and
    therefore cannot import from ``iterate_cli``.
    """
    width = 0
    for ch in text:
        cp = ord(ch)
        # Control characters (C0, DEL, C1) render nothing and take no width.
        if cp < 0x20 or 0x7F <= cp <= 0x9F:
            continue
        # Combining marks and variation selectors follow the previous character.
        if (
            0x0300 <= cp <= 0x036F
            or 0xFE00 <= cp <= 0xFE0F
            or 0xE0100 <= cp <= 0xE01EF
        ):
            continue
        # East Asian wide/fullwidth: CJK ideographs, kana, Hangul, fullwidth
        # forms and fullwidth punctuation.
        if (
            0x1100 <= cp <= 0x115F
            or 0x2E80 <= cp <= 0xA4CF
            or 0xAC00 <= cp <= 0xD7A3
            or 0xF900 <= cp <= 0xFAFF
            or 0xFE30 <= cp <= 0xFE4F
            or 0xFF00 <= cp <= 0xFF60
            or 0xFFE0 <= cp <= 0xFFE6
        ):
            width += 2
            continue
        # Emoji and pictographs render as two columns in most terminals.
        if 0x1F000 <= cp <= 0x1FAFF:
            width += 2
            continue
        width += 1
    return width


def _frame_box(title: str, lines: list[str]) -> None:
    """Print a skills.sh-style framed box.

    Uses single-line box drawing characters so the frame stays aligned
    across terminals that render these glyphs consistently.

    Every pad is computed from display columns rather than ``len()``: the
    summary lines carry project paths and names the user supplies, which for a
    Chinese project include CJK text, and padding by character count left the
    right-hand ``│`` overflowing the top/bottom border by one column per wide
    glyph.
    """
    visible_lines = [_strip_markup(_strip_ansi(line)) for line in lines]
    widths = [_display_width(title)] + [_display_width(line) for line in visible_lines]
    max_len = max(*widths, 1)
    inner_width = max_len + 2

    top = f"┌─ {title} {'─' * max(0, inner_width - _display_width(title) - 2)}┐"
    bottom = f"└{'─' * (inner_width + 1)}┘"

    if _RICH_AVAILABLE:
        _CONSOLE.print(f"[iterate.primary]{top}[/]")
        for line, visible in zip(lines, visible_lines):
            padding = " " * (inner_width - _display_width(visible))
            _CONSOLE.print(f"[iterate.primary]│[/] {line}{padding}[iterate.primary]│[/]")
        _CONSOLE.print(f"[iterate.primary]{bottom}[/]")
    else:
        print(top)
        for line, visible in zip(lines, visible_lines):
            plain_line = _strip_markup(line)
            padding = " " * (inner_width - _display_width(visible))
            print(f"│ {plain_line}{padding}│")
        print(bottom)


GITHUB_REPO_OWNER = "jingzhao-l"
GITHUB_REPO_NAME = "iterate-skill"

# Fallback installer version when pyproject.toml cannot be read (the script is
# often executed standalone, before the package is installed).
_FALLBACK_INSTALLER_VERSION = "0.0.0+unknown"


#: The ``[project]`` table's own header line, and the version assignment that
#: follows it. Deliberately table-scoped: a top-level ``version =`` search would
#: happily return ``[tool.hatch] version`` or any other table's key and print a
#: version that belongs to no one.
_PROJECT_TABLE_RE = re.compile(r"^\[project\]\s*$", re.MULTILINE)
_PROJECT_VERSION_RE = re.compile(r"""^version\s*=\s*["']([^"']+)["']""", re.MULTILINE)


def _version_from_text(text: str) -> str | None:
    """Read ``[project].version`` out of TOML text with no TOML parser.

    Only the shape pyproject.toml actually uses for its own version line is
    recognised: a bare ``version = "..."`` inside the ``[project]`` table, before
    the next table header. Anything else returns ``None`` so the caller falls
    back loudly instead of guessing.
    """
    header = _PROJECT_TABLE_RE.search(text)
    if header is None:
        return None
    tail = text[header.end():]
    next_table = re.search(r"^\[", tail, re.MULTILINE)
    if next_table is not None:
        tail = tail[: next_table.start()]
    match = _PROJECT_VERSION_RE.search(tail)
    return match.group(1) if match else None


def _installed_version() -> str:
    """Return the skill version for ``--version``.

    Reads ``[project].version`` from the bundled pyproject.toml so the value
    can never drift from the single source of truth used by the release; falls
    back to a placeholder when the file is absent or unparseable (standalone
    execution of a copied script) rather than raising.
    """
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    try:
        text = pyproject.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return _FALLBACK_INSTALLER_VERSION
    try:
        import tomllib

        data = tomllib.loads(text)
    except ImportError:
        # Python 3.10 has no tomllib (it is 3.11+), and this package supports
        # >=3.10 — so a missing module is an expected path, not a corrupted
        # manifest. Falling straight through to the placeholder here made
        # `--version` print "0.0.0+unknown" on a supported interpreter while
        # pyproject.toml said the real version.
        parsed = _version_from_text(text)
        return parsed if parsed is not None else _FALLBACK_INSTALLER_VERSION
    except Exception:  # noqa: BLE001 - malformed TOML must not break --version
        return _FALLBACK_INSTALLER_VERSION
    version = data.get("project", {}).get("version")
    return version if isinstance(version, str) and version else _FALLBACK_INSTALLER_VERSION
# NOTE: this is deliberately the *release list*, not `/releases/latest`.
# `/releases/latest` means "newest non-prerelease by published_at" across the
# whole repository, and this repository also publishes releases for the
# harness/plugin sub-projects, which carry no skill tarball. When such a
# release is the most recently published one, `/releases/latest` returns it and
# every install fails with "release has no iterate-skill.tar.gz asset".
# Listing releases and picking the newest one that actually *carries* the
# tarball is immune to whatever else was published last.
RELEASES_API_URL = (
    f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"
    "/releases?per_page=100"
)
CHECKSUMS_ASSET_NAME = "SHA256SUMS.txt"
EXPECTED_TARBALL_FILENAME = "iterate-skill.tar.gz"
#: Detached ASCII-armored signature asset: its presence and validity are
#: MANDATORY (see the signature policy block below).
SIGNATURE_ASSET_NAME = f"{EXPECTED_TARBALL_FILENAME}.asc"

# Accepted GitHub Personal Access Token prefixes (classic ``ghp_``/``gho_``/``ghu_``
# and fine-grained ``github_pat_``). Used to fail fast when a token is mistyped
# rather than sending an arbitrary header value to GitHub.
GITHUB_TOKEN_PREFIXES: tuple[str, ...] = (
    "ghp_",
    "gho_",
    "ghu_",
    "ghs_",
    "ghr_",
    "github_pat_",
)

# Timeouts (seconds) used across network/subprocess calls, kept as named
# constants so the magic values are not scattered through the code.
GITHUB_API_TIMEOUT_SECONDS = 15
DOWNLOAD_TIMEOUT_SECONDS = 30
# Config validation spawns a fresh Python process that imports jsonschema and
# scans the dimensions directory. On a loaded machine (or a cold, slow disk)
# startup alone can exceed 30s — the previous value made `config --set` revert
# a perfectly valid change with "Command timed out after 30 seconds". The
# timeout is a safety net against a hung interpreter, not a performance gate,
# so it is generous and overridable for constrained CI sandboxes.
VALIDATE_SUBPROCESS_TIMEOUT_SECONDS = 120
VALIDATE_TIMEOUT_ENV = "ITERATE_VALIDATE_TIMEOUT"

# Upper bound for a single downloaded payload (release tarball / checksum).
# Streams are read in chunks and truncated when the cap is exceeded, so a
# misbehaving upstream can never exhaust memory.
MAX_DOWNLOAD_BYTES = 50 * 1024 * 1024  # 50 MiB
_DOWNLOAD_CHUNK_SIZE = 64 * 1024  # 64 KiB read chunks while streaming

# Decompression-bomb bounds enforced in _safe_extractall BEFORE extracting:
# a compressed payload can expand far beyond its transport size, so the
# uncompressed budget is (deliberately) a few times the download cap rather
# than derived from it. A member exceeding the per-member cap is also refused.
MAX_EXTRACT_BYTES = 500 * 1024 * 1024  # 500 MiB total uncompressed
MAX_EXTRACT_MEMBER_BYTES = 256 * 1024 * 1024  # 256 MiB per member


# ---------------------------------------------------------------------------
# Release signature policy (MANDATORY)
# ---------------------------------------------------------------------------
#
# The skill release publishes a detached ASCII-armored GPG signature
# (``iterate-skill.tar.gz.asc``) next to the tarball. SHA256SUMS.txt travels in
# the SAME release, so it cannot serve as an independent authenticity anchor —
# the pinned public key below is the only anchor an attacker with release-write
# access cannot forge.
#
# MANDATORY by default: a missing signature, a host without ``gpg``, or a
# signature that does not verify aborts the update. The single documented
# escape hatch is the environment variable ``ITERATE_ALLOW_UNSIGNED`` (for
# hosts without GnuPG) and it NEVER bypasses a BAD signature.
#
# Keep this constant/label byte-identical with ``iterate_cli/signing.py`` and
# ``npm-installer/lib/installer.js`` (tests/test_release_meta.py asserts it).
SIGNING_KEY_FINGERPRINT = "0929EA31DF4F7429F63FC53189D88B1D043A1298"

ALLOW_UNSIGNED_ENV = "ITERATE_ALLOW_UNSIGNED"

ITERATE_SIGNING_PUBLIC_KEY = """-----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBGq45VQBEACdjAoLYyfgPpHjvscmGqxlSsBkcBvSAoGHdCI0p2Rn5cBDaPie
oPU17VmUiK4FBZf8FcaX0L+EeMRO4Bcj5NgoFaSgQPK0YarvoPssClNiWf71hDlg
QmC5IlwM4WuVUeKi3+YoPmRSf0sYHzSYM7vEIoCFzEilYi4iEK/NMihNSktlUsQx
jhIaXtnVJi+7GkO+dhckKmIHhcR76dUfIAsS/R0RzzH4ZXfuKi+B94mfCntURpM4
G+NrxZx7Xv5UDpv9XsrmiWKzNpT+Th9GbNQREjrT1mmKbMEOmD/PWTqxNycJfgdW
hWA++1oassOib3jd44+z5f7FKpp//C+SK8V7vuxNI0jRM/VYrbyrfON30hHwtbFM
0J/quDsAUzlOBNzNVPAyvGsOuSEULFtjaJ2q+JYjF+ZKDPy+lyY8V9sbYrqCCUb9
v3wPn4tDvat30Q0A0rheMZPTMO7tRNSzFOd25H0w3ZF3F5Np8D/aX9VHMkA12xTm
l7gpb1OIEJ1vdQl0twiF6SDz5jsteHfdUXha6CtM7tv7IZ4MIZi/qPkvv4zOKmsE
utLUs1alD671Eez2sQow8NO5IXfd7bX2d34kU5JiM1tF9qhBxOZlpzd/Vm8FZS4V
URF6Y7myW4ildqBeMzLt0to8WjHnHoV4v9rh5581qWEqvNIJ4/R3lKRhxwARAQAB
tC1qaW5nemhhby1sIChzaWduLWdpdGh1YikgPEVUX2xpbkBvdXRsb29rLmNvbT6J
Am0EEwEIAFcWIQQJKeox3090KfY/xTGJ2IsdBDoSmAUCarjlVBsUgAAAAAAEAA5t
YW51MiwyLjUrMS4xMiwwLDMCGwMFCwkIBwICIgIGFQoJCAsCBBYCAwECHgcCF4AA
CgkQidiLHQQ6EpharQ//VhcNiug3cHsgvb/tTqWp1CQV8heSfqoKrW51RPhcGAHW
VMHpbPRO0wBKKE5mybyGAWhGDhh5mZt1MxnBN3lC7RsWBLEaXyJAqW4UPjR5LN8Q
scapkCzFwrF5lisELdqKqkd/ACKR8h6U/fBf0eKE+TMDSrXZ/LkRcFRJErfsC7rx
hy1WQnzQBT2+86HmfW9rrw5RSyCp8MZ0TJhYr0ZdgB4zvLwvVYQCnlRaskkLjGrh
6vUHAjDCUwoDFEpecadCJg34cOEAMRjnTt6Q0t8SnVHDH9PLq1MwGON2VzuSp5rY
rthT3+VRzbzGpBu4wl4/GJiWJMfGTusEu8Ver6MTwHx9pFBDtH3cawIB5BT1RrXk
cYdhtjzJ61RXIrSCeD8yoxEgDOj73Ll6oQ4+fJ+EpOc+SvP9FREeQ4k/uc8MpwtV
YyD/6EPJu1lLMAzgd2Xm2ljokTRhm/Blft9Y0OEEWzsoDGv+jr3Jb3Dgw62OuL6B
pLiZ5XNCYBHYhQhtleGnSpJtD9ooi1UUTbVZftunzYGKafMCgc9nnzPIGVtlzX+d
K10CtPOX7ylS+lKukaIOSStGGSl3I2Fd66yb3ujIH6n/KAKLfMmmy48pxB3+t6WW
StdD7QEASWIyW2wTrq7RyDwmzWMSFtgPzCOWFmcQfFykkvvQEqxMeyCrcPY6ZIy5
Ag0EarjlVAEQAOjPGVDb8zGIc7XQelHhjyd8yLCVpNBWwYLmaSLfI+EQsfVVDJqT
VAAeO82woHELPun06lbJRW59eH8BkVgzGhNkb5vKhrdvmZydYElC1NuRB9ag6/k/
0IaLwedKZscy1k3oG2LqsayzUO3L2d8BxO8zdLEmIl7FqtTdsYwj6DDRgZdA4Aj0
VoUXOgWaR+7qA9GHnnucrE5n0zhrTd7F3mtZErWr6Edo/V9EHQ1PszsQTVH2artr
lYJWjSsAv/ajEvAjaZ1mJoDvz/UzUk7hCCPeNcpy41SpDb3uey38qqxLYOGVgEeD
7JTrhC51VNHj2CCxSgyrlvED+resJtgWnE65Sa8g9cGAVpXlOBRQrPZGMHS+BcAg
9lQExMGrWt76ZPgT5Gygzj09oGx1q6/IyATphit4TblFGl2z1JDnlUQqfz/aCmZN
Vg+fKBPQ93dLLGPKpmY022X3abJ197VaQ0WWB2cA8pcrcfJ8GY7Lm8xjm6nY/cER
RQl72dE1NJsPGrp3Ad/s7fAJuEdR8UmMUPLDQRpiNRTcK6RC2AaRD7wpdyG/1csF
P30IIY97aVSjD5nnkrHxNQKZ17yPef+bFIoJ7OS+WhLZKcr7P0DfgJoTbKc6GK6M
ScQm5N7lRJ9Mfzu4R6576hDrgb3fmgflmpKOIVrZ6GkTGDvQ/FE16QdrABEBAAGJ
AlIEGAEIADwWIQQJKeox3090KfY/xTGJ2IsdBDoSmAUCarjlVBsUgAAAAAAEAA5t
YW51MiwyLjUrMS4xMiwwLDMCGwwACgkQidiLHQQ6Epi4aw//Qu00vxGtvRb+VQl9
lMZLwIP2AgB0lAgKAqYeK6jZh/15GAKJqRh0u2jdgqXj2Sfm79X7Qwn7wAuFUAmx
D1eegOtdAnEP6O8DUtZWWmy2TSRIqjfTcGXlZ12WHiOwwdG5VOUZERWi/rPj0zTs
5V1H4qyPOqgrFx9nNvavzo3zeJVpwYuuFkT2Ne0cZLXGglCQ6MJtuK0Qwk6iYsvy
p3eZ1YCKmAi1v0UFojtFHqJEAsc3PnZb+48veE9b2whrL9DIIkNrrFlfFC1cjm7T
wuRQuH6aYyrRoZiLxgwkW5xmc1Biitw7bMIX6eqYVn8hb1lQUKhTL8aZ2xQa6IsJ
RHIJFYeEIEUtIl/GKQ3MeHQlJrXsfnZ1e8MHgwgMw3o4Nq4xww3Ch0pddYhBskmV
/QUaOHVqmuur9dnRvx9L+FGbzHEjvYDr0MkSe30hUhyBIg1uOLd2elATB/wg33Ow
vcdqgewqpYdSg6g6KZYl6NhmWWNEMgX8KITUXFoTiV5CrSsrptBPJWsyIq+CuseL
CKFdMHrkzbjFLGfdiPqykwttwHBAEk01aWArDP65gXRXmxGzDHVkA7Px1hdo/kMo
Ouw6bEGpHtx7UJJMSMA9ywbTrOyaG4xzVDa7ixUslFtgxts1R/eLoC4I11grxE50
YVXa4IEQs7aBxKO+n+T2AvUYiKQ=
=DYXk
-----END PGP PUBLIC KEY BLOCK-----"""


#: Values that explicitly opt OUT of signature enforcement. Anything else —
#: including "0", "false", "no" and the empty string — keeps the
#: mandatory-signature policy in force. A bare truthiness test treated every
#: non-empty value as an opt-out, so the intuitive ``ITERATE_ALLOW_UNSIGNED=0``
#: ("keep signatures mandatory") silently DISABLED signature enforcement.
_ALLOW_UNSIGNED_TRUE_VALUES = frozenset({"1", "true", "yes"})


def _allow_unsigned() -> bool:
    """True only when the operator explicitly opted out of signature enforcement.

    Requires an explicit truthy value (``1`` / ``true`` / ``yes``,
    case-insensitive); ``0`` / ``false`` / ``no`` / blank all leave the
    mandatory-signature gate in force.
    """
    value = os.environ.get(ALLOW_UNSIGNED_ENV, "").strip().lower()
    return value in _ALLOW_UNSIGNED_TRUE_VALUES


def _validsig_fingerprints(status_output: str) -> list[str]:
    """Extract the fingerprints gpg reported as ``VALIDSIG`` in ``--status-fd``.

    A status line looks like ``[GNUPG:] VALIDSIG <fpr> <date> …``; the
    fingerprint is the token right after the ``VALIDSIG`` keyword. Mirrors
    ``iterate_cli.signing._validsig_fingerprints`` (keep in sync).
    """
    fingerprints: list[str] = []
    for line in status_output.splitlines():
        if not line.startswith("[GNUPG:] VALIDSIG "):
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[2]:
            fingerprints.append(parts[2].upper())
    return fingerprints


def _verify_detached_signature(
    artifact_path: Path,
    signature_path: Path,
    gpg_bin: str = "gpg",
    timeout: int = 30,
) -> tuple[str, str]:
    """Return ``(status, detail)``; status is verified/invalid/unavailable.

    Mirrors ``iterate_cli.signing.verify_detached_signature`` (same pinned key,
    same isolated temporary GNUPGHOME; keep the two in sync).
    """
    gpg = gpg_bin if os.sep in gpg_bin else shutil.which(gpg_bin)
    if not gpg:
        return "unavailable", "gpg binary not found on PATH"
    # Short isolated keyring: gpg's agent socket is <GNUPGHOME>/S.gpg-agent and
    # a deep path trips the ~104-char unix-socket limit ("File name too long").
    try:
        with tempfile.TemporaryDirectory(prefix="ig-") as tmp:
            home = Path(tmp)
            key_path = home / "pub.asc"
            key_path.write_text(ITERATE_SIGNING_PUBLIC_KEY, encoding="utf-8")
            imported = subprocess.run(
                [gpg, "--homedir", str(home), "--batch", "--yes", "--quiet",
                 "--import", str(key_path)],
                capture_output=True, text=True, timeout=timeout, check=False,
            )
            if imported.returncode != 0:
                lines = (imported.stderr or imported.stdout).strip().splitlines()
                return "unavailable", (
                    "could not import the pinned public key"
                    + (f": {lines[-1][:160]}" if lines else "")
                )
            verified = subprocess.run(
                [gpg, "--homedir", str(home), "--batch",
                 "--no-auto-key-retrieve",
                 "--status-fd", "1", "--verify", str(signature_path), str(artifact_path)],
                capture_output=True, text=True, timeout=timeout, check=False,
            )
    except subprocess.TimeoutExpired as exc:
        # A hung gpg is not a missing dependency: classify it as 'invalid' so
        # ITERATE_ALLOW_UNSIGNED cannot bypass authenticity. Only a genuinely
        # absent/unlaunchable gpg may take the explicit unsigned escape hatch.
        # Mirrors iterate_cli/signing.py (keep in sync).
        return "invalid", (
            f"gpg timed out while verifying (treated as invalid): {exc}. "
            "Retry, or inspect the gpg agent/keyring."
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return "unavailable", f"gpg could not run: {exc}"
    # A GOODSIG alone does not prove the signer is the pinned key: a substituted
    # signer whose key is auto-retrieved (or pre-seeded) would pass. Require a
    # VALIDSIG fingerprint that belongs to the pinned key, mirroring
    # iterate_cli/signing.py (keep in sync). --no-auto-key-retrieve above stops
    # gpg fetching an arbitrary signer's key over the network.
    signer_fingerprints = _validsig_fingerprints(verified.stdout)
    if (
        verified.returncode == 0
        and signer_fingerprints
        and any(fpr in (SIGNING_KEY_FINGERPRINT,) for fpr in signer_fingerprints)
    ):
        return "verified", f"signature matches the pinned key ({SIGNING_KEY_FINGERPRINT})"
    lines = [ln for ln in verified.stderr.strip().splitlines() if ln.strip()]
    return "invalid", (lines[-1][:200] if lines else "gpg reported a bad signature")


def _enforce_signature_policy(
    artifact_path: Path,
    signature_path: Path | None,
) -> tuple[bool, str]:
    """Apply the mandatory-signature policy; ``(ok, detail)``.

    ``ok=False`` means the caller MUST abort. Mirrors
    ``iterate_cli.signing.enforce_signature_policy`` (keep in sync).
    """
    override = _allow_unsigned()

    if signature_path is None:
        if override:
            return True, (
                f"UNSIGNED release accepted because {ALLOW_UNSIGNED_ENV} is set "
                "(SHA256 integrity only)"
            )
        return False, (
            "release is UNSIGNED: it publishes no .asc signature, so authenticity "
            "cannot be verified (SHA256SUMS travels in the same release and is not "
            f"an independent anchor). Set {ALLOW_UNSIGNED_ENV}=1 only if you accept "
            "an unauthenticated install."
        )

    status, detail = _verify_detached_signature(artifact_path, signature_path)
    if status == "verified":
        return True, detail
    if status == "invalid":
        return False, (
            f"GPG signature verification FAILED ({detail}). The artifact is not "
            f"signed by the pinned iterate signing key ({SIGNING_KEY_FINGERPRINT}) — "
            f"this is either tampering or a key rotation; {ALLOW_UNSIGNED_ENV} does "
            "NOT bypass a bad signature."
        )
    if override:
        return True, (
            f"signature NOT verified ({detail}) but accepted because "
            f"{ALLOW_UNSIGNED_ENV} is set (SHA256 integrity only)"
        )
    return False, (
        f"cannot verify the release signature ({detail}). Install GnuPG (``gpg``) "
        f"and retry, or set {ALLOW_UNSIGNED_ENV}=1 to accept an unauthenticated install."
    )


def _validate_github_token(token: str | None) -> str | None:
    """Return an error message when ``token`` is malformed, else None.

    Accepts common GitHub token prefixes and requires reasonable length.
    Empty/whitespace-only tokens are treated as absent (None, no error).
    """
    if token is None:
        return None
    stripped = token.strip()
    if not stripped:
        return None
    if any(ch.isspace() or ord(ch) < 0x20 or ord(ch) == 0x7F for ch in stripped):
        # An embedded newline/space reached ``putheader()`` in the old code and
        # raised ``ValueError: Invalid header value`` — whose message echoed the
        # PAT into CLI/CI output. Refuse it before any request is built.
        return (
            "GitHub token contains whitespace or control characters; re-export "
            "it without line breaks (the value is not echoed here on purpose)."
        )
    if len(stripped) < 20 or len(stripped) > 256:
        return (
            "GitHub token looks malformed: expected a PAT (starts with "
            "ghp_/gho_/github_pat_ etc.) of ~40-256 chars, got a very different length."
        )
    if not stripped.startswith(GITHUB_TOKEN_PREFIXES):
        return (
            "GitHub token does not look valid: expected a Personal Access Token "
            "starting with one of (ghp_, gho_, ghu_, ghs_, ghr_, github_pat_). "
            "Double-check the value passed to --token."
        )
    return None

SUPPORTED_AI: dict[str, str] = {
    # Universal / 通用 AI 编程工具（skills.sh 热门支持）
    "claude": ".claude/skills/iterate",
    "claude-code": ".claude/skills/iterate",
    "cursor": ".cursor/skills/iterate",
    "trae": ".trae/skills/iterate",
    "windsurf": ".windsurf/skills/iterate",
    "copilot": ".github/skills/iterate",
    "codex": ".codex/skills/iterate",
    "gemini": ".gemini/skills/iterate",
    "gemini-cli": ".gemini/skills/iterate",
    "opencode": ".opencode/skills/iterate",
    "aider": ".aider/skills/iterate",
    "aiderdesk": ".aiderdesk/skills/iterate",
    "zed": ".zed/skills/iterate",
    "warp": ".warp/skills/iterate",
    "continue": ".continue/skills/iterate",
    "cline": ".cline/skills/iterate",
    "roocode": ".roo/skills/iterate",
    "qoder": ".qoder/skills/iterate",
    "augment": ".augment/skills/iterate",
    "openclaw": "skills/iterate",
    "autohand": ".autohand/skills/iterate",
    "bob": ".bob/skills/iterate",
    "codearts": ".codeartsdoer/skills/iterate",
    "antigravity": ".antigravity/skills/iterate",
    "amp": ".amp/skills/iterate",
    "deepagents": ".deepagents/skills/iterate",
    "kimi": ".kimi/skills/iterate",
    "astral": ".astral/skills/iterate",
}

# 显示名称映射：让交互菜单更友好
AI_DISPLAY_NAMES: dict[str, str] = {
    "claude": "Claude",
    "claude-code": "Claude Code",
    "cursor": "Cursor",
    "trae": "Trae",
    "windsurf": "Windsurf",
    "copilot": "GitHub Copilot",
    "codex": "Codex",
    "gemini": "Gemini",
    "gemini-cli": "Gemini CLI",
    "opencode": "OpenCode",
    "aider": "Aider",
    "aiderdesk": "AiderDesk",
    "zed": "Zed",
    "warp": "Warp",
    "continue": "Continue",
    "cline": "Cline",
    "roocode": "Roo Code",
    "qoder": "Qoder",
    "augment": "Augment",
    "openclaw": "OpenClaw",
    "autohand": "Autohand Code CLI",
    "bob": "IBM Bob",
    "codearts": "CodeArts Agent",
    "antigravity": "Antigravity",
    "amp": "Amp",
    "deepagents": "Deep Agents",
    "kimi": "Kimi Code CLI",
    "astral": "Astral",
}

REQUIRED_FILES = [
    "SKILL.md",
    "config/iterate.config.yaml",
    "config/config.schema.json",
    "config/dimensions.yaml",
    "config/dimensions",
    "scripts/validate.py",
    "scripts/requirements.txt",
    "templates/iterate-decisions.template.md",
    # v2.0.0: CLI onboarding system (iterate onboard / personalize / refresh).
    "iterate_cli",
    "pyproject.toml",
    "templates/ITERATE.template.md",
    "templates/onboarding-playbook.md",
]

OPTIONAL_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "CHANGELOG.md",
    "examples/python-project.md",
    "examples/swift-project.md",
    "examples/typescript-project.md",
    "tools/SKILL.trae.md",
    "tools/SKILL.claude.md",
    "tools/SKILL.cursor.md",
]

AI_CHOICES = list(SUPPORTED_AI.keys()) + ["all"]

DEFAULT_CONFIG_PATH = Path("config/iterate.config.yaml")

MIN_ROUNDS = 1
MAX_ROUNDS = 50

DIMENSION_CHOICES = [
    "correctness",
    "security",
    "performance",
    "architecture",
    "style-tests",
    "tech-debt",
    "spec-compliance",
    "frontend-backend",
    "ui-ux",
]

LANGUAGE_CHOICES = ["zh", "en"]
SCOPE_CHOICES = ["full", "changed-only"]


class ReleaseIntegrityError(Exception):
    """A release could not be verified as authentic (missing/undownloadable
    checksum asset, missing checksum entry, or SHA-256 mismatch).

    Raised by ``_download_release_source`` so callers can fail closed instead of
    silently upgrading from a possibly tampered release. Network/rate-limit
    failures are NOT this exception: they return ``None`` and legitimately
    fall back to local source.
    """


class ReleaseStructureError(Exception):
    """A release passed integrity verification but its archive is unusable
    (extraction failed, or it does not contain exactly one top-level directory
    with a ``SKILL.md`` marker).

    Raised by ``_download_release_source`` so callers abort the update instead
    of silently falling back to the local checkout while the verified release
    is broken — a filtered fallback with the wrong source would be missing the
    failing feature or version, which is the silent defect this class is meant
    to surface.
    """


def copy_skill_files(
    source: Path,
    destination: Path,
    dry_run: bool,
    force: bool,
    *,
    root: Path | None = None,
) -> list[str]:
    """Copy skill files from source to destination.

    Args:
        root: The user-selected install root (project dir or home). When given,
            every destination directory is required to resolve *inside* it, so
            a symlink committed at or above ``destination`` (``.claude ->
            /home/victim/.config``) cannot route writes outside the tree the
            user asked to install into. Without it the leaf-symlink checks
            still apply, but the ancestor anchor necessarily degenerates to the
            destination itself (see the comment below), so callers that know
            the root should always pass it.
    """
    copied: list[str] = []
    all_files = REQUIRED_FILES + OPTIONAL_FILES

    # Resolve the destination once up front so every relative path is checked
    # against the same base. This prevents entries like ``../SKILL.md`` from
    # escaping the destination directory (path traversal on copy).
    # Normalization is purely lexical (normpath/abspath, no symlink following):
    # a pre-existing symlink at the target must be replaced (see below), not
    # treated as a reason to reject the copy.
    destination_base = Path(os.path.abspath(os.path.normpath(destination)))

    # Symlinked *ancestor* guard: a committed symlink at an intermediate
    # directory (e.g. ``.claude -> /home/victim/.config``) would otherwise have
    # every write routed through it and placed outside the user-selected
    # destination — the leaf-symlink replacement below does not cover that.
    #
    # The anchor MUST be the user-selected root, not the destination: resolving
    # the destination follows the very symlink we are trying to detect, so
    # ``realpath(dst.parent) == realpath(destination)`` and the check passed for
    # exactly the attack it documents. With ``root`` known, an escaping
    # ``.claude`` resolves to ``/tmp/outside/skills/iterate``, which is not
    # relative to ``realpath(root)``, and the copy is refused.
    anchor = (
        Path(os.path.abspath(os.path.normpath(root)))
        if root is not None
        else destination_base
    )
    anchor_real = Path(os.path.realpath(anchor))

    for relative in all_files:
        src = source / relative
        if not src.exists():
            if relative in REQUIRED_FILES:
                raise FileNotFoundError(f"Required skill file missing: {src}")
            continue

        dst = destination / relative
        normalized_dst = Path(os.path.abspath(os.path.normpath(dst)))
        if not normalized_dst.is_relative_to(destination_base):
            raise ValueError(
                f"Refusing to copy outside destination: {relative!r} resolves to {normalized_dst}"
            )

        parent_real = Path(os.path.realpath(dst.parent))
        if not (parent_real == anchor_real or parent_real.is_relative_to(anchor_real)):
            raise ValueError(
                f"Refusing to copy through symlinked directory: {relative!r} "
                f"resolves to {parent_real}, outside the install root {anchor_real}"
            )

        if dry_run:
            copied.append(str(dst))
            _hint(f"[dry-run] Would copy: {relative} -> {dst}")
            continue

        if dst.exists() and not force:
            _hint(f"Skipped (already exists, use --force): {dst}")
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            # A symlinked destination must be unlinked, not rmtree'd: on modern
            # Python shutil.rmtree raises OSError when asked to walk a symlink.
            if dst.is_symlink():
                dst.unlink()
            elif dst.exists() and dst.is_dir() and force:
                shutil.rmtree(dst)
            elif dst.exists() and not dst.is_dir() and force:
                # Type collision: a stale regular file where a directory is
                # needed. rmtree would raise NotADirectoryError; unlink the file
                # first so copytree can create the real directory.
                dst.unlink()
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            # Replace a symlinked destination instead of writing through it.
            if dst.is_symlink():
                dst.unlink()
            elif dst.exists() and dst.is_dir() and force:
                # Type collision: a stale directory where a file is needed.
                # copy2(src, dst) would silently write dst/<basename> instead.
                shutil.rmtree(dst)
            shutil.copy2(src, dst)
        copied.append(str(dst))

    return copied


def detect_installed_assistants(effective_target: Path) -> list[str]:
    """Detect which supported AI assistants appear to be installed.

    A tool is considered installed only when its skill directory under
    ``effective_target`` is an actual iterate-skill installation (i.e. it
    contains ``SKILL.md``, the canonical skill marker). This matches the
    exact criterion used by ``_is_iterate_install_dir`` in the uninstall
    and install/upgrade paths, so detection, pre-selection in the installer
    menu, and auto-detected ``update`` all agree.

    Args:
        effective_target: Base directory to inspect (home or project).

    Returns:
        Sorted list of assistant keys that appear installed.
    """
    found: list[str] = []
    for assistant, relative_dir in SUPPORTED_AI.items():
        if _is_iterate_install_dir(effective_target / relative_dir):
            found.append(assistant)
    return sorted(set(found))


def _prompt_multi_select(
    options: list[str],
    input_func: InputFunc,
    title: str = "Select items",
    default_all: bool = True,
    preselected: set[str] | None = None,
) -> list[str]:
    """Present a simple text-based multi-select prompt.

    This intentionally avoids extra dependencies (e.g. simple-term-menu)
    so the installer remains a single standalone script. The interaction
    mimics skills.sh: numbers toggle selection, Enter confirms.

    Args:
        options: List of option identifiers (e.g. assistant keys).
        input_func: Callable used to read user input.
        title: Prompt title.
        default_all: Whether all options start selected (ignored when
            ``preselected`` is provided).
        preselected: Optional set of options to start selected (e.g. the
            auto-detected tools). When provided, only these are pre-checked.

    Returns:
        List of selected option identifiers.
    """
    if preselected is not None:
        selected = set(preselected) & set(options)
    else:
        selected = set(options) if default_all else set()

    while True:
        _tui_print(f"\n{title}", style="iterate.primary")
        _hint("Enter numbers to toggle (comma-separated), or press Enter to confirm.")
        _hint("Tip: prefix with 'a' to select all, 'n' to select none.")
        for i, opt in enumerate(options, 1):
            display = AI_DISPLAY_NAMES.get(opt, opt)
            marker = "[✓]" if opt in selected else "[ ]"
            _tui_print(f"  {marker} {i}. {display}", style="iterate.label" if opt in selected else "")

        try:
            raw = input_func("  \u2514 ").strip()
        except EOFError:
            # Piped/closed stdin (e.g. `installer < /dev/null`) ends the prompt
            # cleanly instead of crashing with a traceback.
            break
        if not raw:
            break

        if raw.lower() == "a":
            selected = set(options)
            continue
        if raw.lower() == "n":
            selected = set()
            continue

        changed = False
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                idx = int(part) - 1
            except ValueError:
                _warning(f"Invalid input: '{part}'")
                continue
            if not (0 <= idx < len(options)):
                _warning(f"Out of range: '{part}'")
                continue
            opt = options[idx]
            if opt in selected:
                selected.remove(opt)
            else:
                selected.add(opt)
            changed = True

        if not changed:
            # User typed something but nothing valid; keep looping.
            _hint("No valid selection; try again or press Enter to confirm.")

    return sorted(selected)


class _ArrowSelectState:
    """State for the arrow-key multi-select menu.

    The visible list is ``options + [None]`` where ``None`` is the trailing
    "Done" confirmation row. Arrow keys move the highlight, Space / Enter
    toggle the current option (or confirm when on the Done row), and ``q``
    cancels. Kept as a plain state machine so the key-handling logic can be
    unit-tested without a TTY.
    """

    MAX_WINDOW = 6  # visible option rows; keeps the menu short enough to fit any terminal

    def __init__(
        self,
        options: list[str],
        default_all: bool = True,
        preselected: set[str] | None = None,
        window_size: int = MAX_WINDOW,
    ) -> None:
        self.options = list(options)
        self.rows: list[str | None] = self.options + [None]
        self.index = 0
        # Scroll window over the option rows. The "Done" confirmation row is
        # always rendered as the final line regardless of scrolling, so the
        # menu height stays bounded (and never overflows short terminals).
        self.window_size = max(1, int(window_size))
        self.window_top = 0
        if preselected is not None:
            # Pre-select only the given options (e.g. auto-detected tools).
            # Options not in the preselected set are still shown but start
            # unchecked, so the user must explicitly opt in to them.
            self.selected: set[str] = set(preselected) & set(self.options)
        else:
            self.selected = set(self.options) if default_all else set()
        self.finished = False

    def move(self, delta: int) -> None:
        """Move the highlight by ``delta`` (wrap around)."""
        self.index = (self.index + delta) % len(self.rows)
        self._ensure_selection_visible()

    def _ensure_selection_visible(self) -> None:
        """Scroll the window so the highlighted row stays on screen.

        When the "Done" row is selected the last page is shown so the final
        options remain visible above the confirmation row.
        """
        count = len(self.options)
        if count == 0:
            self.window_top = 0
            return
        size = min(self.window_size, count)
        max_top = max(0, count - size)
        if self.index >= count:
            self.window_top = max_top
            return
        top = self.window_top
        if self.index < top:
            new_top = max(0, self.index)
        elif self.index >= top + size:
            new_top = max(0, min(self.index - size + 1, max_top))
        else:
            new_top = top
        self.window_top = min(new_top, max_top)

    def visible_options(self) -> list[str]:
        """The currently visible slice of options (scrolled window)."""
        self._ensure_selection_visible()
        count = len(self.options)
        if count == 0:
            return []
        size = min(self.window_size, count)
        max_top = max(0, count - size)
        self.window_top = min(self.window_top, max_top)
        return self.options[self.window_top : self.window_top + size]

    def toggle_current(self) -> None:
        """Toggle the highlighted option; on the Done row, finish instead."""
        opt = self.rows[self.index]
        if opt is None:
            self.finished = True
            return
        if opt in self.selected:
            self.selected.remove(opt)
        else:
            self.selected.add(opt)

    def cancel(self) -> None:
        """Cancel the selection (empty result, finished)."""
        self.finished = True
        self.selected = set()

    @property
    def result(self) -> list[str]:
        """Ordered, sorted list of selected option identifiers."""
        return sorted(self.selected)


def _read_arrow_key(stdin) -> str | None:
    """Decode one raw keypress into a command name.

    Commands: ``up``, ``down``, ``toggle`` (Space / Enter), ``cancel`` (q/Q).
    Returns ``None`` for unrecognized keys. Raises ``KeyboardInterrupt`` on
    Ctrl+C so the caller can restore the terminal and cancel. An EOF read is
    mapped to ``cancel`` so a closed/torn-down terminal cannot busy-loop the
    menu at 100% CPU reading endless empty reads.
    """
    ch = stdin.read(1)
    if ch == "":
        return "cancel"
    if ch == "\x1b":
        # Escape sequence: ESC [ A (up) / B (down).
        seq = stdin.read(2)
        if seq == "[A":
            return "up"
        if seq == "[B":
            return "down"
        return None
    if ch in ("\r", "\n", " "):
        return "toggle"
    if ch in ("q", "Q"):
        return "cancel"
    if ch == "\x03":
        raise KeyboardInterrupt
    return None


def _arrow_select_lines(state: _ArrowSelectState, title: str) -> list[str]:
    """Build the arrow-select menu lines.

    Only the scroll window of options is rendered (bounded number of rows),
    and ``Done`` is always the final line. This keeps the menu compact so
    re-draws never overflow short terminals or rely on line-wrapping to stay
    aligned.
    """
    lines = [
        f"\x1b[36m◆ {title}\x1b[0m",
        "\x1b[2m  ↑/↓ 移动 · 空格 勾选 · Done 完成 · q 取消\x1b[0m",
    ]
    current = state.options[state.index] if state.index < len(state.options) else None
    for opt in state.visible_options():
        display = AI_DISPLAY_NAMES.get(opt, opt)
        check = "\x1b[32m◉\x1b[0m" if opt in state.selected else "\x1b[90m○\x1b[0m"
        if opt == current:
            lines.append(f"\x1b[7m  {check} {display}\x1b[0m")
        else:
            lines.append(f"  {check} {display}")
    if state.index >= len(state.options):
        lines.append("\x1b[7m  \u2192 Done / 完成\x1b[0m")
    else:
        lines.append("  \u2192 Done / 完成")
    return lines


def _arrow_redraw_output(
    state: _ArrowSelectState, title: str, cols: int, prev_rows: int | None = None
) -> str:
    """Build the full ANSI redraw sequence for the arrow-select menu.

    The sequence rewinds to the first row of the previously drawn frame,
    clears everything below the cursor, then writes the new frame. Lines are
    joined with ``\\r\\n`` (not bare ``\\n``) because the menu runs in raw
    terminal mode (``tty.setraw``), which disables the ``OPOST/ONLCR``
    newline translation — a bare ``\\n`` would only move down without
    returning to column 0, stacking each row diagonally ("staircase /
    spiral" redraw bug).

    ``prev_rows`` must be the number of physical rows the *previous* frame
    occupied (computed with the previous terminal width). Different options
    can wrap to different row counts as the highlight moves, so rewinding by
    the previous frame's height — not the new one's — prevents leftover rows
    from a taller previous frame.
    """
    lines = _arrow_select_lines(state, title)
    rows = _physical_row_count(lines, cols)
    # Reclaim the previously drawn block: rewind to its first row, back to
    # column 0, then clear everything below the cursor.
    move_up = (prev_rows if prev_rows is not None else rows) - 1
    out = ""
    if move_up > 0:
        out += f"\x1b[{move_up}A"
    out += "\r\x1b[0J"
    out += "\r\n".join(lines)
    out += "\r"
    return out


def _arrow_select_available() -> bool:
    """Whether the raw arrow-key selector can run on this platform.

    The selector uses ``termios``/``tty`` which are POSIX-only. On Windows
    (and other platforms where they are unavailable) installation falls back
    to the number-based menu so interactive install never crashes.
    """
    if os.name == "nt":
        return False
    try:
        import termios  # noqa: F401 - presence check only
        import tty  # noqa: F401

        return True
    except ImportError:
        return False


def _prompt_arrow_multi_select(
    options: list[str],
    title: str = "Select items",
    default_all: bool = True,
    preselected: set[str] | None = None,
) -> list[str]:
    """Present an arrow-key multi-select menu (requires a TTY).

    Uses raw terminal mode to read arrow keys, Space and Enter. On a non-TTY
    stdin (pipes, tests) this function is not used; callers fall back to
    ``_prompt_multi_select`` instead. On platforms without ``termios``/``tty``
    (e.g. Windows) this falls back to the number-based menu so it never crashes.

    Args:
        options: List of option identifiers (e.g. assistant keys).
        title: Menu title.
        default_all: Whether all options start selected (ignored when
            ``preselected`` is provided).
        preselected: Optional set of options to start selected (e.g. the
            auto-detected tools). When provided, only these are pre-checked.

    Returns:
        List of selected option identifiers (empty if cancelled).
    """
    if not _arrow_select_available():
        return _prompt_multi_select(
            options,
            input,
            title=title,
            default_all=default_all,
            preselected=preselected,
        )

    import sys as _sys
    import termios
    import tty

    state = _ArrowSelectState(options, default_all, preselected)

    # Hide the block cursor so redraws do not flicker it across the menu.
    _sys.stdout.write("\x1b[?25l")
    _sys.stdout.flush()

    prev_rows = 0

    def redraw() -> None:
        nonlocal prev_rows
        # Re-query the terminal width on every redraw: the window may have
        # been resized since the menu opened, and the previous frame's height
        # (used to rewind) must be computed with the width it was drawn at.
        cols = _terminal_columns()
        _sys.stdout.write(_arrow_redraw_output(state, title, cols, prev_rows))
        _sys.stdout.flush()
        prev_rows = _physical_row_count(_arrow_select_lines(state, title), cols)

    redraw()

    fd = _sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while not state.finished:
            cmd = _read_arrow_key(_sys.stdin)
            if cmd is None:
                continue
            if cmd == "up":
                state.move(-1)
            elif cmd == "down":
                state.move(1)
            elif cmd == "toggle":
                state.toggle_current()
            elif cmd == "cancel":
                state.cancel()
            redraw()
    except KeyboardInterrupt:
        state.cancel()
    finally:
        # A torn-down terminal can make the restore itself fail
        # (``termios.error``); swallow it rather than surfacing a second
        # traceback on top of the cancel that already happened.
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except termios.error:
            pass
        _sys.stdout.write("\x1b[?25h")
        _sys.stdout.write("\n")
        _sys.stdout.flush()

    return state.result


def interactive_select_assistants(
    effective_target: Path,
    input_func: InputFunc = input,
) -> list[str]:
    """Interactively select AI assistants to install to.

    Auto-detects the AI tools already present at the install target directory
    (``effective_target`` — the project root for a project install, the home
    directory for ``--global``) and pre-selects them. Tools that are not
    auto-detected are still listed so the user can pick them manually. When no
    tool is detected, all supported tools are offered for manual selection.

    On an interactive TTY an arrow-key / Space multi-select menu is shown;
    otherwise it falls back to the number-based ``_prompt_multi_select`` so
    the behavior stays testable.

    Args:
        effective_target: Directory where the skill will be installed; tools
            already installed there are detected and pre-selected.
        input_func: Callable used to read user input (non-TTY fallback).

    Returns:
        Sorted list of selected assistant keys. Empty list means the user
        cancelled or selected nothing.
    """
    installed = detect_installed_assistants(effective_target)
    if installed:
        _tui_print("检测到本机已安装的 AI 工具 / Detected AI assistants:", style="iterate.primary")
        for assistant in installed:
            _success(f"  {AI_DISPLAY_NAMES.get(assistant, assistant)}")
        options = installed + sorted(a for a in SUPPORTED_AI if a not in installed)
        # Pre-select only the detected (installed) tools; the rest are shown
        # but unchecked so the user can opt in explicitly. This matches the
        # "detect and pre-select" intent instead of pre-selecting every tool.
        preselected = set(installed)
    else:
        _warning("未检测到已安装的 AI 工具 / No supported AI assistants detected.")
        _hint("可手动选择要安装的工具 / You can select tools manually below.")
        options = sorted(SUPPORTED_AI.keys())
        preselected = set()

    title = "选择要安装的 AI 工具 / Select AI assistants to install to"
    if sys.stdin.isatty() and _arrow_select_available():
        return _prompt_arrow_multi_select(options, title, preselected=preselected)
    return _prompt_multi_select(options, input_func, title, preselected=preselected)


def _effective_target_and_mode_label(target: Path, global_install: bool) -> tuple[Path, str]:
    """Resolve the effective install root and a human-readable mode label.

    A global install targets the user's home directory; a project install
    targets ``target``. The label (" (global)" / "") is used in messages and
    summary boxes. Shared by install / uninstall / update so the three
    commands stay consistent about what "global" means.
    """
    effective_target = Path.home() if global_install else target
    mode_label = " (global)" if global_install else ""
    return effective_target, mode_label


def _safe_confirm(prompt: str, input_func: InputFunc, *, default: bool = False) -> bool | None:
    """Ask a yes/no confirmation safely, even on a non-interactive stdin.

    Mirrors the :func:`install_command` upgrade-prompt guard: on a non-TTY
    stdin (CI, ``</dev/null``, piped job) the builtin ``input()`` would raise
    ``EOFError`` and crash mid-flow. In that case ``None`` is returned so the
    caller can skip the prompt (refusing to act by default is the safe choice).

    Returns:
        - ``True`` — user answered yes ("y"/"yes").
        - ``False`` — user answered no ("n"/"no") or any other input.
        - ``None`` — stdin is not interactive (EOF/TTY), caller should treat
          the confirmation as declined without crashing.
    """
    if not sys.stdin.isatty():
        return None
    try:
        answer = input_func(prompt).strip().lower()
    except EOFError:
        return None
    if answer in ("y", "yes"):
        return True
    if answer in ("n", "no"):
        return False
    return default


def _ask_upgrade_confirmation(
    assistant: str, destination: Path, display_name: str, input_func: InputFunc
) -> bool:
    """Ask whether to overwrite an existing installation (interactive TTY).

    Returns True when the user confirmed the upgrade, False when they declined
    (the assistant is then skipped). Callers must guard this on
    ``sys.stdin.isatty()`` before calling.
    """
    _warning(f"{display_name} 已存在 iterate-skill 安装（可能为旧版本）：{destination}")
    try:
        answer = input_func("  是否覆盖升级到最新版？[Y/n]: ").strip().lower()
    except EOFError:
        # EOF on a TTY (Ctrl-D): decline the overwrite rather than crash.
        return False
    if answer in ("n", "no"):
        _hint(f"Skipped {display_name}：保留现有安装。")
        return False
    return True


def _print_install_summary(
    installed: list[tuple[str, str, Path]], mode_label: str
) -> None:
    """Print the framed installation summary box."""
    summary_lines: list[str] = [
        f"[iterate.success]✓[/] Installed to {len(installed)} assistant(s){mode_label}",
        "",
    ]
    for _assistant, display_name, destination in installed:
        # Escape only the USER-INFLUENCED fragments: display_name comes from
        # the assistant registry but destination is a real filesystem path the
        # operator chose, and rich would silently drop any `[...]` in it as a
        # style tag — hiding the very path the summary exists to show.
        summary_lines.append(
            f"  [iterate.label]{_escape_markup(display_name)}:[/] "
            f"{_escape_markup(str(destination))}"
        )
    summary_lines.append("")
    summary_lines.append(
        "[iterate.hint]Run `iterate onboard` in your project to initialize.[/]"
    )
    _frame_box("Installation Summary", summary_lines)


def install_command(
    ai: str | None,
    target: Path,
    dry_run: bool,
    source: Path,
    force: bool,
    global_install: bool,
    input_func: InputFunc = input,
) -> int:
    """Install the skill for one or more AI assistants.

    Args:
        ai: Target assistant key, "all", or None for interactive selection.
        target: Project or home directory.
        dry_run: Print what would be copied without copying.
        source: Source directory containing skill files.
        force: Overwrite existing skill files.
        global_install: Install into home directory instead of project.
        input_func: Callable used to read user input (interactive mode).

    Returns:
        Exit code: 0 for success, 1 for error/cancel.
    """
    effective_target, mode_label = _effective_target_and_mode_label(target, global_install)

    if ai is None:
        selected = interactive_select_assistants(effective_target, input_func)
        if not selected:
            # A dead-end for CI: the prompt above has no answers to read, so the
            # caller only ever saw "cancelled" and never learned that stdin was
            # the cause or that `--ai` bypasses the prompt entirely.
            if not sys.stdin.isatty():
                _hint(
                    "Non-interactive stdin detected — cannot ask which "
                    "assistants to install. Pass `--ai <assistant>` or "
                    "`--ai all`."
                )
            else:
                _hint("No assistants selected. Installation cancelled.")
            # Non-zero so the npx wrapper does not report a false success.
            return 1
        targets = selected
    else:
        targets = list(SUPPORTED_AI.keys()) if ai == "all" else [ai]

    installed: list[tuple[str, str, Path]] = []
    failed: list[tuple[str, str]] = []
    seen_destinations: set[Path] = set()
    user_declined = 0
    auto_skipped = 0
    for assistant in targets:
        relative_dir = SUPPORTED_AI[assistant]
        destination = effective_target / relative_dir
        display_name = AI_DISPLAY_NAMES.get(assistant, assistant)

        # Some assistants share the identical target directory (e.g. "claude"
        # and "claude-code" both map to ".claude/skills/iterate"), so a run can
        # collide on the same destination. Mark it seen the moment we reach it —
        # not only after a successful copy — so the second alias is skipped even
        # when the first was declined, auto-skipped or failed, instead of being
        # re-prompted for the very same directory.
        if destination in seen_destinations:
            _hint(f"Skipped {assistant}: target {destination} already handled in this run.")
            continue
        seen_destinations.add(destination)

        if dry_run:
            _hint(f"[dry-run] Would install for {assistant}{mode_label} into {destination}")
        else:
            _tui_print(f"Installing for {assistant}{mode_label} into {destination}", style="iterate.primary")

        overwrite = force
        if not dry_run and not force and _is_iterate_install_dir(destination):
            # A previous version of the skill is already present. On an
            # interactive terminal, ask whether to upgrade; otherwise (CI/pipe)
            # keep the existing copy and warn, rather than silently skipping.
            if sys.stdin.isatty():
                if not _ask_upgrade_confirmation(assistant, destination, display_name, input_func):
                    user_declined += 1
                    continue
                overwrite = True
            else:
                _warning(
                    f"{display_name} 已存在 iterate-skill 安装；非交互模式保留现有拷贝，"
                    f"如需覆盖请使用 --force。{destination}"
                )
                auto_skipped += 1

        try:
            copied = copy_skill_files(
                source, destination, dry_run, overwrite, root=effective_target
            )
        except (OSError, ValueError, FileNotFoundError) as exc:
            # A copy failure for one assistant must not abort the whole run:
            # record it and keep installing the remaining assistants, then
            # report the partial outcome with a non-zero exit. This mirrors the
            # per-assistant tolerance of ``update_command``.
            failed.append((assistant, str(exc)))
            continue
        for item in copied:
            _hint(item)

        if copied or dry_run:
            installed.append((assistant, display_name, destination))

    if dry_run:
        _success("Dry run complete; no files were copied.")
        return 0

    if failed:
        # Report a partial installation explicitly instead of a misleading
        # "Installation complete." The <2.0.0 npx wrapper and CI callers rely
        # on exit 0 meaning "every target installed".
        for name, reason in failed:
            _error(f"install failed for {name}: {reason}")
        if installed:
            _error(
                f"Installation incomplete: installed {len(installed)} assistant(s) "
                f"({', '.join(name for name, _, _ in installed)}), failed {len(failed)} "
                f"({', '.join(name for name, _ in failed)})."
            )
        else:
            _error(f"Installation failed for: {', '.join(name for name, _ in failed)}")
        return 1

    if not installed and user_declined == 0 and auto_skipped > 0:
        # Auto-skip no-op: every target already existed on a non-interactive
        # stdin and no copy happened for *any* target. Report this explicitly
        # instead of a misleading "complete": a caller (e.g. the npx wrapper)
        # must be able to distinguish "installed/refreshed" from "nothing
        # happened". A deliberate user decline of an upgrade prompt (or a
        # mixed run that installed at least one assistant) is still a valid
        # outcome and keeps exit 0.
        _warning(
            "Nothing was installed: every target already existed and --force "
            "was not given (non-interactive stdin). Use --force to overwrite."
        )
        return 1

    _success("Installation complete.")
    if installed:
        _print_install_summary(installed, mode_label)
    return 0


def _is_iterate_install_dir(path: Path) -> bool:
    """Whether ``path`` looks like an actual iterate-skill installation.

    Returns True only when ``path`` is a directory (not a symlink), exists,
    and contains ``SKILL.md`` (the canonical skill marker). This guards
    uninstall / update against recursively deleting an unrelated directory
    that happens to live at a configured relative path (e.g. ``skills/iterate``
    for OpenClaw when a project merely has such a directory).
    """
    if not path.exists():
        return False
    if path.is_symlink() or not path.is_dir():
        return False
    return (path / "SKILL.md").is_file()


def uninstall_command(
    ai: str | None,
    target: Path,
    global_install: bool,
    yes: bool = False,
    input_func: InputFunc = input,
) -> int:
    """Remove the skill for one or more AI assistants.

    Args:
        ai: Target assistant key, "all", or None for auto-detect.
        target: Project or home directory.
        global_install: Uninstall from home directory instead of project.
        yes: Skip confirmation prompt.
        input_func: Callable used to read user input.

    Returns:
        Exit code: 0 for success, 1 for error/cancel.
    """
    effective_target, mode_label = _effective_target_and_mode_label(target, global_install)

    if ai is None:
        # Auto-detect existing iterate-skill installations.
        existing_keys = [
            assistant
            for assistant in SUPPORTED_AI
            if _is_iterate_install_dir(effective_target / SUPPORTED_AI[assistant])
        ]
        if not existing_keys:
            _warning(f"No iterate-skill installation found in {effective_target}{mode_label}")
            # "Nothing to uninstall" is a failure for the caller (e.g. the npx
            # wrapper), which must not report success for a no-op.
            return 1
        targets = existing_keys
    else:
        targets = list(SUPPORTED_AI.keys()) if ai == "all" else [ai]

    existing = [
        (assistant, effective_target / SUPPORTED_AI[assistant])
        for assistant in targets
        if _is_iterate_install_dir(effective_target / SUPPORTED_AI[assistant])
    ]
    if not existing:
        _warning(f"No iterate-skill installation found in {effective_target}{mode_label}")
        return 1

    # Several assistant keys are aliases for one directory (`claude` and
    # `claude-code` both resolve to .claude/skills/iterate, likewise gemini).
    # Without de-duplicating, `--ai all` deleted the directory once, then hit
    # the defensive marker re-check for the second alias, reported it as
    # "no SKILL.md marker, refusing to delete", and summed to
    # "Skipped N target(s) that did not look like iterate-skill
    # installations" — a false alarm printed on top of a fully successful
    # uninstall. The first name wins so the confirmation list stays informative.
    deduped: list[tuple[str, Path]] = []
    seen_dirs: set[Path] = set()
    for assistant, destination in existing:
        if destination in seen_dirs:
            continue
        seen_dirs.add(destination)
        deduped.append((assistant, destination))
    existing = deduped

    if not yes:
        _tui_print("The following installations will be removed:", style="iterate.primary")
        for assistant, destination in existing:
            _hint(f"- {assistant}{mode_label}: {destination}")
        confirmed = _safe_confirm("  \u2514 Proceed? [y/N]: ", input_func, default=False)
        if confirmed is not True:
            if confirmed is None:
                # Non-interactive stdin: refuse to delete anything without a
                # confirmed yes (same fail-closed stance as --force).
                _warning("Non-interactive stdin — refusing to uninstall without confirmation. Pass --yes to auto-confirm.")
                return 1
            _hint("Uninstall cancelled.")
            # User declined the confirmation: report non-zero so callers do not
            # mistake the cancellation for a completed uninstall.
            return 1

    skipped: list[tuple[str, Path]] = []
    failed: list[tuple[str, Path, str]] = []
    for assistant, destination in existing:
        if not _is_iterate_install_dir(destination):
            # Defensive re-check just before deletion; SKILL.md may have been
            # removed concurrently, in which case we refuse rather than rmtree
            # an arbitrary directory.
            _warning(f"Skipped (no SKILL.md marker, refusing to delete): {destination}")
            skipped.append((assistant, destination))
            continue
        # One unreadable directory must not abort the whole uninstall: an
        # uncaught OSError here left the user with a traceback, no summary, and
        # no indication that the other assistants were in fact removed.
        try:
            shutil.rmtree(destination)
        except OSError as exc:
            _warning(f"Failed to remove {assistant}{mode_label}: {exc}")
            failed.append((assistant, destination, str(exc)))
            continue
        _success(f"Uninstalled {assistant}{mode_label}: {destination}")

    if skipped:
        _warning(f"Skipped {len(skipped)} target(s) that did not look like iterate-skill installations.")
    if failed:
        _warning(f"Failed to remove {len(failed)} target(s) — check file permissions.")
        return 1
    _success("Uninstall complete.")
    return 0


def _select_skill_release(releases: object) -> dict[str, object] | None:
    """Pick the newest published release that actually carries the skill tarball.

    Args:
        releases: Decoded ``/releases`` list payload from the GitHub API.

    Returns:
        The first release object (API order is newest-published first) that is
        not a draft, not a prerelease, and ships ``iterate-skill.tar.gz``; or
        None when the list holds no such release.
    """
    if not isinstance(releases, list):
        return None
    for release in releases:
        if not isinstance(release, dict):
            continue
        if release.get("draft") or release.get("prerelease"):
            continue
        assets = release.get("assets")
        if not isinstance(assets, list):
            continue
        names = {asset.get("name") for asset in assets if isinstance(asset, dict)}
        if EXPECTED_TARBALL_FILENAME in names:
            return release
    return None


def _fetch_latest_release_info(
    token: str | None,
) -> tuple[dict[str, str] | None, str | None]:
    """Query GitHub API for the latest release tag, tarball URL and checksum asset URL.

    Returns ``(info, error_reason)`` — on success ``error_reason`` is None; on
    failure ``info`` is None and ``error_reason`` carries the concrete cause
    (HTTP status such as 401 for an invalid token, timeout, DNS failure, ...)
    so the caller can surface it instead of a generic "could not reach GitHub".
    """
    request = urllib.request.Request(RELEASES_API_URL, method="GET")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    try:
        with _urlopen(request, GITHUB_API_TIMEOUT_SECONDS) as response:
            # Read the API payload through the same bounded-loop discipline
            # used by _download_bytes: an API response that exceeds the cap is
            # rejected instead of exhausting memory on an unbounded read().
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = response.read(_DOWNLOAD_CHUNK_SIZE)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    return None, (
                        f"GitHub API response body exceeds {MAX_DOWNLOAD_BYTES} "
                        f"byte safety cap (downloaded {total} bytes)"
                    )
                chunks.append(chunk)
            payload = json.loads(b"".join(chunks).decode("utf-8"))
    except urllib.error.HTTPError as exc:
        reason = f"GitHub API returned HTTP {exc.code}"
        if exc.code == 401:
            reason += " (token may be invalid or expired)"
        elif exc.code == 403:
            reason += " (rate limit exceeded; retry with --token)"
        return None, reason
    except urllib.error.URLError as exc:
        return None, f"GitHub API network error: {exc.reason}"
    except TimeoutError:
        return None, (
            f"GitHub API request timed out after {GITHUB_API_TIMEOUT_SECONDS}s"
        )
    except http.client.HTTPException as exc:
        return None, f"GitHub API connection error: {exc}"
    except OSError as exc:
        # Bare OSError catches what the specific handlers above cannot:
        # ConnectionResetError / ssl.SSLError raised mid-read() are OSError
        # subclasses but NOT URLError subclasses, and used to escape this
        # function as an unhandled traceback (updater.py already had this
        # guard; install.py must not regress the same path).
        return None, f"GitHub API connection error: {exc}"
    except json.JSONDecodeError as exc:
        return None, f"GitHub API returned invalid JSON: {exc}"
    except Exception as exc:  # noqa: BLE001 — CLI boundary: clean reason, never traceback
        return None, f"GitHub API request failed: {exc}"

    if not isinstance(payload, list):
        return None, "GitHub API returned an unexpected payload shape"

    data = _select_skill_release(payload)
    if data is None:
        return None, (
            f"no published release in the last 100 carries an "
            f"{EXPECTED_TARBALL_FILENAME} asset"
        )

    tag = data.get("tag_name")
    if not isinstance(tag, str):
        return None, "GitHub API response is missing tag_name"

    tarball_url: str | None = None
    checksum_url: str | None = None
    signature_url: str | None = None
    assets = data.get("assets")
    if isinstance(assets, list):
        for asset in assets:
            if not isinstance(asset, dict):
                continue
            name = asset.get("name")
            asset_url = asset.get("browser_download_url")
            if not isinstance(asset_url, str):
                continue
            if name == EXPECTED_TARBALL_FILENAME:
                tarball_url = asset_url
            elif name == CHECKSUMS_ASSET_NAME:
                checksum_url = asset_url
            elif name == SIGNATURE_ASSET_NAME:
                signature_url = asset_url

    if not isinstance(tarball_url, str):
        return None, f"release has no {EXPECTED_TARBALL_FILENAME} asset"

    result: dict[str, str] = {"tag": tag, "tarball_url": tarball_url}
    if checksum_url:
        result["checksum_url"] = checksum_url
    if signature_url:
        result["signature_url"] = signature_url
    return result, None


def _safe_extractall(tar: tarfile.TarFile, path: Path) -> None:
    """Extract a tarball safely, preventing path traversal and decompression bombs.

    Enforces three guarantees over the full member list BEFORE extracting:
      1. no member path escapes ``path`` (traversal / zip-slip),
      2. no symlink/hard-link target escapes ``path``,
      3. the total *uncompressed* size stays under ``MAX_EXTRACT_BYTES`` and
         every individual member under it too (a tiny compressed tarball must
         not decompress into hundreds of GiB on disk).

    Checks (1) and (2) are applied on EVERY Python version, not only the
    ``filter="data"`` path: the containment guarantee must not depend on the
    interpreter (the device/fifo guard below is enforced the same way). On
    Python 3.12+ ``filter="data"`` is still passed to ``extractall`` as
    defence in depth.
    """
    members = tar.getmembers()
    base = path.resolve()
    total_uncompressed = 0
    for member in members:
        if member.size > MAX_EXTRACT_MEMBER_BYTES:
            raise tarfile.TarError(
                f"Suspicious member size: {member.name} is {member.size} bytes "
                f"(> {MAX_EXTRACT_MEMBER_BYTES})"
            )
        total_uncompressed += member.size
        if total_uncompressed > MAX_EXTRACT_BYTES:
            raise tarfile.TarError(
                f"Archive expands to > {MAX_EXTRACT_BYTES} bytes uncompressed "
                f"(decompression-bomb guard)"
            )
        # Device/fifo members must never be created on disk: creating them
        # usually requires privileges and they are never legitimate content of
        # a skill release. Enforced on every Python version (the 3.12+
        # ``filter="data"`` path drops them silently; here they are refused
        # outright so the policy and its test are version-independent).
        if member.isdev() or member.isfifo():
            raise tarfile.TarError(
                f"Refusing device/fifo member in archive: {member.name}"
            )
        # The member's OWN path must resolve inside the destination. Uses
        # is_relative_to (platform-agnostic) instead of a hardcoded "/" join,
        # which would break on Windows backslash separators.
        member_path = (path / member.name).resolve()
        if not member_path.is_relative_to(base):
            raise tarfile.TarError(f"Suspicious member path: {member.name}")
        # Symlinks are the classic escape vector even when their own path is
        # inside the destination: the link *target* may point outside it.
        # Absolute targets and relative targets that climb out of the
        # destination are both rejected here. A symlink's target is resolved
        # relative to the LINK's own directory (POSIX semantics, and what
        # ``filter="data"`` does).
        if member.issym():
            link_target = (path / member.name).parent / member.linkname
            if not link_target.resolve().is_relative_to(base):
                raise tarfile.TarError(
                    f"Suspicious symlink target in member {member.name}: {member.linkname}"
                )
        # Hard links are equally dangerous: extracting a hard link whose
        # linkname resolves outside the destination would create a file entry
        # pointing at an arbitrary file on disk. A hard link's ``linkname`` is
        # an archive-root-relative path (NOT relative to the link's directory),
        # so it must be resolved against ``base`` — resolving it against the
        # member's parent let a link in a subdirectory (``a/b/evil`` ->
        # ``../outside``) slip past the guard even though the archive root
        # resolution escapes.
        if member.islnk():
            link_target = (base / member.linkname).resolve()
            if not link_target.is_relative_to(base):
                raise tarfile.TarError(
                    f"Suspicious hard link target in member {member.name}: {member.linkname}"
                )

    if hasattr(tarfile, "data_filter"):
        tar.extractall(path=path, filter="data")
    else:
        tar.extractall(path=path)


def _download_bytes(
    url: str, token: str | None, timeout: int = DOWNLOAD_TIMEOUT_SECONDS
) -> tuple[bytes | None, str | None]:
    """Download raw bytes from a URL, optionally using a GitHub token.

    The token is only attached when the URL targets the GitHub API host
    (``api.github.com``). Release-asset URLs (``release-assets.githubusercontent.com``)
    are public and must not receive the caller's PAT, keeping credential surface
    minimal.

    The response is streamed in bounded chunks: when the total exceeds
    ``MAX_DOWNLOAD_BYTES`` the download is aborted and an error reason is
    returned, so a misbehaving upstream cannot exhaust memory.

    Returns ``(data, error_reason)`` — on success ``error_reason`` is None; on
    failure ``data`` is None and ``error_reason`` carries the concrete cause
    (HTTP status such as 401 for an invalid token, timeout, DNS failure, ...).
    """
    request = urllib.request.Request(url, method="GET")
    request.add_header("Accept", "application/vnd.github+json")
    if token and _is_github_api_url(url):
        request.add_header("Authorization", f"Bearer {token}")

    try:
        with _urlopen(request, timeout) as response:
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = response.read(_DOWNLOAD_CHUNK_SIZE)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    return None, (
                        f"response body exceeds {MAX_DOWNLOAD_BYTES} byte safety cap "
                        f"(downloaded {total} bytes)"
                    )
                chunks.append(chunk)
            return b"".join(chunks), None
    except urllib.error.HTTPError as exc:
        reason = f"HTTP {exc.code}"
        if exc.code == 401:
            reason += " (token may be invalid or expired)"
        elif exc.code == 403:
            reason += " (rate limit exceeded or access forbidden)"
        return None, f"download failed: {reason}"
    except urllib.error.URLError as exc:
        return None, f"network error: {exc.reason}"
    except TimeoutError:
        return None, f"request timed out after {timeout}s"
    except http.client.HTTPException as exc:
        return None, f"connection error: {exc}"
    except OSError as exc:
        # ConnectionResetError / ssl.SSLError raised mid-read() are OSError
        # subclasses but NOT URLError subclasses; without this arm a dropped
        # connection surfaced as an unhandled traceback instead of a clean
        # error reason (updater.py's twin function already had this guard).
        return None, f"connection error: {exc}"
    except ValueError as exc:
        return None, f"invalid response: {exc}"
    except Exception as exc:  # noqa: BLE001 — CLI boundary: clean reason, never traceback
        return None, f"download failed: {exc}"


def _is_github_api_url(url: str) -> bool:
    """True when ``url`` targets the GitHub API host over HTTPS.

    Uses a netloc prefix check (hostname.lower() starts with ``api.github.com``)
    so a rogue ``https://api.github.com.evil`` cannot match, and requires the
    ``https`` scheme: a ``http://api.github.com/...`` URL (a hostile redirect or
    a hand-crafted asset URL) would otherwise receive the PAT in cleartext.
    """
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return False
    if parts.scheme.lower() != "https":
        return False
    host = (parts.hostname or "").lower()
    return host == "api.github.com" or host.endswith(".api.github.com")


def _origin(url: str) -> tuple[str, str, int | None]:
    """Return ``(scheme, hostname, port)`` for a URL, normalised for comparison.

    Used by the redirect handler: comparing hostnames alone let a same-host
    ``https -> http`` (or ``:443 -> :8443``) downgrade keep the Authorization
    header, i.e. the PAT was carried to a different origin in cleartext.
    """
    parts = urllib.parse.urlsplit(url)
    scheme = parts.scheme.lower()
    default_port = 443 if scheme == "https" else 80 if scheme == "http" else None
    return (scheme, (parts.hostname or "").lower(), parts.port or default_port)


class _SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """HTTP redirect handler that strips credentials on cross-host redirects.

    urllib's default redirect handler forwards custom headers (including
    ``Authorization: Bearer <PAT>``) verbatim to a 301/302/307 Location even
    when that target is a different origin. If a GitHub response — or an
    on-path proxy — ever redirects cross-host, the PAT would be transmitted to
    the third party. This handler drops ``Authorization`` whenever the request
    host changes, so a token attached to ``api.github.com`` can never leak to
    another origin.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_req is None:
            return None
        try:
            same_origin = _origin(req.full_url) == _origin(newurl)
        except ValueError:
            # Unparseable/invalid port: treat it as a different origin.
            same_origin = False
        if not same_origin:
            new_req.remove_header("Authorization")
        return new_req


def _safe_opener() -> urllib.request.OpenerDirector:
    """Build an opener whose cross-host redirects never carry credentials.

    Used by every network request in this module so the PAT is stripped on any
    redirect that leaves the GitHub host (see ``_SafeRedirectHandler``).
    """
    return urllib.request.build_opener(_SafeRedirectHandler())


def _urlopen(request: urllib.request.Request, timeout: int | None = None):
    """Open ``request`` through the credential-safe opener.

    Module-level seam so tests can patch ``install._urlopen`` without losing
    the real cross-host redirect protection in production.
    """
    return _safe_opener().open(request, timeout=timeout)


#: A SHA-256 digest is exactly 64 hex characters. Used by the checksum parser
#: so malformed entries (``+abc…``, ``0xabc…``, short strings) are skipped
#: exactly as the npx installer's ``parseChecksums`` skips them.
_SHA256_HEX_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _parse_checksum(checksum_text: bytes, filename: str) -> str | None:
    """Parse a SHA256SUMS-style file and return the hash for ``filename``.

    Only a full SHA-256 digest (exactly 64 hex characters) is accepted: any
    other value can never be the output of ``hashlib.sha256(data).hexdigest()``
    used by the verifier, so a non-hex or truncated digest is treated as a
    malformed entry (skipped) rather than compared as if it were a real hash.
    A body that is not valid UTF-8 is treated as malformed too (None) instead
    of leaking an uncaught ``UnicodeDecodeError``; the caller then refuses to
    proceed. Two conflicting digests for the same basename also yield None:
    a self-contradictory checksum file must never be trusted (parity with the
    npx installer's parseChecksums).
    """
    try:
        text = checksum_text.decode("utf-8")
    except UnicodeDecodeError:
        return None
    found: str | None = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        digest, name = parts
        # Strict 64-hex match: ``int(digest, 16)`` also accepted forms like
        # "+abc…", "-abc…" and "0xabc…" that can never be a real digest, so the
        # two installers disagreed about the same malformed file (JS uses
        # ^[0-9a-fA-F]{64}$). Either way the comparison would fail closed, but
        # the error text differed ("mismatch" vs "not found in checksum file").
        if not _SHA256_HEX_RE.match(digest):
            continue
        # Handle "HASH  filename", "HASH *filename" and "HASH ./filename"
        # formats (the ``./`` prefix is common for tarballs stored at repo root).
        # Match on the basename so checksum entries with a subpath prefix or a
        # vaguely versioned file component (e.g. ``dist/iterate-skill.tar.gz`` or
        # ``release/iterate-skill-1.2.3.tar.gz``) still resolve to the expected
        # asset instead of being rejected as "not found".
        name = name.lstrip("*").strip()
        name = name.removeprefix("./")
        if os.path.basename(name) != filename:
            continue
        candidate = digest.lower()
        if found is not None and found != candidate:
            # Two CONFLICTING entries for the same asset make the file
            # untrustworthy (the npx installer rejects it outright): return
            # None so the caller refuses the release, instead of silently
            # trusting whichever line happened to come first.
            return None
        found = candidate
    return found


def _download_release_source(
    tarball_url: str,
    checksum_url: str | None,
    token: str | None,
    signature_url: str | None = None,
) -> Path | None:
    """Download a release tarball, verify checksum + signature, and extract it.

    Refuses to proceed if ``checksum_url`` is None or if the checksum
    cannot be verified. Because the SHA256SUMS file is fetched from the
    SAME release as the tarball, this guards against transport corruption
    and asset mis-pairing; it cannot defend against a release that is
    itself compromised at the source — that trust anchor is the MANDATORY
    detached GPG signature (``signature_url``), verified against the pinned
    public key (``ITERATE_SIGNING_PUBLIC_KEY``) below.

    Raises:
        ReleaseIntegrityError: When the release was CHECKSUMMED but failed
            verification (no matching checksum entry, or a SHA-256 mismatch),
            when the signature is missing/unverifiable, or when the archive is
            unusable. Callers must fail closed on this — never fall back to a
            different source while claiming the release applied.
        ReleaseStructureError: When the verified archive is unusable (extraction
            failed, or it does not contain exactly one top-level directory with a
            ``SKILL.md`` marker). Callers must abort — a broken release must not
            silently fall back to a possibly-different local source.

    Returns:
        The extracted ``SKILL.md`` root directory, or ``None`` when the
        tarball OR the checksum file could not be downloaded (a pure network
        failure, which legitimately allows falling back to the local source;
        the unverified bytes are discarded either way).
    """
    if not checksum_url:
        raise ReleaseIntegrityError("SHA256SUMS.txt URL is required for integrity verification.")

    data, tarball_error = _download_bytes(tarball_url, token)
    if data is None:
        if tarball_error:
            _error(f"Could not download release tarball: {tarball_error}")
        return None

    checksum_data, checksum_error = _download_bytes(checksum_url, token)
    if not checksum_data:
        # A checksum file we could not FETCH is a transport problem, not an
        # integrity failure — the same class as the tarball fetch failing
        # above. Fall back to the trusted local source (discarding the
        # unverified tarball bytes entirely) instead of aborting the whole
        # update: we never install the unverified download, so the
        # fail-closed property still holds.
        if checksum_error:
            _warning(
                f"Could not download checksum file ({checksum_error}); "
                "discarding the unverified tarball."
            )
        else:
            _warning(
                "Could not download checksum file; discarding the unverified tarball."
            )
        return None
    # Everything below is a genuine INTEGRITY verdict: the checksum was
    # retrieved and the release failed to satisfy it. These abort.
    expected_hash = _parse_checksum(checksum_data, EXPECTED_TARBALL_FILENAME)
    if not expected_hash:
        raise ReleaseIntegrityError(f"{EXPECTED_TARBALL_FILENAME} not found in checksum file.")

    actual_hash = hashlib.sha256(data).hexdigest()
    # Constant-time compare: the expected hash is attacker-influenced (it
    # travels over the network with the tarball), so early-exit string !=
    # would leak prefix information usable to forge a checksum.
    if not hmac.compare_digest(actual_hash.lower(), expected_hash.lower()):
        raise ReleaseIntegrityError(
            f"Checksum mismatch for release tarball: expected {expected_hash}, got {actual_hash}"
        )
    _success("Release tarball checksum verified.")

    try:
        temp_dir = Path(tempfile.mkdtemp(prefix="iterate-release-"))
    except OSError as exc:
        # mkdtemp failure (TMPDIR unwritable / disk full) must not escape as a
        # raw traceback past the ReleaseStructureError/ReleaseIntegrityError
        # handlers in update_command; surface it as a clean structure error.
        raise ReleaseStructureError(
            f"could not create a temporary directory: {exc}"
        ) from exc
    # The extracted tree is returned to the caller, who owns it and removes its
    # parent afterwards — so it must survive this function on SUCCESS only. On
    # every failure path (including ``ReleaseIntegrityError`` from the signature
    # gate, which is NOT in the except tuple below) the ``finally`` below removes
    # the temp dir; without it a failed signature check leaked one
    # ``iterate-release-*`` directory per attempt.
    keep_temp_dir = False
    try:
        # Mandatory authenticity gate (see _enforce_signature_policy): the
        # signature is written next to the tarball inside the temp dir so gpg
        # can verify it, then the whole temp dir is either extracted into or
        # removed on failure.
        signature_bytes: bytes | None = None
        if signature_url:
            signature_bytes, signature_error = _download_bytes(signature_url, token)
            if signature_bytes is None:
                raise ReleaseIntegrityError(
                    "could not download the release signature "
                    f"({signature_error or 'unknown error'})"
                )
        tarball_path = temp_dir / EXPECTED_TARBALL_FILENAME
        tarball_path.write_bytes(data)
        signature_path: Path | None = None
        if signature_bytes is not None:
            signature_path = temp_dir / SIGNATURE_ASSET_NAME
            signature_path.write_bytes(signature_bytes)
        signature_ok, signature_detail = _enforce_signature_policy(
            tarball_path, signature_path
        )
        if not signature_ok:
            raise ReleaseIntegrityError(signature_detail)

        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
            _safe_extractall(tar, temp_dir)
            root_candidates = [p for p in temp_dir.iterdir() if p.is_dir()]
            skill_roots = [d for d in root_candidates if (d / "SKILL.md").is_file()]
            if len(skill_roots) != 1:
                raise ReleaseStructureError(
                    "release tarball must contain exactly one top-level directory "
                    "with a SKILL.md marker, "
                    f"found {len(skill_roots)}."
                )
            keep_temp_dir = True
            return skill_roots[0]
    except (tarfile.TarError, OSError, EOFError, ValueError, zlib.error):
        # A checksum-verified archive that cannot be extracted is a broken
        # release, not a network flake: abort instead of falling back to local
        # and silently installing a different source tree. zlib.error (corrupt
        # deflate stream) / EOFError (truncated gzip) / ValueError are NOT
        # TarError/OSError subclasses — without them a damaged-but-correctly-
        # checksummed archive raised a raw traceback (same fix as
        # updater._download_verified_release; keep the two in sync).
        raise ReleaseStructureError("release tarball could not be extracted.")
    finally:
        if not keep_temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)


def _update_one_assistant(
    assistant: str,
    target: Path,
    update_source: Path,
    global_install: bool,
    input_func: InputFunc,
) -> int:
    """Refresh a single assistant's install; returns ``install_command``'s exit code.

    ``update`` semantically means "refresh the installed copy to the latest
    version", so it must overwrite existing files rather than skip them.
    """
    return install_command(
        ai=assistant,
        target=target,
        dry_run=False,
        source=update_source,
        force=True,
        global_install=global_install,
        input_func=input_func,
    )


def update_command(
    ai: str | None,
    target: Path,
    source: Path,
    token: str | None,
    global_install: bool,
    yes: bool = False,
    input_func: InputFunc = input,
) -> int:
    """Refresh installed skill files from the latest GitHub release or local source.

    Args:
        ai: Target assistant key, "all", or None for auto-detection.
        target: Project or home directory.
        source: Local source directory (fallback when no release is available).
        token: GitHub Personal Access Token (optional, for rate limits).
        global_install: Update the home-directory installation instead.
        yes: Skip the download confirmation prompt.
        input_func: Callable used to read user input (injectable for tests).

    Returns:
        Exit code: 0 for success, 1 for error/cancel.
    """
    effective_target, mode_label = _effective_target_and_mode_label(target, global_install)

    # Fail fast on a malformed --token: GitHub would otherwise reject the
    # request with a 401 and we would silently fall back to local source,
    # hiding the typo from the user.
    # Normalise ONCE, then validate and USE the same value. The old code
    # validated ``token.strip()`` but kept the raw string, so a whitespace-only
    # token passed validation as "absent" while ``if token:`` still attached
    # ``Authorization: Bearer    `` (401 + rate-limit burn), and an embedded
    # newline made ``putheader()`` raise with the PAT in the message.
    token = (token.strip() or None) if isinstance(token, str) else token
    token_error = _validate_github_token(token)
    if token_error:
        _error(token_error)
        return 1

    release_info, release_error = _fetch_latest_release_info(token)
    release_source: Path | None = None
    if release_info:
        _tui_print(f"Latest GitHub release: {release_info['tag']}", style="iterate.primary")
        _hint(f"This will download code from https://github.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/releases and install it into your AI assistant skill directories.")
        has_checksum = "checksum_url" in release_info
        if not has_checksum:
            # A release without integrity metadata can never be verified: fail
            # closed rather than silently upgrading from the local checkout
            # while reporting "Update complete." (exit 0).
            _error(
                "Error: no SHA256SUMS.txt asset found for this release. "
                "Refusing to update without integrity verification. "
                "Run again when the release carries checksums, or update manually "
                "from a local source with confidence in its origin."
            )
            return 1
        if not yes:
            confirmed = _safe_confirm("Continue? [y/N]: ", input_func, default=False)
            if confirmed is None:
                # Non-interactive stdin (CI/pipe/</dev/null). _safe_confirm
                # returns None rather than raising EOFError, but reporting
                # "Update cancelled." left the caller guessing *why* — and
                # `--yes` is the flag written for exactly this case.
                _hint(
                    "Non-interactive stdin detected. Pass `update --yes` to "
                    "update without a prompt."
                )
                return 1
            if confirmed is not True:
                _hint("Update cancelled.")
                return 1
        _hint("Downloading release source...")
        try:
            release_source = _download_release_source(
                release_info["tarball_url"],
                release_info["checksum_url"],
                token,
                release_info.get("signature_url"),
            )
        except ReleaseIntegrityError as exc:
            # Integrity failure (checksum retrieved but no matching entry, or a
            # SHA mismatch) must abort — never fall back to local and claim
            # "Update complete." for an unverified release. (A checksum file
            # that could not be DOWNLOADED is not this case: it returns None
            # and falls back below, with the unverified tarball discarded.)
            _error(f"Refusing to update from release: {exc}")
            return 1
        except ReleaseStructureError as exc:
            # The release checksum-verified but its archive is unusable: abort
            # rather than install a locally-checked-out tree that may differ
            # from the broken release.
            _error(f"Refusing to update from release: {exc}")
            return 1
        if release_source:
            _hint(f"Using release source: {release_source}")
        else:
            _warning("Could not download release source; falling back to local source...")
    else:
        _warning("Could not reach GitHub releases; refreshing from local source...")
        if release_error:
            _hint(f"Reason: {release_error}")

    update_source = release_source if release_source else source

    if ai is None:
        assistants = detect_installed_assistants(effective_target)
        if not assistants:
            _warning(f"No iterate-skill installation found in {effective_target}{mode_label}")
            _hint("Run 'install --ai <assistant>' first, or use 'update --ai <assistant>'.")
            return 1
        _tui_print(f"Updating detected installations: {', '.join(assistants)}", style="iterate.primary")
    elif ai == "all":
        assistants = list(SUPPORTED_AI.keys())
    else:
        assistants = [ai]

    # Update every target assistant, tracking which succeeded and which failed
    # so a mid-run failure is reported explicitly instead of silently leaving a
    # partially-updated state behind (and never printing a false "complete").
    updated: list[str] = []
    failed: list[tuple[str, str]] = []
    # Some assistants share one destination (claude/claude-code →
    # .claude/skills/iterate). Update it once; the second alias would otherwise
    # trigger a redundant full copy of the tree.
    seen_destinations: set[Path] = set()
    try:
        for assistant in assistants:
            effective_target, _ = _effective_target_and_mode_label(
                target, global_install
            )
            relative_dir = SUPPORTED_AI[assistant]
            destination = effective_target / relative_dir
            if destination in seen_destinations:
                # A second alias for an already-UPDATED destination (claude /
                # claude-code share one dir) is genuinely covered by the first
                # copy, so it is counted as handled — but only when the first
                # alias actually SUCCEEDED (a failed first alias must not make
                # its twin look updated). seen_destinations is populated only
                # after a successful update, so a failed first alias falls
                # through and the twin gets a real (honest) attempt/report.
                _hint(
                    f"Skipped {assistant}: target {destination} already updated in this run."
                )
                updated.append(assistant)  # count it as handled, not a failure
                continue
            try:
                code = _update_one_assistant(
                    assistant, target, update_source, global_install, input_func
                )
            except (OSError, ValueError, tarfile.TarError) as exc:
                failed.append((assistant, str(exc)))
                continue
            if code != 0:
                failed.append((assistant, f"installer exited with code {code}"))
            else:
                updated.append(assistant)
                seen_destinations.add(destination)
    finally:
        if release_source:
            # release_source is always a subdir of a mkdtemp parent; remove the
            # whole temp dir (subdir + parent) so no empty mkdtemp dir leaks.
            shutil.rmtree(release_source.parent, ignore_errors=True)

    if failed:
        if updated:
            _error(
                f"Update incomplete: updated {len(updated)} assistant(s) "
                f"({', '.join(updated)}), failed {len(failed)} ({', '.join(name for name, _ in failed)})."
            )
        else:
            _error(f"Update failed for: {', '.join(name for name, _ in failed)}")
        for name, reason in failed:
            _hint(f"  - {name}: {reason}")
        return 1

    _success("Update complete.")
    return 0


def _validate_timeout_seconds() -> float:
    """Return the validate.py subprocess timeout in seconds.

    ``ITERATE_VALIDATE_TIMEOUT`` overrides the default for constrained
    environments (slow disks, emulated CI). Invalid/non-positive values are
    ignored so a typo can never disable the safety net (``timeout=0`` would
    make every validation fail immediately).
    """
    raw = os.environ.get(VALIDATE_TIMEOUT_ENV, "").strip()
    if raw:
        try:
            value = float(raw)
        except ValueError:
            value = 0
        if value > 0:
            return value
    return float(VALIDATE_SUBPROCESS_TIMEOUT_SECONDS)


def _run_validate_subprocess(
    source: Path, config_path: Path, schema_path: Path, dimensions_dir: Path
) -> list[str]:
    """Run ``scripts/validate.py config`` as a subprocess and return errors.

    Uses subprocess instead of ``importlib`` dynamic execution so that
    static analyzers do not flag the skill for ``exec_module`` usage.
    The validate script is part of this skill's own source tree.
    """
    import subprocess

    validate_script = source / "scripts" / "validate.py"
    if not validate_script.exists():
        return [f"validate.py not found at {validate_script}"]

    cmd = [
        sys.executable,
        str(validate_script),
        "config",
        str(config_path),
        str(schema_path),
        str(dimensions_dir),
    ]
    timeout = _validate_timeout_seconds()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired:
        return [
            (
                f"validate.py did not finish within {timeout:g}s (the config "
                "was not changed). Retry on a less loaded machine, or raise "
                f"the limit with {VALIDATE_TIMEOUT_ENV}=300."
            )
        ]
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"Failed to run validate.py: {exc}"]

    if result.returncode == 0:
        return []

    errors: list[str] = []
    for line in result.stderr.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            errors.append(stripped[2:])
        elif stripped and not stripped.startswith("Validation failed"):
            errors.append(stripped)
    # Also surface stdout lines: some validate frontends write diagnostics to
    # stdout rather than stderr, and dropping them would degrade the error
    # report to a generic message. Deduplicate while preserving order.
    if not errors:
        for line in result.stdout.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            detail = stripped.removeprefix("- ")
            if detail and detail not in errors and not detail.startswith("Validation failed"):
                errors.append(detail)
    return errors if errors else ["Validation failed (see stderr for details)"]


def validate_command(target: Path, source: Path) -> int:
    """Validate the project-level iterate.config.yaml."""
    config_path = target / "iterate.config.yaml"
    schema_path = source / "config" / "config.schema.json"
    dimensions_dir = source / "config" / "dimensions"

    if not config_path.exists():
        _warning(f"No project config found at {config_path}")
        return 1

    errors = _run_validate_subprocess(source, config_path, schema_path, dimensions_dir)
    if errors:
        _error(f"Validation failed for {config_path}")
        for error in errors:
            _hint(f"- {error}")
        return 1

    _success(f"Validation passed: {config_path}")
    return 0


def _validate_project_config(target: Path, source: Path) -> list[str]:
    """Validate the saved project config and return errors."""
    config_path = target / "iterate.config.yaml"
    schema_path = source / "config" / "config.schema.json"
    dimensions_dir = source / "config" / "dimensions"
    return _run_validate_subprocess(source, config_path, schema_path, dimensions_dir)


YAML_BOOLEAN_ALIASES = {"true", "false", "True", "False", "TRUE", "FALSE"}

#: YAML 1.1 boolean-like spellings that PyYAML parses to bool but which are
#: NOT in ``YAML_BOOLEAN_ALIASES`` (so ``parse_value`` keeps them as strings
#: for free-form string fields). They are valid boolean spellings for a
#: boolean-typed config field and must be coerced there.
_YAML_BOOL_LIKE = {
    "yes", "no", "on", "off", "y", "n",
    "Yes", "No", "On", "Off", "Y", "N",
    "YES", "NO", "ON", "OFF",
    "true", "false", "True", "False", "TRUE", "FALSE",
}


def _config_boolean_paths(schema_path: Path) -> set[str]:
    """Return the dotted config paths the schema declares as ``type: boolean``.

    Traverses the JSON Schema ``properties`` tree so ``--set`` can coerce a
    YAML-1.1 boolean spelling (``yes``/``no``/``on``/``off``) to a real bool on
    exactly the fields the schema expects a boolean, while leaving string
    fields (``goal``, ``target_branch``) untouched.

    Args:
        schema_path: Path to ``config/config.schema.json``.

    Returns:
        The set of dotted paths whose schema type is ``boolean``.
    """
    result: set[str] = set()
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return result

    def _walk(node: object, prefix: str) -> None:
        if not isinstance(node, dict):
            return
        if node.get("type") == "boolean":
            result.add(prefix)
            return
        props = node.get("properties")
        if not isinstance(props, dict):
            return
        for name, child in props.items():
            _walk(child, f"{prefix}.{name}" if prefix else str(name))

    _walk(schema, "")
    return result


def parse_bool_spelling(raw: str) -> bool:
    """Parse a boolean config value from its string spelling.

    Accepts the YAML-1.1 spellings a user types for a boolean field
    (``yes``/``no``/``on``/``off``/``y``/``n`` plus ``true``/``false`` in any
    case). Rejects anything else so a mistyped value fails loudly instead of
    being silently stored as a string the schema then rejects.

    Args:
        raw: The raw string value.

    Returns:
        The parsed bool.

    Raises:
        ValueError: If ``raw`` is not a recognised boolean spelling.
    """
    normalized = raw.strip().lower()
    if normalized in ("1", "true", "yes", "on", "y"):
        return True
    if normalized in ("0", "false", "no", "off", "n"):
        return False
    raise ValueError(f"{raw!r} is not a boolean value (expected yes/no/on/off/true/false)")


def parse_value(raw: str) -> object:
    """Parse a config value from CLI string using JSON, then YAML semantics.

    JSON is tried first so a value that is a valid JSON literal takes strict
    JSON semantics (e.g. ``{"a": 1}``); constructs that only exist in YAML
    (bare lists like ``[correctness, security]``, block mappings, dates)
    then fall back to YAML. YAML 1.1 treats yes/no/on/off as booleans; we keep
    only explicit true/false as bool to avoid surprising behavior in free-form
    strings.
    """
    stripped = raw.strip()
    if not stripped:
        return ""

    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        try:
            parsed = yaml.safe_load(stripped)
        except yaml.YAMLError:
            parsed = stripped

    if isinstance(parsed, bool) and stripped not in YAML_BOOLEAN_ALIASES:
        return stripped

    # YAML 1.1 parses an unquoted date-like string (``2024-01-01``) as a
    # datetime.date object. A string field such as ``git.target_branch`` that a
    # user legitimately sets to a date-shaped value (a tag/branch/version named
    # after a date) would then be stored as a date and fail schema validation
    # with a confusing "changes have been reverted" — instead of keeping the
    # literal string the user typed. Convert temporal scalars back to the raw
    # text; JSON-first values (numbers/bools/lists) are unaffected.
    if isinstance(parsed, (datetime.datetime, datetime.date, datetime.time)):
        return stripped

    return parsed


def set_nested_value(config: dict[str, object], key: str, value: object) -> None:
    """Set a possibly nested config key, creating intermediate mappings.

    Raises:
        ValueError: When ``key`` is empty, or contains an empty segment
            (e.g. ``a..b`` or ``dimensions.``), which would otherwise create a
            phantom empty-string mapping level.
    """
    parts = key.split(".")
    if not key or any(not part for part in parts):
        raise ValueError(f"nested key must not contain empty segments: {key!r}")
    current = config
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value


def load_config(path: Path) -> dict[str, object]:
    """Load a YAML config file or return an empty mapping."""
    if not path.exists():
        return {}

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc
    except (OSError, UnicodeDecodeError) as exc:
        # UnicodeDecodeError (non-UTF-8 bytes) inherits ValueError, not
        # YAMLError — without this clause a binary/locale-encoded config
        # would crash with a raw traceback instead of a clean message.
        raise OSError(f"Could not read {path}: {exc}") from exc

    if data is None:
        return {}
    if not isinstance(data, dict):
        raise TypeError(f"Configuration must be a YAML mapping: {path}")
    return data


def _atomic_write_text(path: Path, content: str) -> None:
    """Atomically write raw text to ``path`` (temp file + ``os.replace``).

    Used for config writes and rollbacks so a mid-write failure can never
    leave a truncated config behind. Preserves the original file's permission
    bits (e.g. ``0600`` for a manually restricted config); a NEW file is
    created with mode ``0o666`` so the process umask decides its final mode,
    matching ``iterate_cli.generator.atomic_write``. The previous
    ``tempfile.mkstemp``-based write forced every config to ``0600`` regardless
    of its prior mode, silently dropping group/other read bits.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        original_mode = path.stat().st_mode & 0o777
    except OSError:
        original_mode = None
    create_mode = original_mode if original_mode is not None else 0o666
    # Process-unique, collision-resistant temp name in the same directory (so
    # ``os.replace`` stays on one mount point and is atomic).
    tmp_name = str(
        path.with_name(
            f".{path.name}.{os.getpid()}-{uuid.uuid4().hex[:8]}.tmp"
        )
    )
    open_flags = (
        os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    fd = os.open(tmp_name, open_flags, create_mode)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if original_mode is not None:
            os.chmod(tmp_name, original_mode)
        os.replace(tmp_name, path)
    except BaseException:
        # Never leave a partial temp file behind on failure.
        try:
            os.remove(tmp_name)
        except OSError:
            pass
        raise


def save_config(path: Path, config: dict[str, object]) -> None:
    """Save a config mapping to a YAML file with helpful comments.

    The write is atomic (same-directory temp file + ``os.replace``) and
    preserves the destination's permission bits (new files use the umask),
    matching ``_atomic_write_text`` / ``generator.atomic_write``.
    """
    try:
        content = yaml.safe_dump(
            config, sort_keys=False, allow_unicode=True, default_flow_style=False
        )
    except TypeError as exc:
        # yaml.safe_dump cannot serialise a non-serialisable value (e.g. a
        # date object a hand-edited config introduced); surface it cleanly.
        raise ValueError(f"Cannot serialise config: {exc}") from exc
    _atomic_write_text(path, content)


def init_config(target: Path, source: Path) -> int:
    """Copy the master config to the project root if it does not exist."""
    master_path = source / DEFAULT_CONFIG_PATH
    project_path = target / "iterate.config.yaml"

    if project_path.exists():
        _warning(f"Project config already exists: {project_path}")
        _hint("Use --set to modify it, or delete it first to re-initialize.")
        return 1

    if not master_path.exists():
        _error(f"Master config not found: {master_path}")
        return 1

    content = master_path.read_text(encoding="utf-8")
    # mkdir the TARGET dir itself, not its parent: mkstemp(dir=target)
    # requires target to exist. The parent-level mkdir only masked this for
    # callers that pre-created the directory (main checks target.exists()),
    # so any direct call — tests, refactors — crashed with FileNotFoundError.
    target.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=target, prefix=".iterate.config.yaml.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(tmp_name, project_path)
    except BaseException:
        try:
            os.remove(tmp_name)
        except OSError:
            pass
        raise
    _success(f"Initialized project config: {project_path}")
    return 0


def list_config(target: Path) -> int:
    """Print the current project-level config."""
    project_path = target / "iterate.config.yaml"
    if not project_path.exists():
        _warning(f"No project config found at {project_path}")
        return 1

    config = load_config(project_path)
    print(yaml.safe_dump(config, sort_keys=False, allow_unicode=True))
    return 0


def set_config_values(target: Path, source: Path, set_pairs: list[list[str]]) -> int:
    """Apply --set key=value pairs to the project-level config and validate."""
    project_path = target / "iterate.config.yaml"
    if project_path.exists():
        try:
            config = load_config(project_path)
            previous_text = project_path.read_text(encoding="utf-8")
        except (OSError, ValueError, TypeError) as exc:
            # load_config surfaces YAML/type/read errors; guard the raw text
            # read too so a non-UTF-8 file fails with a clean message instead
            # of a traceback (and never gets blindly overwritten).
            _error(f"Cannot modify {project_path}: {exc}")
            _hint("Fix the file manually, or delete it and re-run with --init.")
            return 1
    else:
        config = {}
        previous_text = None

    # Resolve which dotted paths are boolean-typed so a YAML-1.1 spelling
    # (yes/no/on/off) becomes a real bool on exactly those fields.
    bool_paths = _config_boolean_paths(source / "config" / "config.schema.json")

    for group in set_pairs:
        for pair in group:
            if "=" not in pair:
                _error(f"Invalid --set argument (expected key=value): {pair}")
                return 1
            key, value = pair.split("=", 1)
            key = key.strip()
            if not key:
                _error(f"Empty key in --set argument: {pair}")
                return 1
            try:
                if key in bool_paths:
                    set_nested_value(config, key, parse_bool_spelling(value))
                else:
                    set_nested_value(config, key, parse_value(value))
            except ValueError as exc:
                _error(f"{exc}")
                return 1

    save_config(project_path, config)

    errors = _validate_project_config(target, source)
    if errors:
        _error(f"Validation failed for {project_path}; changes have been reverted.")
        for error in errors:
            _hint(f"- {error}")
        if previous_text is not None:
            _atomic_write_text(project_path, previous_text)
        else:
            project_path.unlink()
        return 1

    _success(f"Updated project config: {project_path}")
    return 0


def prompt_choice(
    question: str,
    choices: list[str],
    default: str | None = None,
    input_func: InputFunc = input,
) -> str:
    """Ask the user to select one option from a list.

    Args:
        question: The prompt shown to the user.
        choices: List of valid options to choose from.
        default: Optional default option returned on an empty answer.
        input_func: Callable used to read user input (injectable for tests).
    """
    _tui_print("")
    _tui_print(question, style="iterate.primary")
    for idx, choice in enumerate(choices, start=1):
        marker = " (default)" if choice == default else ""
        _hint(f"{idx}. {choice}{marker}")
    while True:
        try:
            answer = input_func("  \u2514 Enter number or name: ").strip()
        except EOFError:
            # Ctrl-D / closed stdin mid-prompt: adopt the default (or, with no
            # default, empty) instead of crashing with a traceback.
            return default if default is not None else ""
        if not answer and default is not None:
            return default
        if answer.isdigit():
            idx = int(answer) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
        if answer in choices:
            return answer
        _warning("Invalid choice, please try again.")


def prompt_text(
    question: str,
    default: str | None = None,
    input_func: InputFunc = input,
) -> str:
    """Ask the user for free-form text input.

    Args:
        question: The prompt shown to the user.
        default: Optional default returned when the answer is empty.
        input_func: Callable used to read user input (injectable for tests).
    """
    default_hint = f" [{default}]" if default else ""
    while True:
        try:
            answer = input_func(f"\n{question}{default_hint}: ").strip()
        except EOFError:
            # EOF mid-prompt: fall back to the default (or empty text when no
            # default exists) instead of surfacing a traceback.
            return default if default is not None else ""
        if answer:
            return answer
        if default is not None:
            return default
        _warning("A value is required.")


def prompt_int(
    question: str,
    default: int | None = None,
    input_func: InputFunc = input,
) -> int:
    """Ask the user for an integer.

    Args:
        question: The prompt shown to the user.
        default: Optional default returned when the answer is empty.
        input_func: Callable used to read user input (injectable for tests).
    """
    default_hint = f" [{default}]" if default is not None else ""
    while True:
        try:
            answer = input_func(f"\n{question}{default_hint}: ").strip()
        except EOFError:
            # EOF mid-prompt: adopt the default; without one there is no
            # sane integer to synthesize, so surface the cancellation.
            if default is not None:
                return default
            raise
        if not answer and default is not None:
            return default
        try:
            return int(answer)
        except ValueError:
            _warning("Please enter a valid integer.")


def prompt_bool(
    question: str,
    default: bool = True,
    input_func: InputFunc = input,
) -> bool:
    """Ask the user a yes/no question.

    Args:
        question: The prompt shown to the user.
        default: Default answer returned on an empty input.
        input_func: Callable used to read user input (injectable for tests).
    """
    default_text = "Y/n" if default else "y/N"
    while True:
        try:
            answer = input_func(f"\n{question} [{default_text}]: ").strip().lower()
        except EOFError:
            # EOF mid-prompt: adopt the default (answering "no" on a decline-
            # by-default question is the safe conservative choice).
            return default
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        _warning("Please enter 'y' or 'n'.")


def interactive_config(
    target: Path,
    source: Path,
    input_func: InputFunc = input,
) -> int:
    """Run an interactive wizard to create or update the project config.

    Args:
        target: Project directory (where iterate.config.yaml lives).
        source: Skill source directory (for the master config + schema).
        input_func: Callable used to read user input (injectable for tests).
    """
    project_path = target / "iterate.config.yaml"
    master_path = source / DEFAULT_CONFIG_PATH

    if project_path.exists():
        try:
            config = load_config(project_path)
            previous_text = project_path.read_text(encoding="utf-8")
        except (OSError, ValueError, TypeError) as exc:
            # A project config we cannot parse or read (bad YAML, non-UTF-8
            # bytes, unreadable file) must not be clobbered by the wizard:
            # fail with a clean message instead of a traceback.
            _error(f"Cannot edit {project_path}: {exc}")
            _hint("Fix the file manually first, or delete it and run the wizard again.")
            return 1
    elif master_path.exists():
        config = load_config(master_path)
        previous_text = None
    else:
        config = {}
        previous_text = None

    _intro("iterate-skill configuration wizard")

    config["goal"] = prompt_text(
        "Iteration goal",
        config.get("goal", "Improve code quality"),
        input_func=input_func,
    )
    config["max_rounds"] = prompt_int_in_range(
        "Max rounds",
        MIN_ROUNDS,
        MAX_ROUNDS,
        config.get("max_rounds", 7),
        input_func=input_func,
    )
    config["language"] = prompt_choice(
        "Output language",
        LANGUAGE_CHOICES,
        config.get("language", "en"),
        input_func=input_func,
    )
    config["dimensions"] = prompt_dimensions(
        config.get("dimensions", DIMENSION_CHOICES), input_func=input_func
    )
    # A hand-edited config may hold a scalar for a section the schema declares
    # as object (e.g. `atomic: 5`). load_config only requires the top level to
    # be a mapping, so these would crash the wizard with AttributeError before
    # schema validation ever runs. Coerce non-mapping sections to {} first,
    # matching the sibling CLI wizard's isinstance(section, dict) guard.
    if not isinstance(config.get("review"), dict):
        config["review"] = {}
    config["review"]["scope"] = prompt_choice(
        "Review scope",
        SCOPE_CHOICES,
        config["review"].get("scope", "full"),
        input_func=input_func,
    )
    if not isinstance(config.get("atomic"), dict):
        config["atomic"] = {}
    config["atomic"]["max_lines"] = prompt_int(
        "Atomic issue max lines",
        config["atomic"].get("max_lines", 20),
        input_func=input_func,
    )
    if not isinstance(config.get("git"), dict):
        config["git"] = {}
    config["git"]["push_per_round"] = prompt_bool(
        "Push after each round",
        config["git"].get("push_per_round", False),
        input_func=input_func,
    )

    save_config(project_path, config)

    errors = _validate_project_config(target, source)
    if errors:
        _error(f"Validation failed for {project_path}; changes have been reverted.")
        for error in errors:
            _hint(f"- {error}")
        if previous_text is not None:
            _atomic_write_text(project_path, previous_text)
        else:
            project_path.unlink()
        return 1

    _success(f"Configuration saved: {project_path}")
    return 0


def prompt_int_in_range(
    question: str,
    min_value: int,
    max_value: int,
    default: int | None = None,
    input_func: InputFunc = input,
) -> int:
    """Ask the user for an integer constrained to [min_value, max_value].

    An out-of-range ``default`` is clamped into range before prompting.
    Otherwise an empty answer (Enter, or EOF — both of which return the
    default) fails the range check, re-prompts with the same default, and
    fails again forever: an unreachable prompt the user can only escape with
    Ctrl-C. The clamp makes the default itself always acceptable.
    """
    full_question = f"{question} ({min_value}-{max_value})"
    if default is not None:
        default = max(min_value, min(default, max_value))
    while True:
        value = prompt_int(full_question, default, input_func=input_func)
        if min_value <= value <= max_value:
            return value
        _warning(f"Please enter a value between {min_value} and {max_value}.")


def prompt_dimensions(current: object, input_func: InputFunc = input) -> list[str]:
    """Interactively select enabled dimensions."""
    # Preserve the ORDER of the current selection: the EOF/empty-answer paths
    # below used to round-trip through a set, so the same config produced a
    # differently-ordered `dimensions:` list on every run (YAML diff noise).
    ordered_current = list(dict.fromkeys(current)) if isinstance(current, list) else list(DIMENSION_CHOICES)
    current_set = set(ordered_current)
    selected: list[str] = []
    _tui_print("")
    _tui_print("Select review dimensions (enter numbers/names, comma-separated):", style="iterate.primary")
    for idx, dim in enumerate(DIMENSION_CHOICES, start=1):
        marker = " [enabled]" if dim in current_set else ""
        _hint(f"{idx}. {dim}{marker}")
    try:
        answer = input_func("Dimensions: ").strip()
    except EOFError:
        # EOF mid-prompt: keep the current dimension selection.
        return _ensure_non_empty_dimensions(ordered_current)
    if not answer:
        return _ensure_non_empty_dimensions(ordered_current)

    for part in answer.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(DIMENSION_CHOICES):
                selected.append(DIMENSION_CHOICES[idx])
            else:
                _warning(f"Invalid dimension number: '{part}' (ignored)")
        elif part in DIMENSION_CHOICES:
            selected.append(part)
        else:
            _warning(f"Invalid dimension name: '{part}' (ignored)")

    unique_selected = list(dict.fromkeys(selected))
    if not unique_selected:
        # Never silently fall back to all dimensions: tell the user their input
        # was rejected and that every dimension has been enabled instead.
        _warning("输入无效，已启用全部维度 / Invalid input; enabling all dimensions.")
        return list(DIMENSION_CHOICES)
    return unique_selected


def _ensure_non_empty_dimensions(dimensions: list[str]) -> list[str]:
    """Return the dimensions list, falling back to all choices if empty."""
    return dimensions if dimensions else list(DIMENSION_CHOICES)


def config_command(
    target: Path,
    source: Path,
    init: bool,
    list_config_flag: bool,
    interactive: bool,
    set_pairs: list[list[str]] | None = None,
    input_func: InputFunc = input,
) -> int:
    """Manage the project-level iterate.config.yaml.

    Args:
        target: Project directory (where iterate.config.yaml lives).
        source: Skill source directory (master config + schema).
        init: Copy the master config to the project root if missing.
        list_config_flag: Print the current project-level config.
        interactive: Run the interactive config wizard.
        set_pairs: ``--set`` key=value pairs to apply, then validate.
        input_func: Callable used to read user input (interactive wizard).
    """
    if init:
        return init_config(target, source)
    if list_config_flag:
        return list_config(target)
    if set_pairs:
        return set_config_values(target, source, set_pairs)
    if interactive:
        return interactive_config(target, source, input_func=input_func)

    _warning("No config action specified. Use --init, --list, --set, or --interactive.")
    return 1


def _add_install_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "install", help="Install the skill into an AI assistant's skills directory."
    )
    parser.add_argument(
        "--ai",
        choices=AI_CHOICES,
        help="Target AI assistant (or 'all'). If omitted, auto-detect installed assistants and prompt.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Project or home directory (default: current directory).",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print what would be copied without copying."
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing skill files."
    )
    parser.add_argument(
        "--global",
        dest="global_install",
        action="store_true",
        help="Install into the user's home directory instead of the project.",
    )


def _add_uninstall_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "uninstall", help="Remove the skill from an AI assistant's skills directory."
    )
    parser.add_argument(
        "--ai", choices=AI_CHOICES, help="Target AI assistant (or 'all'). If omitted, auto-detect installed assistants."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory).",
    )
    parser.add_argument(
        "--global",
        dest="global_install",
        action="store_true",
        help="Uninstall from the user's home directory instead of the project.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt.",
    )


def _add_validate_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "validate", help="Validate the project-level iterate.config.yaml."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory).",
    )


def _add_update_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "update", help="Refresh installed skill files and check for new releases."
    )
    parser.add_argument(
        "--ai",
        choices=AI_CHOICES,
        help="Target AI assistant (default: auto-detect installed assistants).",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory).",
    )
    parser.add_argument(
        "--token",
        help="GitHub Personal Access Token for higher API rate limits.",
    )
    parser.add_argument(
        "--global",
        dest="global_install",
        action="store_true",
        help="Update the installation in the user's home directory.",
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip the confirmation prompt before downloading from GitHub.",
    )


def _add_config_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "config", help="Manage the project-level iterate.config.yaml."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory).",
    )
    parser.add_argument(
        "--init", action="store_true", help="Copy the master config to the project root."
    )
    parser.add_argument(
        "--list",
        dest="list_config",
        action="store_true",
        help="Print the current project config.",
    )
    parser.add_argument(
        "--set",
        action="append",
        nargs="+",
        metavar="KEY=VALUE",
        help="Set a config value (supports nested keys like validation.commands.python).",
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Run an interactive configuration wizard."
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="iterate-skill",
        description="Install and configure iterate-skill for AI coding assistants.",
    )
    # `--version` was missing, so `npx iterate-skill-installer --version` (and
    # the bare script) printed a usage error instead of the version — there was
    # no way to confirm which installer build is running without reading the
    # file. Reads pyproject at runtime so the value cannot drift from
    # [project].version; falls back to the packaged constant.
    parser.add_argument(
        "--version",
        action="version",
        version=f"iterate-skill-installer {_installed_version()}",
    )
    subparsers = parser.add_subparsers(dest="command")
    _add_install_parser(subparsers)
    _add_uninstall_parser(subparsers)
    _add_validate_parser(subparsers)
    _add_update_parser(subparsers)
    _add_config_parser(subparsers)
    return parser


def parse_legacy_args(argv: list[str] | None) -> argparse.Namespace | None:
    """Support the original direct install invocation for backward compatibility."""
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        return None
    if args[0] in ("install", "uninstall", "validate", "config", "update"):
        return None
    # Accept both ``--ai trae`` and ``--ai=trae``. The equality-only test
    # missed the ``--ai=<value>`` spelling, so the legacy direct invocation
    # (``install.py --ai=trae``) fell through to the subcommand parser and
    # exited 2 with a usage error instead of installing.
    if not any(arg == "--ai" or arg.startswith("--ai=") for arg in args):
        return None

    parser = argparse.ArgumentParser()
    parser.add_argument("--ai", required=True, choices=AI_CHOICES)
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--global", dest="global_install", action="store_true")
    namespace, unknown = parser.parse_known_args(args)
    if unknown:
        return None
    namespace.command = "install"
    return namespace


def _reconfigure_stdio() -> None:
    """Force UTF-8 on stdio so CJK output cannot crash the installer.

    Windows Python defaults stdout/stderr to cp1252/locale encoding unless a
    UTF-8 mode or a modern terminal is detected; printing the Chinese banner
    or a CJK project name then raises ``UnicodeEncodeError`` and aborts the
    install mid-way. Best-effort: a stream that refuses to be reconfigured
    (a closed pipe, a StringIO in tests) is left alone.
    """
    for stream in (sys.stdout, sys.stderr, sys.stdin):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError, AttributeError):
            # e.g. "I/O operation on closed file" from an already-closed
            # stream, or a stream that does not accept the keyword args.
            continue


def main(argv: list[str] | None = None, source: Path | None = None) -> int:
    """CLI entry point."""
    _reconfigure_stdio()
    if source is None:
        source = Path(__file__).resolve().parent.parent

    legacy = parse_legacy_args(argv)
    if legacy is not None:
        args = legacy
    else:
        parser = build_parser()
        args = parser.parse_args(argv)

    if not args.command:
        build_parser().print_help()
        # Usage error (no subcommand given), matching argparse's own exit 2
        # for bad flags in this same entry point — previously 1 made "the
        # user mistyped the invocation" indistinguishable from a business
        # failure that a retry/fix loop should act on.
        return 2

    if args.command == "install":
        if not args.target.exists():
            _error(f"Error: target directory does not exist: {args.target}")
            return 1
        try:
            return install_command(
                args.ai,
                args.target.resolve(),
                args.dry_run,
                source,
                args.force,
                args.global_install,
                input,
            )
        except FileNotFoundError as exc:
            _error(f"Error: {exc}")
            return 1

    if args.command == "uninstall":
        return uninstall_command(
            args.ai, args.target.resolve(), args.global_install, args.yes, input
        )

    if args.command == "validate":
        if not args.target.exists():
            _error(f"Error: target directory does not exist: {args.target}")
            return 1
        return validate_command(args.target.resolve(), source)

    if args.command == "update":
        if not args.target.exists():
            _error(f"Error: target directory does not exist: {args.target}")
            return 1
        return update_command(
            args.ai,
            args.target.resolve(),
            source,
            args.token,
            args.global_install,
            args.yes,
        )

    if args.command == "config":
        if not args.target.exists():
            _error(f"Error: target directory does not exist: {args.target}")
            return 1
        return config_command(
            args.target.resolve(),
            source,
            args.init,
            args.list_config,
            args.interactive,
            args.set,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
