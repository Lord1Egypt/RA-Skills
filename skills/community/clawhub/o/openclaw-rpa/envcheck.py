#!/usr/bin/env python3
"""Environment checks for Python + Playwright (import + Chromium)."""

from __future__ import annotations

import subprocess
import sys
from typing import Callable, Tuple

MIN_PYTHON = (3, 8)

CheckFn = Callable[[], Tuple[bool, str]]


def check_python() -> Tuple[bool, str]:
    if sys.version_info < MIN_PYTHON:
        return (
            False,
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required (found {sys.version_info.major}.{sys.version_info.minor})",
        )
    return True, f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def check_playwright_import() -> Tuple[bool, str]:
    try:
        import playwright  # noqa: F401

        try:
            from importlib.metadata import version as pkg_version

            ver = pkg_version("playwright")
        except Exception:
            ver = getattr(playwright, "__version__", "?")
        return True, f"playwright package ({ver})"
    except ImportError:
        return False, "playwright package not installed"


def check_chromium_launch() -> Tuple[bool, str]:
    try:
        r = subprocess.run(
            [
                sys.executable,
                "-c",
                "from playwright.sync_api import sync_playwright;"
                "p=sync_playwright().start(); b=p.chromium.launch(headless=True);"
                "b.close(); p.stop()",
            ],
            capture_output=True,
            timeout=45,
        )
        if r.returncode == 0:
            return True, "Chromium launch (headless) OK"
        err = (r.stderr or b"").decode("utf-8", errors="replace").strip()
        out = (r.stdout or b"").decode("utf-8", errors="replace").strip()
        return False, err or out or "Chromium launch failed"
    except subprocess.TimeoutExpired:
        return False, "Chromium launch timed out"
    except Exception as e:
        return False, str(e)


def install_chromium() -> None:
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=True,
    )


def ensure_playwright_chromium(*, auto_install: bool = True) -> int:
    """
    Verify Python, playwright import, and Chromium. Optionally install Chromium.
    Returns 0 on success, 1 on failure.
    """
    ok, msg = check_python()
    if not ok:
        print(f"❌ {msg}", file=sys.stderr)
        return 1

    ok, msg = check_playwright_import()
    if not ok:
        print(f"❌ {msg}", file=sys.stderr)
        print("   Install: pip install -r requirements.txt", file=sys.stderr)
        return 1

    ok, msg = check_chromium_launch()
    if ok:
        return 0

    if not auto_install:
        print(f"❌ Chromium: {msg}", file=sys.stderr)
        print(
            "   Fix: python3 -m playwright install chromium",
            file=sys.stderr,
        )
        return 1

    print("⚙️  Playwright Chromium missing or broken; installing (about 1–2 minutes)…")
    try:
        install_chromium()
    except subprocess.CalledProcessError as e:
        print(f"❌ playwright install failed: {e}", file=sys.stderr)
        return 1

    ok, msg = check_chromium_launch()
    if not ok:
        print(f"❌ Chromium still not usable: {msg}", file=sys.stderr)
        return 1
    return 0


def print_report() -> int:
    """Print human-readable lines; exit code 0 if all OK, else 1."""
    lines: list[str] = []
    fatal = False

    ok, msg = check_python()
    lines.append(f"{'✅' if ok else '❌'} {msg}")
    if not ok:
        fatal = True

    ok, msg = check_playwright_import()
    lines.append(f"{'✅' if ok else '❌'} {msg}")
    if not ok:
        fatal = True

    if not fatal:
        ok, msg = check_chromium_launch()
        lines.append(f"{'✅' if ok else '❌'} {msg}")
        if not ok:
            fatal = True

    print("\n".join(lines))
    if fatal:
        print(
            "\nInstall (recommended):\n"
            "  ./scripts/install.sh\n"
            "Or: pip install -r requirements.txt && python3 -m playwright install chromium",
            file=sys.stderr,
        )
        return 1
    return 0


def main() -> int:
    return print_report()


# ── Capability profiles (chat onboarding: single letter) ─────────────────
# needs_browser: A/D/E/G 含浏览器；B/C/F/N 纯文件/API，无需 Playwright + Chromium。
# needs_browser: A/D/E/G include browser steps; B/C/F/N are file/API only — Playwright not required.

