"""The command-line text protocol is UTF-8, including redirected output.

Windows can default redirected Python streams to an ANSI code page. A gate
then crashes while printing a Chinese finding, after appearing to return the
same exit code as a genuine rejection. Configure only command-line entry
points; importing a library must not replace its caller's streams.

`configure_output` is also the one call every entry point's `__main__` makes
before parsing its arguments, so it is where a script refuses to start at all:
on a Python older than the documented floor, and on a `--workspace` inside the
skill directory. Both exit 2 with one line, the shared "could not run" answer.

This module must itself stay importable on old Pythons — that is why it has the
`__future__` import — or the version check below could never print.
"""
from __future__ import annotations

import pathlib
import sys

# README.md, REFERENCE.md and references/agent-setup.md all say Python 3.10+,
# and setup_dependencies.py enforces the same floor. macOS still ships 3.9 as
# /usr/bin/python3, and every mode file says `python3 scripts/...`.
MIN_PYTHON = (3, 10)


def require_supported_python(version_info=None, script=None) -> None:
    """Exit 2 with one readable line on a Python older than MIN_PYTHON.

    The scripts are written for 3.10+ and tested on 3.11. On 3.9 they failed
    with a TypeError traceback and exit 1 (`str | None` evaluated at import),
    and exit 1 is a gate's code for "findings". Making 3.9 limp further would
    only move the traceback deeper, into a runtime path nobody tests on it.
    ASCII only: this prints before the streams are switched to UTF-8.
    """
    found = tuple((sys.version_info if version_info is None else version_info)[:3])
    if found[:2] >= MIN_PYTHON:
        return
    name = pathlib.Path(script or sys.argv[0] or "<tool>.py").name
    print(f"PYTHON_TOO_OLD: job-hunt needs Python "
          f"{'.'.join(map(str, MIN_PYTHON))}+, but {sys.executable} is "
          f"{'.'.join(map(str, found))}. Run it through the prepared runtime: "
          f"python3 scripts/run_tool.py python scripts/{name} <same arguments>. "
          f"If no runtime is prepared yet, run scripts/setup_dependencies.py with "
          f"a Python 3.10+ interpreter first (references/agent-setup.md).",
          file=sys.stderr)
    raise SystemExit(2)


def workspace_arguments(argv) -> list:
    """Every value argparse would bind to `--workspace`, exactly as typed.

    Both `--workspace X` and `--workspace=X`, plus the unambiguous prefixes
    argparse also accepts (`--work X`). Scanning stops at `--`, after which
    nothing is an option.
    """
    out, tokens, i = [], list(argv), 0
    while i < len(tokens):
        token = tokens[i]
        if token == "--":
            break
        flag, has_value, value = token.partition("=")
        if len(flag) >= 3 and "--workspace".startswith(flag):
            if has_value:
                out.append(value)
            elif i + 1 < len(tokens):
                out.append(tokens[i + 1])
                i += 1
        i += 1
    return out


def refuse_skill_workspace(argv=None) -> None:
    """Exit 2 before anything is written when `--workspace` is in the skill.

    See `paths.skill_workspace_refusal`. Here rather than in each script's
    argparse so that every entry point gets it from the call it already makes.
    """
    import paths

    for raw in workspace_arguments(sys.argv[1:] if argv is None else argv):
        reason = paths.skill_workspace_refusal(raw)
        if reason:
            print(reason, file=sys.stderr)
            raise SystemExit(2)


def configure_output() -> None:
    require_supported_python()
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors=stream.errors, newline="\n")
    refuse_skill_workspace()


def pass_notice(gate: str, mode: str | None = None) -> None:
    """One line on STDERR when a gate finds nothing.

    Not stdout. `references/workflow-checklist.md` fixes stdout as one finding
    per line with a stable CODE prefix, because an always-on line there trains
    the reader to skip the channel that reports real findings; twenty
    assertions across six test files pin that silence, and they stay true.

    But total silence is the other failure, and it is the one that was
    measured. On 2026-10-08 two agents walked discover and apply using only
    what the files and scripts print, and both stopped at the first green
    light and reported the round finished — the four discover completion gates
    exit 0 with zero bytes of stdout between them, while report.md, the
    coverage check, the render and the delivery were all still to do.

    This says the one thing a gate alone cannot: passing is not finishing. It
    deliberately does NOT name the next command. Which command follows depends
    on the mode and the step, the mode file owns that order, and a per-gate
    successor list here would go stale the first time a step moved.

    It names `modes/<mode>.md` only when that file is really there. The caller
    is `journal.receipt`, which passes `journal.current_mode`'s answer, and
    that answer is the string "unknown" when nothing recorded a mode_entry —
    the shape check_apply's NO_MODE_ENTRY finding exists to catch. Interpolated
    blindly, the line sent the reader to `modes/unknown.md`, a file the skill
    does not ship. The guard asks the filesystem rather than the one sentinel,
    so the next sentinel, a typo or a renamed mode degrades to the generic
    wording instead of printing a path to nothing.
    """
    known = False
    if mode:
        try:
            import paths
            known = paths.mode_file(mode).exists()
        except (ImportError, OSError):
            known = False
    where = f"the {mode} run" if known else "the run"
    print(f"PASS: {gate} — no findings. This is not the end of {where}; return to "
          f"{'modes/' + mode + '.md' if known else 'the mode file'} and continue "
          "from the step that ran it.", file=sys.stderr)
