"""
debug_utils.py — Post-mortem debugging, traceback introspection, exception analysis.

NEW in v7 — v6 had no actual debugging helpers despite the "python debugging skill" framing.
This module fills that gap with patterns for:
- Post-mortem: drop into pdb at the frame where an exception was raised
- Traceback introspection: walk frames, extract locals, format for review
- Exception summarization: type, message, root cause, frame chain
- breakpoint() helper: works in both script and IPython contexts

These are designed for *interactive* debugging — the model calls these from
the ipython tool to investigate a crash that just happened.
"""
from __future__ import annotations

import inspect
import pdb
import sys
import traceback
from types import TracebackType
from typing import Any, Optional


def post_mortem(tb: Optional[TracebackType] = None) -> None:
    """Drop into pdb at the frame where an exception was raised.

    If `tb` is None, uses sys.last_traceback (the most recent uncaught
    exception in the interactive session). This is the standard "I just got
    an exception, investigate it" entry point.

    Usage in ipython tool:
        try:
            risky_call()
        except Exception:
            post_mortem()
    """
    if tb is None:
        tb = getattr(sys, "last_traceback", None)
        if tb is None:
            print("No traceback available — pass an explicit tb= or run after an exception.")
            return
    pdb.post_mortem(tb)


def extract_traceback(exc: BaseException, *, include_locals: bool = False) -> list[dict]:
    """Walk an exception's traceback and return a structured frame list.

    Each frame dict has: file, line, lineno, function, source_line, and
    optionally locals (when ``include_locals=True``).

    **Security note**: locals may contain credentials, PII, tokens, or other
    sensitive runtime state. The default is ``False`` (no locals collected).
    Pass ``include_locals=True`` only when the output stays within a trusted
    context — interactive debugging in the ipython tool — and never enable
    it for output that may be saved to disk, shared in a chat, or attached
    to a bug report without first redacting sensitive keys.
    """
    frames = []
    tb = exc.__traceback__
    while tb is not None:
        frame = tb.tb_frame
        info = {
            "file": frame.f_code.co_filename,
            "lineno": tb.tb_lineno,
            "function": frame.f_code.co_name,
            "source_line": _get_source_line(frame.f_code.co_filename, tb.tb_lineno),
        }
        if include_locals:
            # Filter to safe-to-show locals (skip dunder modules)
            info["locals"] = {
                k: _safe_repr(v)
                for k, v in frame.f_locals.items()
                if not k.startswith("_") and not inspect.ismodule(v)
            }
        frames.append(info)
        tb = tb.tb_next
    return frames


def summarize_exception(exc: BaseException, *, max_frames: int = 20, include_locals: bool = False) -> dict:
    """Return a structured summary of an exception suitable for review.

    Includes type, message, root cause chain (for __cause__/__context__),
    frame list, and the formatted traceback string.

    **Security note**: pass ``include_locals=True`` to capture frame locals
    alongside each stack frame. Locals may contain credentials, PII, tokens,
    or other sensitive runtime state. The default is ``False`` — enable
    only for interactive debugging where the output stays in a trusted
    context. See :func:`extract_traceback` for the full guidance.
    """
    chain = []
    current = exc
    while current is not None:
        chain.append({
            "type": type(current).__name__,
            "message": str(current),
        })
        current = current.__cause__ or current.__context__
        if current is getattr(exc, "__cause__", None) and current is exc.__cause__:
            break  # avoid infinite loop on self-referential contexts

    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "cause_chain": chain,
        "frames": extract_traceback(exc, include_locals=include_locals)[:max_frames],
        "traceback_str": "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
    }


def format_exception(exc: BaseException, *, max_frames: int = 10, show_locals: bool = False) -> str:
    """Format an exception as a readable multi-line string.

    More compact than the full traceback; useful for showing the user
    what went wrong without dumping 500 lines of stdlib frames.

    **Security note**: pass ``show_locals=True`` to include frame locals in
    the output. Locals may contain credentials, PII, tokens, or other
    sensitive runtime state. The default is ``False`` — enable only for
    interactive debugging where the output stays in a trusted context.
    """
    lines = [f"{type(exc).__name__}: {exc}"]
    if exc.__cause__:
        lines.append(f"  Caused by: {type(exc.__cause__).__name__}: {exc.__cause__}")

    tb = exc.__traceback__
    frame_count = 0
    while tb is not None and frame_count < max_frames:
        frame = tb.tb_frame
        lines.append(f"  at {frame.f_code.co_filename}:{tb.tb_lineno} in {frame.f_code.co_name}")
        if show_locals and frame.f_locals:
            for k, v in list(frame.f_locals.items())[:8]:
                if k.startswith("_") or inspect.ismodule(v):
                    continue
                lines.append(f"      {k} = {_safe_repr(v)}")
        tb = tb.tb_next
        frame_count += 1

    if tb is not None:
        lines.append(f"  ... ({max_frames} frames shown, more truncated)")
    return "\n".join(lines)


def breakpoint_helper(condition: bool = True, message: str = "") -> None:
    """Conditional breakpoint that works in both scripts and IPython.

    Sets PYTHONBREAKPOINT=pdb.set_trace by default (works in IPython).
    Pass condition=False to skip — easier than wrapping in if/else at
    every call site.
    """
    if not condition:
        return
    if message:
        print(f"[breakpoint] {message}")
    sys.breakpointhook()  # respects PYTHONBREAKPOINT env var


def _get_source_line(filename: str, lineno: int) -> Optional[str]:
    """Get a source line from a file, returning None on any failure."""
    try:
        with open(filename, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if i == lineno:
                    return line.rstrip()
    except (OSError, UnicodeDecodeError):
        return None
    return None


def _safe_repr(obj: Any, max_len: int = 200) -> str:
    """repr() with length cap and exception fallback."""
    try:
        r = repr(obj)
        return r if len(r) <= max_len else r[: max_len - 3] + "..."
    except Exception as e:
        return f"<repr failed: {type(e).__name__}>"


__all__ = [
    "post_mortem",
    "extract_traceback",
    "summarize_exception",
    "format_exception",
    "breakpoint_helper",
]