CAPABILITY_PROFILES: dict[str, dict[str, bool]] = {
    "A": {"needs_excel": False, "needs_word": False, "needs_browser": True},
    "B": {"needs_excel": True,  "needs_word": False, "needs_browser": False},
    "C": {"needs_excel": False, "needs_word": True,  "needs_browser": False},
    "D": {"needs_excel": True,  "needs_word": False, "needs_browser": True},
    "E": {"needs_excel": False, "needs_word": True,  "needs_browser": True},
    "F": {"needs_excel": True,  "needs_word": True,  "needs_browser": False},
    "G": {"needs_excel": True,  "needs_word": True,  "needs_browser": True},
    "N": {"needs_excel": False, "needs_word": False, "needs_browser": False},
}


def normalize_capability_letter(raw: str) -> str | None:
    s = (raw or "").strip().upper()
    if len(s) == 1 and s in CAPABILITY_PROFILES:
        return s
    return None


def check_openpyxl() -> Tuple[bool, str]:
    try:
        import openpyxl  # noqa: F401

        try:
            from importlib.metadata import version as pkg_version

            ver = pkg_version("openpyxl")
        except Exception:
            ver = "?"
        return True, f"openpyxl ({ver})"
    except ImportError:
        return False, "openpyxl not installed"


def check_python_docx() -> Tuple[bool, str]:
    try:
        import docx  # noqa: F401

        try:
            from importlib.metadata import version as pkg_version

            ver = pkg_version("python-docx")
        except Exception:
            ver = "?"
        return True, f"python-docx ({ver})"
    except ImportError:
        return False, "python-docx not installed (pip package name: python-docx)"


def deps_check_capability(letter: str) -> tuple[list[str], bool]:
    """
    Check Python + Playwright/Chromium + optional openpyxl / python-docx.
    Returns (lines, all_ok).
    """
    cap = normalize_capability_letter(letter)
    if cap is None:
        return ([f"❌ invalid capability code (use A–G or N): {letter!r}"], False)

    lines: list[str] = []
    fatal = False
    profile = CAPABILITY_PROFILES[cap]
    needs_excel = profile["needs_excel"]
    needs_word = profile["needs_word"]
    needs_browser = profile["needs_browser"]

    ok, msg = check_python()
    lines.append(f"{'✅' if ok else '❌'} {msg}")
    if not ok:
        fatal = True

    if needs_browser:
        ok, msg = check_playwright_import()
        lines.append(f"{'✅' if ok else '❌'} {msg}")
        if not ok:
            fatal = True

        if not fatal:
            ok, msg = check_chromium_launch()
            lines.append(f"{'✅' if ok else '❌'} {msg}")
            if not ok:
                fatal = True

    if needs_excel:
        ok, msg = check_openpyxl()
        lines.append(f"{'✅' if ok else '❌'} {msg}")
        if not ok:
            fatal = True

    if needs_word:
        ok, msg = check_python_docx()
        lines.append(f"{'✅' if ok else '❌'} {msg}")
        if not ok:
            fatal = True

    return lines, not fatal


def print_deps_capability_report(letter: str) -> int:
    lines, ok = deps_check_capability(letter)
    print("\n".join(lines))
    if not ok:
        cap = normalize_capability_letter(letter)
        print(
            "\nFix (same Python as Playwright / rpa_manager):\n"
            "  python3 rpa_manager.py deps-install "
            + (cap or letter.upper()),
        )
        return 1
    return 0


def install_openpyxl_docx(*, excel: bool, word: bool) -> int:
    pkgs: list[str] = []
    if excel:
        pkgs.append("openpyxl")
    if word:
        pkgs.append("python-docx")
    if not pkgs:
        return 0
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", *pkgs],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ pip install failed: {e}", file=sys.stderr)
        return 1
    return 0


def ensure_capability_deps(letter: str, *, auto_chromium: bool = True) -> int:
    """
    Install missing office libs; ensure Playwright Chromium like record-start.
    Returns 0 on success.
    """
    cap = normalize_capability_letter(letter)
    if cap is None:
        print(f"❌ invalid capability code: {letter!r}", file=sys.stderr)
        return 1

    profile = CAPABILITY_PROFILES[cap]
    if install_openpyxl_docx(excel=profile["needs_excel"], word=profile["needs_word"]) != 0:
        return 1

    if profile["needs_browser"]:
        if ensure_playwright_chromium(auto_install=auto_chromium) != 0:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
