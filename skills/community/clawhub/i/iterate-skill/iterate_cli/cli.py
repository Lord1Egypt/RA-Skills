"""iterate CLI entry point.

Provides subcommands for onboarding and personalization management:
    iterate onboard     — Run interactive CLI onboarding wizard (multi-path)
    iterate init        — Non-interactive onboarding from scan defaults (CI/agents)
    iterate personalize — Direct personalization configuration (mid-project)
    iterate refresh     — Incremental refresh of ITERATE.md (preserve user sections)
    iterate reonboard   — Full re-onboarding (backup old files, run wizard)
    iterate status      — Show onboarding status and drift detection
    iterate next        — Guided next action (what to run now, and why)
    iterate scan        — Read-only export of the project tech-stack scan
    iterate report      — Aggregated Markdown/JSON health report (PR/CI friendly)
    iterate export      — Snapshot config + ITERATE.md as a portable JSON bundle
    iterate import      — Restore a bundle (backups written first)
    iterate show        — Read-only resolved config + personalization detail
    iterate doctor      — Project health diagnostics (--json / --json-out / --fix)
    iterate guard       — Defensive-programming pre/post-edit checks (v3.0)
    iterate invariant   — Project-level invariant check (v3.0, defensive mode)
    iterate backup      — List or restore timestamped backups written by write commands
    iterate update      — Self-update the CLI + installed assistant skill dirs
    iterate completion  — Print a bash/zsh/fish completion script
    iterate template    — List or show the skill's bundled templates (read-only)
    iterate help        — Print help for iterate or for one command
    iterate --version   — Print version

All user-facing output is routed through the unified TUI layer
(``iterate_cli.tui``) for consistent skills.sh / Claude Code style styling.
"""

from __future__ import annotations

import argparse
import contextlib
import difflib
import json
import os
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

#: Third-party imports the CLI cannot run without. A ModuleNotFoundError for
#: one of these is a DEPENDENCY GAP (exit 127 per the documented contract:
#: "127 | 依赖缺失"), not a bug — every other import failure is re-raised so a
#: typo in our own modules still surfaces as a traceback.
_REQUIRED_DEPENDENCIES = frozenset({"yaml", "rich"})


def _dependency_exit_code(missing: str) -> int | None:
    """Return the exit code for a missing top-level module, or None to re-raise.

    Extracted from the import guard below so the documented 127 contract is
    unit-testable without having to uninstall PyYAML/rich.
    """
    return 127 if missing in _REQUIRED_DEPENDENCIES else None


try:
    from iterate_cli import __version__
    from iterate_cli.fingerprint import drift_summary
    from iterate_cli.generator import (
        atomic_write,
        has_valid_user_owned_markers,
        write_onboarding_outputs,
    )
    from iterate_cli.refresh import (
        CONFIG_YAML,
        DRIFT_REASON_CORRUPT,
        DRIFT_REASON_DISABLED,
        DRIFT_REASON_NO_FINGERPRINTS,
        REONBOARD_CANCELLED,
        REONBOARD_COMPLETED,
        REONBOARD_NO_CHANGES,
        check_onboarding_drift,
        drift_unavailable_code,
        drift_unavailable_reason,
        full_reonboard,
        get_drift_ignore,
        get_stored_fingerprints,
        is_onboarding_complete,
        load_onboarding_config,
    )
    from iterate_cli.scan import collect_scan_data, render_scan
    from iterate_cli.tui import tui
    from iterate_cli.wizard import NO_CHANGES_NEEDED, run_wizard
except ModuleNotFoundError as _import_error:
    _missing = (_import_error.name or "").split(".")[0]
    _code = _dependency_exit_code(_missing)
    if _code is None:
        raise
    print(
        f"iterate: missing required dependency {_missing!r}. "
        "Install the skill properly (``pip install iterate-skill`` / "
        "``pipx install .``) or add the dependency (``pip install "
        f"{'pyyaml' if _missing == 'yaml' else _missing}``) and retry.",
        file=sys.stderr,
    )
    raise SystemExit(_code) from _import_error


def _should_show_banner(args: argparse.Namespace) -> bool:
    """Determine whether the ASCII banner should be shown.

    Banner is disabled by ``--no-banner`` or the ``ITERATE_NO_BANNER``
    environment variable (any non-empty value), and by a redirected (non-TTY)
    stdout.

    The TTY gate is required, not merely polite: the banner is eight lines of
    block art printed to **stdout**, so without it a piped command captured
    the whole art block ahead of the answer. That directly contradicted the
    promise two lines below the call site — "a bare ``iterate <version>`` line
    is emitted on non-TTY stdout so scripts can parse ``iterate --version``" —
    and broke the same capture for ``iterate config get KEY``, which SKILL.md
    documents as *the* way to read a single value.
    """
    if getattr(args, "no_banner", False):
        return False
    if os.environ.get("ITERATE_NO_BANNER", "").strip():
        return False
    return sys.stdout.isatty()


def _collect_value_options(parser: argparse.ArgumentParser) -> set[str]:
    """Collect every option string that consumes a following value.

    Walks the top-level parser into each subparser so ``--out``, ``--check``,
    ``--set`` etc. are all known, and returns the set of their option strings.
    Used to disambiguate a literal ``--json`` token from a *value* that happens
    to equal ``--json`` (e.g. ``iterate report --out --json`` means "write the
    report to a file literally named ``--json``", not "emit JSON").

    Args:
        parser: The top-level parser.

    Returns:
        The set of option strings that take an argument.
    """
    value_options: set[str] = set()
    seen_parsers: set[int] = set()

    def _walk(p: argparse.ArgumentParser) -> None:
        if id(p) in seen_parsers:
            return
        seen_parsers.add(id(p))
        for action in p._actions:
            if getattr(action, "nargs", None) == 0:
                # store_true/store_false/const/help/version consume no value.
                continue
            value_options.update(action.option_strings)
            if isinstance(action, argparse._SubParsersAction):
                for sub in action.choices.values():
                    if isinstance(sub, argparse.ArgumentParser):
                        _walk(sub)

    _walk(parser)
    return value_options


def _json_requested(argv: list[str], parser: argparse.ArgumentParser) -> bool:
    """Return whether ``--json`` is a real flag request, not a value.

    The old check (``"--json" in argv``) misread a *value* equal to ``--json``
    as a JSON request: ``iterate report --out --json`` (out path literally
    ``--json``) or ``iterate config set goal --json`` made a subsequent usage
    error emit a JSON document even though the caller never asked for one.
    A token is only counted as ``--json`` when it is not the value of a
    preceding value-consuming option (``--out``, ``--check``, ``-p``, ...).

    Args:
        argv: The raw argument list.
        parser: The top-level parser (for value-option introspection).

    Returns:
        True when ``--json`` was passed as a flag.
    """
    value_options = _collect_value_options(parser)
    expect_value = False
    for token in argv:
        if expect_value:
            # This token is the argument of the previous option; it is never a
            # flag, even if its text happens to be ``--json``.
            expect_value = False
            continue
        if token in value_options:
            expect_value = True
            continue
        if token == "--json":
            return True
    return False


def _force_utf8_stdio() -> None:
    """Best-effort switch stdout/stderr to UTF-8 (``errors="replace"``).

    Structured output contains non-ASCII text (Chinese drift advice, etc.);
    on consoles using a legacy/ANSI code page (notably Windows) printing it
    would raise ``UnicodeEncodeError`` and turn a working command into a raw
    traceback. Fails silently when the streams do not support reconfigure.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


# ---------------------------------------------------------------------------
# Typo tolerance — "invalid choice" becomes "did you mean …?"
# ---------------------------------------------------------------------------

#: argparse's message for a rejected choice. Python ≤3.12 quotes the choices
#: (``choose from 'a', 'b'``) and 3.13 dropped the quotes, so the choices are
#: split on commas and de-quoted rather than matched against a fixed layout.
_INVALID_CHOICE_RE = re.compile(
    r"^argument (?P<argument>[^:]+): invalid choice: '(?P<value>[^']*)' "
    r"\(choose from (?P<choices>.*)\)$"
)

#: Set by :meth:`_IterateArgumentParser.error` for the *most recent* rejected
#: choice and read back by ``main()`` so the ``--json`` failure document can
#: carry the same suggestion the human message shows.
#:
#: A module-level slot rather than a parser attribute because the error can be
#: raised by a *sub*parser (``iterate fingerprint verfy``), whose instance is
#: not reachable from the top-level parser ``main()`` holds. ``argparse`` exits
#: immediately after ``error()`` returns, so a single slot can never hold two
#: competing values.
_PENDING_USAGE_SUGGESTION: str | None = None


def _did_you_mean(token: str, choices: list[str] | tuple[str, ...]) -> str | None:
    """Return the closest known choice for ``token``, or None when nothing is close.

    ``cutoff=0.6`` keeps the two failure modes acceptable: below it a
    resemblance as weak as ``status`` → ``stat`` is not worth guessing, and a
    wrong guess is worse than none because the user follows it.
    """
    matches = difflib.get_close_matches(token, list(choices), n=1, cutoff=0.6)
    return matches[0] if matches else None


def _suggestion_from_usage_error(message: str) -> str | None:
    """Extract a "did you mean" suggestion from an argparse error message.

    Only ``invalid choice`` carries an enumerable set to match against; every
    other argparse error (missing value, unrecognised flag) has no useful
    candidate list, so they pass through unchanged.
    """
    match = _INVALID_CHOICE_RE.match(message.strip())
    if match is None:
        return None
    choices = [choice.strip().strip("'\"") for choice in match.group("choices").split(",")]
    choices = [choice for choice in choices if choice]
    return _did_you_mean(match.group("value"), choices)


class _IterateArgumentParser(argparse.ArgumentParser):
    """``ArgumentParser`` that answers "then what should I type?".

    Stock argparse answers a typo with a usage wall and
    ``invalid choice: 'statu' (choose from …)`` — it states the problem but
    never the fix, and on a narrow terminal the fix is scrolled off. This
    subclass appends the one line the user actually needs and records the
    suggestion so ``iterate --json <typo>`` can report it too.

    ``add_subparsers`` hands ``parser_class`` down to each subparser, so a typo
    in a nested choice (``iterate guard precheck``) gets the same treatment.
    """

    def error(self, message: str) -> None:
        global _PENDING_USAGE_SUGGESTION
        suggestion = _suggestion_from_usage_error(message)
        if suggestion is not None:
            _PENDING_USAGE_SUGGESTION = suggestion
            message = (
                f"{message}\n"
                f"did you mean '{suggestion}'? Run `iterate help` to list every command."
            )
        super().error(message)


def _subcommands(parser: argparse.ArgumentParser) -> dict[str, argparse.ArgumentParser]:
    """Return the parser's subcommand map (name → parser), or an empty dict."""
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return dict(action.choices)
    return {}


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code:

        - ``0`` success
        - ``1`` error / cancellation (also ``doctor --strict`` with warnings,
          ``status``/``show`` with a config that exists but cannot be parsed)
        - ``2`` usage error (invalid/unknown arguments, bare ``iterate``, or
          ``--json`` passed to an interactive command)
        - ``127`` a required external dependency is missing
    """
    _force_utf8_stdio()
    parser = _build_parser()
    # Detect --json from the RAW argv: argparse has not run yet, and the
    # global --json help promises "stdout holds exactly one JSON document,
    # including on failure" — so a usage error must still emit JSON when the
    # caller asked for it (a script doing `iterate fingerprint bogus --json |
    # jq` otherwise gets an empty body and a jq parse error). A token equal to
    # ``--json`` that is the VALUE of a preceding option (e.g.
    # ``report --out --json``) is NOT a JSON request.
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    json_requested = _json_requested(raw_argv, parser)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        if json_requested and exc.code not in (0, None):
            # Carry the same "did you mean" the human message got, so a script
            # can act on the suggestion instead of re-parsing stderr.
            payload: dict[str, Any] = {
                "error": "invalid usage",
                "hint": "run `iterate --help`",
            }
            if _PENDING_USAGE_SUGGESTION is not None:
                payload["did_you_mean"] = _PENDING_USAGE_SUGGESTION
            print(json.dumps(payload, ensure_ascii=False))
        raise

    if args.version:
        # `iterate --json --version` honours the JSON contract of the other
        # structured commands instead of emitting the human banner/text.
        if getattr(args, "json", False):
            print(json.dumps({"command": "version", "version": __version__}))
            return 0
        # Structured (JSON) output must not be polluted by the ASCII banner,
        # matching the subcommand paths below.
        if _should_show_banner(args):
            tui.banner()
        # A bare "iterate <version>" line is emitted on non-TTY (piped) stdout
        # so scripts can parse `iterate --version` without ANSI/prompt noise.
        if sys.stdout.isatty():
            tui.info(f"iterate {__version__}")
            tui.empty_line()
            tui.hint(
                "Install the skill across AI assistants: npx iterate-skill-installer"
            )
            tui.hint("Initialize a project: iterate onboard")
        else:
            print(f"iterate {__version__}")
        # Advisory update hint (24h-cached): must never break --version.
        _maybe_print_update_hint()
        return 0

    if args.command == "help":
        # Handled before the project-root check on purpose: `iterate help` asks
        # a question about the CLI, so it must work from a directory where no
        # project exists (and with `-p` pointing anywhere).
        return _cmd_help(
            parser,
            getattr(args, "topic", None),
            json_output=getattr(args, "json", False),
        )

    if args.command == "completion":
        # Same rationale as `help`: completion describes the CLI, not a
        # project, so it must work outside one (and `-p` is irrelevant).
        return _cmd_completion(
            getattr(args, "shell", ""),
            parser,
            json_output=getattr(args, "json", False),
            install=getattr(args, "install", False),
            uninstall=getattr(args, "uninstall", False),
            directory=getattr(args, "dir", None),
            force=getattr(args, "force", False),
        )

    if args.command == "template":
        # Same rationale as help/completion: the templates belong to the skill,
        # not to one project, so this works outside a project (and `-p` is
        # irrelevant). Read-only by construction.
        from iterate_cli.template_cmd import run_template

        return run_template(
            getattr(args, "template_action", None),
            getattr(args, "template_name", None),
            json_output=getattr(args, "json", False),
        )

    # Interactive commands never produce structured output; a caller passing
    # --json to them has a misunderstanding, not a silent success.
    non_json_commands = {"onboard", "personalize", "reonboard"}
    if getattr(args, "json", False) and args.command in non_json_commands:
        message = (
            f"--json is not supported for '{args.command}' (interactive command). "
            "Use `iterate status/show/doctor --json` for structured output, or "
            "`iterate config get KEY --json` for single values."
        )
        # Honour the global --json contract on this failure path too: a script
        # piping `iterate onboard --json | jq` must get one JSON document, not
        # an empty body.
        print(json.dumps({"error": message}, ensure_ascii=False))
        tui.error(message)
        return 2

    project_root = Path(args.project).resolve()

    if not project_root.is_dir():
        # `--json` must put the error on stdout: a script piping
        # `iterate status --json | jq` to a missing/typo'd project path got an
        # empty body plus a bare exit 1, while a corrupt config in the *same*
        # command did emit {"error": ...}. One command, one contract.
        message = f"project directory not found: {project_root}"
        if getattr(args, "json", False):
            print(json.dumps({"error": message}, ensure_ascii=False))
        else:
            # tui.error already renders a ✗ prefix; a literal "Error: " here
            # produced "✗ Error: ..." — the only spot in the codebase stacking
            # both markers.
            tui.error(message)
        return 1

    # Structured (JSON) output must not be polluted by the ASCII banner.
    show_banner = (
        _should_show_banner(args)
        and not getattr(args, "json", False)
        # `report` is a data-producing command: its stdout is the Markdown
        # document, so an art block would corrupt a redirect/CI artifact.
        and args.command != "report"
        # `export --out -` writes the bundle itself to stdout; the banner must
        # not precede it, exactly like --json.
        and not (
            args.command == "export" and getattr(args, "out", None) == "-"
        )
        # `config schema` emits the JSON Schema on stdout (the whole point of
        # the command is a clean machine document), so never banner it.
        and not (
            args.command == "config"
            and getattr(args, "config_action", None) == "schema"
        )
    )

    try:
        return _dispatch_command(args, parser, project_root, show_banner)
    except KeyboardInterrupt:
        # Ctrl+C mid-interaction must not surface a raw traceback.
        # Under `--json` stdout is reserved for the single JSON document, so
        # the human cancellation output is suppressed (it would corrupt it).
        if not getattr(args, "json", False):
            tui.cancel()
            # Deliberately NOT "nothing was written": `config set` may already
            # have copied its backup, `doctor --fix` may have applied fixes, and
            # `update` may have copied files — the old blanket claim was false
            # for exactly the paths where a user is most likely to interrupt.
            tui.hint(
                "已中止；写入类步骤可能已部分完成并留下时间戳备份，请检查项目目录 / "
                "Interrupted mid-run; write steps may have left timestamped backups "
                "(*.configset-*, *.doctorfix-*, .bak-*) — check the project directory.",
                indent=2,
            )
        _emit_json_failure("interrupted (KeyboardInterrupt)", args)
        return 1
    except EOFError:
        # Ctrl+D / closed stdin (e.g. piped without data) mid-prompt. Show a
        # clean cancellation instead of an unhandled-input traceback.
        if not getattr(args, "json", False):
            tui.cancel()
            tui.hint(
                "输入已结束（Ctrl+D / EOF）；已写入的备份文件仍保留在项目目录 / "
                "Input ended (Ctrl+D / EOF); any backups already written remain in "
                "the project directory.",
                indent=2,
            )
        _emit_json_failure("interrupted (EOF on stdin)", args)
        return 1
    except BrokenPipeError:
        # A downstream consumer closed the pipe early (`iterate status --json |
        # head`). Suppress the spurious traceback: redirect stdout to devnull so
        # the interpreter's final flush does not re-raise, then exit non-zero
        # quietly like every other early-terminated stream.
        try:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
        except (OSError, ValueError, AttributeError):
            pass
        return 1


def _dispatch_command(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
    project_root: Path,
    show_banner: bool,
) -> int:
    """Route a parsed subcommand to its handler.

    Centralized so that interactive handlers (onboard, personalize) can be
    wrapped once by the caller for graceful Ctrl+C/EOF handling.
    """
    if args.command == "onboard":
        if show_banner:
            tui.banner()
        return _cmd_onboard(project_root)
    if args.command == "init":
        if show_banner:
            tui.banner()
        return _cmd_init(
            project_root,
            yes=getattr(args, "yes", False),
            dry_run=getattr(args, "dry_run", False),
            json_output=getattr(args, "json", False),
            language=getattr(args, "language", None),
            target_branch=getattr(args, "target_branch", None),
            goal=getattr(args, "goal", None),
        )
    if args.command == "personalize":
        if show_banner:
            tui.banner()
        return _cmd_personalize(
            project_root,
            clear=getattr(args, "clear", False),
            yes=getattr(args, "yes", False),
        )
    if args.command == "refresh":
        if show_banner:
            tui.banner()
        return _cmd_refresh(
            project_root,
            dry_run=getattr(args, "dry_run", False),
            json_output=getattr(args, "json", False),
            show_diff=getattr(args, "diff", False),
        )
    if args.command == "reonboard":
        if show_banner:
            tui.banner()
        return _cmd_reonboard(project_root)
    if args.command == "status":
        if show_banner:
            tui.banner()
        return _cmd_status(project_root, json_output=getattr(args, "json", False))
    if args.command == "next":
        if show_banner:
            tui.banner()
        from iterate_cli.nextcmd import run_next

        return run_next(project_root, json_output=getattr(args, "json", False))
    if args.command == "scan":
        if show_banner:
            tui.banner()
        return _cmd_scan(project_root, json_output=getattr(args, "json", False))
    if args.command == "report":
        # No banner: stdout is the report document itself.
        return _cmd_report(
            project_root,
            out=getattr(args, "out", None),
            strict=getattr(args, "strict", False),
            json_output=getattr(args, "json", False),
            force=getattr(args, "force", False),
        )
    if args.command == "export":
        if show_banner:
            tui.banner()
        return _cmd_export(
            project_root,
            out=getattr(args, "out", None),
            force=getattr(args, "force", False),
            json_output=getattr(args, "json", False),
        )
    if args.command == "import":
        if show_banner:
            tui.banner()
        return _cmd_import(
            project_root,
            bundle_path=getattr(args, "bundle", ""),
            dry_run=getattr(args, "dry_run", False),
            yes=getattr(args, "yes", False),
            reset_fingerprints=getattr(args, "reset_fingerprints", False),
            json_output=getattr(args, "json", False),
        )
    if args.command == "show":
        if show_banner:
            tui.banner()
        return _cmd_show(project_root, json_output=getattr(args, "json", False))
    if args.command == "doctor":
        if show_banner:
            tui.banner()
        return _cmd_doctor(
            project_root,
            json_output=getattr(args, "json", False),
            fix=getattr(args, "fix", False),
            strict=getattr(args, "strict", False),
            json_out=getattr(args, "json_out", None),
            check=getattr(args, "check", None),
            list_checks=getattr(args, "list_checks", False),
        )
    if args.command == "config":
        if show_banner:
            tui.banner()
        return _cmd_config(
            project_root,
            action=getattr(args, "config_action", None),
            key=getattr(args, "key", None),
            value=getattr(args, "value", None),
            json_output=getattr(args, "json", False),
            out=getattr(args, "out", None),
            compact=getattr(args, "compact", False),
            force=getattr(args, "force", False),
        )
    if args.command == "guard":
        if show_banner:
            tui.banner()
        return _cmd_guard(
            project_root,
            guard_action=getattr(args, "guard_action", None),
            targets=getattr(args, "targets", None),
            json_output=getattr(args, "json", False),
            dry_run=getattr(args, "dry_run", False),
        )
    if args.command == "invariant":
        if show_banner:
            tui.banner()
        return _cmd_invariant(
            project_root,
            json_output=getattr(args, "json", False),
            dry_run=getattr(args, "dry_run", False),
        )
    if args.command == "fingerprint":
        if show_banner:
            tui.banner()
        return _cmd_fingerprint(
            project_root,
            json_output=getattr(args, "json", False),
            action=getattr(args, "fingerprint_action", None) or "verify",
        )
    if args.command == "backup":
        if show_banner:
            tui.banner()
        return _cmd_backup(
            project_root,
            action=getattr(args, "backup_action", None) or "list",
            backup_file=getattr(args, "backup_file", None),
            yes=getattr(args, "yes", False),
            dry_run=getattr(args, "dry_run", False),
            json_output=getattr(args, "json", False),
            keep=getattr(args, "keep", None),
            older_than=getattr(args, "older_than", None),
        )
    if args.command == "update":
        if show_banner:
            tui.banner()
        return _cmd_update(
            project_root,
            check_only=getattr(args, "check", False),
            yes=getattr(args, "yes", False),
            json_output=getattr(args, "json", False),
            assistants=getattr(args, "assistants", None),
        )
    if getattr(args, "json", False):
        # A bare `iterate --json` (no subcommand) must not spray the human
        # help text onto stdout: `iterate --json | jq` would choke on it.
        # Emit the one JSON document the contract promises instead.
        print(
            json.dumps(
                {"error": "no subcommand given", "hint": "run `iterate --help`"},
                ensure_ascii=False,
            )
        )
        return 2
    # Bare `iterate` is a usage error: print help to stderr so `iterate | head`
    # in a script does not receive 60 lines of help on the data stream, and
    # return 2 (usage) rather than 0.
    parser.print_help(file=sys.stderr)
    return 2


def _build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser."""
    global _PENDING_USAGE_SUGGESTION
    # A fresh parse must not inherit a suggestion from a previous one; tests
    # build the parser repeatedly in the same process.
    _PENDING_USAGE_SUGGESTION = None
    parser = _IterateArgumentParser(
        prog="iterate",
        description="Iterate skill onboarding and project knowledge management.",
        epilog=(
            "Exit codes:\n"
            "  0    success\n"
            "  1    error / cancellation\n"
            "  2    usage error (invalid or unknown arguments)\n"
            "  127  a required external dependency is missing\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="Show version and exit (also -v for backwards compatibility).",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        default=False,
        help="Disable the ITERATE ASCII art banner at startup.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Emit structured JSON instead of TUI output for status, next, "
        "scan, init, report, export, import, show, doctor, refresh, config, guard, "
        "invariant, fingerprint, backup and update "
        "(and for --version). Interactive commands (onboard/personalize/"
        "reonboard) reject it; on every other path stdout holds exactly one "
        "JSON document, including on failure.",
    )
    parser.add_argument(
        "-p",
        "--project",
        default=".",
        help="Project root directory (default: current directory).",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Shared arguments for subcommands: allows -p and --no-banner after the
    # subcommand, matching the global flags so `iterate status --no-banner`
    # works the same as `iterate --no-banner status`.
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument(
        "-p",
        "--project",
        default=argparse.SUPPRESS,
        help="Project root directory (default: current directory).",
    )
    parent.add_argument(
        "--no-banner",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Disable the ITERATE ASCII art banner at startup.",
    )

    onboard_parser = subparsers.add_parser(
        "onboard",
        parents=[parent],
        help="Run interactive CLI onboarding wizard (multi-path).",
        description="Run the interactive onboarding wizard. First-time projects get "
        "basic onboarding + personalization offer; existing projects get "
        "config update + personalization offer.",
    )
    # Declared so `iterate onboard --json` parses and hits the friendly
    # "interactive commands reject --json" gate instead of an argparse
    # "unrecognized arguments" error (the gate itself refuses the combo).
    onboard_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )
    init_parser = subparsers.add_parser(
        "init",
        parents=[parent],
        help="Non-interactive bootstrap: write ITERATE.md + config from the scan.",
        description="Initialize a project without any prompts. The tech stack, "
        "review dimensions, validation commands and command whitelist are "
        "derived from `iterate scan`; the result is byte-for-byte the same "
        "shape `iterate onboard` writes. Safe to re-run: an initialized "
        "project is reported and left untouched. Non-interactive stdin "
        "requires --yes; add --dry-run to preview without writing.",
    )
    init_parser.add_argument(
        "--yes",
        action="store_true",
        default=False,
        help="Write without a confirmation prompt (required when stdin is not "
        "a terminal).",
    )
    init_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Show what would be detected and written without touching any file.",
    )
    init_parser.add_argument(
        "--language",
        choices=("zh", "en"),
        default=None,
        help="Output language for generated files (default: en, matching the "
        "wizard).",
    )
    init_parser.add_argument(
        "--target-branch",
        default=None,
        help="Git target branch recorded in the config (default: main).",
    )
    init_parser.add_argument(
        "--goal",
        default=None,
        help="Override the default review goal recorded in the config.",
    )
    init_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON report instead of TUI output.",
    )
    personalize_parser = subparsers.add_parser(
        "personalize",
        parents=[parent],
        help="Direct personalization configuration (mid-project).",
        description="Skip basic onboarding and go directly to the 9-step "
        "personalization wizard. Ideal for adding constraints mid-project. "
        "Use --clear to remove all personalization.",
    )
    personalize_parser.add_argument(
        "--clear",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Remove all personalization (structured rules + ITERATE.md "
        "sections) without running the wizard.",
    )
    personalize_parser.add_argument(
        "--yes",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Skip the confirmation prompt (only meaningful with --clear).",
    )
    # Same reachable-gate rationale as onboard: parse --json so the rejection
    # above can print the friendly message instead of an argparse error.
    personalize_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )
    refresh_parser = subparsers.add_parser(
        "refresh",
        parents=[parent],
        help="Incrementally refresh ITERATE.md (preserve user sections).",
        description="Re-scan the project and update AI-maintained sections of ITERATE.md "
        "while preserving user-owned sections. Also updates manifest fingerprints.",
    )
    refresh_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Preview what would change without writing any files.",
    )
    refresh_parser.add_argument(
        "--diff",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Print a unified diff of exactly what refresh would change "
        "(implies a dry-run preview; never writes files).",
    )
    refresh_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON report instead of TUI output.",
    )
    reonboard_parser = subparsers.add_parser(
        "reonboard",
        parents=[parent],
        help="Full re-onboarding (backup old files, run wizard).",
        description="Back up existing ITERATE.md and iterate.config.yaml, then run the "
        "full onboarding wizard from scratch.",
    )
    # Same reachable-gate rationale as onboard / personalize.
    reonboard_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )
    status_parser = subparsers.add_parser(
        "status",
        parents=[parent],
        help="Show onboarding status and drift detection.",
        description="Check whether onboarding is complete and whether the project's "
        "tech stack has drifted since the last onboarding.",
    )
    status_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON report instead of TUI output.",
    )
    next_parser = subparsers.add_parser(
        "next",
        parents=[parent],
        help="Guided next action: what to run now, and why.",
        description="Answer 'what should I do next?' from the project state: "
        "not initialized -> init/onboard; corrupt config -> doctor --fix; "
        "manifest drift -> refresh --diff then refresh; failing checks -> "
        "doctor; healthy -> /iterate <goal>. Read-only and advisory (always "
        "exits 0); --json returns the prioritized plan for scripts and other "
        "skills.",
    )
    next_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit the prioritized plan as one JSON document.",
    )
    scan_parser = subparsers.add_parser(
        "scan",
        parents=[parent],
        help="Show what the project scanner detected (read-only).",
        description="Read-only export of the tech-stack scan that onboarding runs "
        "internally: detected manifests, languages, package managers, top-level "
        "directories, feature flags, and the review dimensions / validation "
        "commands / command whitelist the scanner would suggest. Writes nothing "
        "and always exits 0, so `iterate scan --json` is safe to call from CI.",
    )
    scan_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON report instead of TUI output.",
    )
    report_parser = subparsers.add_parser(
        "report",
        parents=[parent],
        help="Aggregated Markdown/JSON health report for PRs and CI.",
        description="One read-only command that aggregates status, scan and "
        "doctor into a single document. Default output is GitHub-flavoured "
        "Markdown, ready to paste into a PR/issue or save as a CI artifact; "
        "--json emits one structured document instead. --out PATH writes the "
        "document to PATH (stdout by default); --strict makes warnings "
        "blocking. Exit code is 0 when healthy, 1 when the report is blocking, "
        "matching `iterate doctor`.",
    )
    report_parser.add_argument(
        "--out",
        metavar="PATH",
        default=argparse.SUPPRESS,
        help="Write the report to PATH instead of stdout ('-' means stdout).",
    )
    report_parser.add_argument(
        "--force",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Replace an existing --out file (refused by default).",
    )
    report_parser.add_argument(
        "--strict",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Treat warnings as blocking too (exit 1), like `doctor --strict`.",
    )
    report_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON report instead of Markdown.",
    )
    export_parser = subparsers.add_parser(
        "export",
        parents=[parent],
        help="Snapshot config + ITERATE.md as a portable JSON bundle.",
        description="Write the project's iterate state (iterate.config.yaml plus "
        "ITERATE.md) as one portable JSON bundle. Use it to back the state up, "
        "move it to another machine, attach it to a review, or seed the same "
        "profile in another repository. Read-only with respect to the project: "
        "only the bundle file is written. `--json` prints the bundle on stdout "
        "instead of writing a file, so `iterate export --json > state.json` "
        "works.",
    )
    export_parser.add_argument(
        "--out",
        metavar="PATH",
        default=argparse.SUPPRESS,
        help="Write the bundle to PATH (default: iterate-bundle-<UTC>.json in "
        "the project root). '-' writes it to stdout, like --json.",
    )
    export_parser.add_argument(
        "--force",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Overwrite PATH if it already exists (refused by default).",
    )
    export_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Print the bundle to stdout and write nothing.",
    )
    import_parser = subparsers.add_parser(
        "import",
        parents=[parent],
        help="Restore config + ITERATE.md from a bundle (backups first).",
        description="Validate a bundle written by `iterate export` and apply it: "
        "iterate.config.yaml and (when the bundle carries one) ITERATE.md are "
        "written after timestamped backups are taken. The bundle's config is "
        "checked against the schema before anything is touched, so an invalid "
        "or foreign file leaves the project unchanged. Use --dry-run to preview, "
        "--yes for non-interactive/CI use, and --reset-fingerprints when the "
        "bundle comes from a different repository.",
    )
    import_parser.add_argument(
        "bundle",
        metavar="FILE",
        help="Bundle JSON file to import ('-' reads it from stdin).",
    )
    import_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Show what would change without writing anything.",
    )
    import_parser.add_argument(
        "--yes",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Apply without the confirmation prompt (required when stdin is "
        "not a terminal).",
    )
    import_parser.add_argument(
        "--reset-fingerprints",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Drop the bundle's recorded manifest fingerprints before writing, "
        "so a profile exported from another repository does not report that "
        "project's manifests as drift. `iterate refresh` re-records them.",
    )
    import_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON report instead of TUI output.",
    )
    show_parser = subparsers.add_parser(
        "show",
        parents=[parent],
        help="Show resolved config and personalization (read-only).",
        description="Read-only inspection of the resolved project state: "
        "onboarding metadata, effective config, drift status, and the full "
        "personalization detail. Never writes files.",
    )
    show_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON report instead of TUI output.",
    )
    doctor_parser = subparsers.add_parser(
        "doctor",
        parents=[parent],
        help="Run project health diagnostics against the skill.",
        description="Validate the project's iterate.config.yaml, ITERATE.md and "
        "onboarding state against the skill's canonical definitions. "
        "Exits non-zero when errors are found.",
    )
    doctor_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON report instead of TUI output.",
    )
    doctor_parser.add_argument(
        "--json-out",
        metavar="PATH",
        default=argparse.SUPPRESS,
        help="Write a structured JSON report to PATH (created if missing).",
    )
    doctor_parser.add_argument(
        "--fix",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Apply safe, non-destructive fixes to iterate.config.yaml "
        "(backup written first) before running diagnostics.",
    )
    doctor_parser.add_argument(
        "--strict",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Treat warnings as failures too: exit 1 when any warning is "
        "present (default: only errors are blocking). Useful for CI gating.",
    )
    doctor_parser.add_argument(
        "--check",
        action="append",
        metavar="NAME",
        default=argparse.SUPPRESS,
        help="Run only the named check(s) instead of all of them (repeatable, "
        "or comma-separated). Use '--list-checks' to see the valid names.",
    )
    doctor_parser.add_argument(
        "--list-checks",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Print every available check name and exit (no diagnostics run).",
    )
    config_parser = subparsers.add_parser(
        "config",
        parents=[parent],
        help="Inspect or modify config values without the interactive wizard.",
        description="Non-interactive config inspection and editing. With no "
        "action, prints every settable value; 'get KEY' prints one resolved "
        "value; 'set KEY VALUE' validates and writes one value with a "
        "timestamped backup; 'unset KEY' removes one value so it falls back "
        "to its documented default; 'schema' emits the canonical JSON Schema "
        "for iterate.config.yaml (editor/CI tooling).",
    )
    # NOTE: no `choices=` here on purpose. The help promises `get` is the
    # default action ("`iterate config get [KEY]`... get is the default when
    # omitted"), so `iterate config language` must mean `config get language`.
    # With `choices=["get","set","unset"]`, argparse rejected "language" as an
    # invalid choice before `_cmd_config` could reinterpret it as the implicit
    # key. `_cmd_config` now treats any non-action first positional as the key.
    config_parser.add_argument(
        "config_action",
        nargs="?",
        default=None,
        help="Action to perform: 'get' (default when omitted), 'set', "
        "'unset' (restore the documented default), or 'schema' (emit the "
        "canonical config JSON Schema).",
    )
    config_parser.add_argument(
        "key",
        nargs="?",
        default=None,
        help="Flat config key to read, write, or remove (omit to list all keys).",
    )
    config_parser.add_argument(
        "value",
        nargs="?",
        default=None,
        help="Value to set (only used with 'set').",
    )
    config_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON object instead of TUI output.",
    )
    # Schema-only flags. Accepted here (not on a dedicated subparser) so the
    # action stays a plain positional, exactly like get/set/unset.
    config_parser.add_argument(
        "--out",
        default=None,
        help="Write the schema to PATH instead of stdout (schema action only).",
    )
    config_parser.add_argument(
        "--compact",
        action="store_true",
        default=False,
        help="Emit single-line JSON (schema action only).",
    )
    config_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Overwrite an existing --out file (schema action only).",
    )

    guard_parser = subparsers.add_parser(
        "guard",
        parents=[parent],
        help="Defensive-programming pre/post-edit checks (v3.0 defensive mode).",
        description="Deterministic checks a host AI runs around every coding step: "
        "'pre-check' verifies targets exist / worktree is clean / manifests are "
        "ready before editing; 'post-check' executes exactly the configured "
        "validation.commands after editing. Exits non-zero on failure. "
        "On 'post-check', --dry-run previews the exact commands instead of "
        "executing them ('pre-check' never executes anything, so the flag only "
        "labels its output there).",
    )
    guard_parser.add_argument(
        "guard_action",
        choices=["pre-check", "post-check"],
        help="Which guard to run: 'pre-check' (before edits) or 'post-check' (after edits).",
    )
    guard_parser.add_argument(
        "targets",
        nargs="*",
        default=None,
        help="Paths to check (pre-check: must exist; post-check: module names to filter).",
    )
    guard_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON object instead of TUI output.",
    )
    guard_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=argparse.SUPPRESS,
        help="On 'post-check', preview the exact commands that would run "
        "without executing them. 'pre-check' is read-only and never runs "
        "commands, so there the flag only labels the report.",
    )

    invariant_parser = subparsers.add_parser(
        "invariant",
        parents=[parent],
        help="Run project-level invariant checks (v3.0 defensive mode).",
        description="Evaluate the invariants declared under config.invariants "
        "(per-module command lists plus 'ensure' file assertions). Degrades to "
        "validation.commands when no invariants section is configured. "
        "Exits non-zero when any invariant is violated. Use --dry-run to preview.",
    )
    invariant_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON object instead of TUI output.",
    )
    invariant_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Preview the exact commands that would run without executing anything.",
    )

    fingerprint_parser = subparsers.add_parser(
        "fingerprint",
        parents=[parent],
        help="Verify manifest fingerprints against the project state.",
        description="Compare the SHA-256 manifest fingerprints recorded at "
        "onboarding/refresh time against the current project root. Detects "
        "added, removed, and changed tech-stack manifests. Exits non-zero "
        "when drift is detected.",
    )
    fingerprint_parser.add_argument(
        "fingerprint_action",
        nargs="?",
        choices=["verify", "list"],
        default="verify",
        help="Action to perform: 'verify' (default) compares recorded "
        "fingerprints against the project; 'list' prints what was recorded "
        "at the last onboarding/refresh without rescanning.",
    )
    fingerprint_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON object instead of TUI output.",
    )

    backup_parser = subparsers.add_parser(
        "backup",
        parents=[parent],
        help="List, restore or prune timestamped backups written by write "
        "commands.",
        description="List, restore or prune the timestamped backups other "
        "iterate commands write before mutating project state (config "
        "set/unset, doctor --fix, refresh, personalize, onboard, import, "
        "reonboard). 'list' (default) enumerates every recognisable backup in "
        "the project root, newest first; 'restore FILE' puts one back, taking "
        "a fresh backup of the current file first so the restore is itself "
        "reversible; 'prune' deletes old backups under a retention policy. "
        "Restore and prune never touch a file that does not look like an "
        "iterate backup.",
    )
    backup_parser.add_argument(
        "backup_action",
        nargs="?",
        choices=["list", "restore", "prune"],
        default="list",
        help="Action to perform: 'list' (default) enumerates backups; "
        "'restore FILE' restores one backup file to its original name; "
        "'prune' deletes old backups (see --keep / --older-than).",
    )
    backup_parser.add_argument(
        "backup_file",
        nargs="?",
        default=None,
        help="Backup file to restore (required with 'restore').",
    )
    backup_parser.add_argument(
        "--yes",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Restore without a confirmation prompt (required when stdin is "
        "not a terminal).",
    )
    backup_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Show what would be restored without writing anything.",
    )
    backup_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON object instead of TUI output.",
    )
    backup_parser.add_argument(
        "--keep",
        metavar="N",
        type=int,
        default=argparse.SUPPRESS,
        help="With 'prune': keep the N newest backups of each original file "
        "and delete the rest (must be >= 1).",
    )
    backup_parser.add_argument(
        "--older-than",
        metavar="AGE",
        default=argparse.SUPPRESS,
        help="With 'prune': delete backups older than AGE (e.g. '30d', '7d', "
        "'24h', '90m', or a plain number of days).",
    )

    update_parser = subparsers.add_parser(
        "update",
        parents=[parent],
        help="Self-update the CLI and installed assistant skill dirs.",
        description="Check the latest iterate-skill release, verify its SHA-256, "
        "and apply it: refresh installed assistant skill directories (SKILL.md, "
        "config/, iterate_cli/, scripts/, templates/, ...) and reinstall the "
        "CLI package into the current environment. --check only compares "
        "versions without downloading or writing anything.",
    )
    update_parser.add_argument(
        "--check",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Only compare versions; never download or write.",
    )
    update_parser.add_argument(
        "--yes",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Apply the update without a confirmation prompt (required for "
        "non-interactive/CI runs).",
    )
    update_parser.add_argument(
        "--assistants",
        nargs="+",
        default=None,
        help="Restrict the skill-dir refresh to these assistants (default: all "
        "detected). Omit to refresh all detected assistants.",
    )
    update_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit a structured JSON outcome instead of TUI output (implies "
        "a write operation, so it requires --yes).",
    )

    help_parser = subparsers.add_parser(
        "help",
        parents=[parent],
        help="Show help for iterate or for one command.",
        description="Print the top-level usage overview, or the detailed help "
        "for one command (`iterate help doctor`). Equivalent to `iterate "
        "--help` and `iterate doctor --help`, spelled the way most CLIs spell it.",
    )
    help_parser.add_argument(
        "topic",
        nargs="?",
        default=None,
        help="Command to describe (omit for the top-level overview).",
    )

    completion_parser = subparsers.add_parser(
        "completion",
        parents=[parent],
        help="Print a shell completion script (bash/zsh/fish).",
        description="Print a ready-to-install shell completion script generated "
        "from the same parser as `--help`, so Tab completion can never drift "
        "from the real command/option list. Completes commands, flags, fixed "
        "value choices and path arguments. The script is printed to stdout: "
        "`iterate completion zsh > \"${fpath[1]}/_iterate\"`. With --install, "
        "write it to the shell's conventional per-user completion path instead; "
        "with --uninstall, remove it again.",
    )
    completion_parser.add_argument(
        "shell",
        choices=("bash", "zsh", "fish"),
        help="Shell to generate completion for.",
    )
    completion_parser.add_argument(
        "--install",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Install the script to the shell's per-user completion path "
        "instead of printing it.",
    )
    completion_parser.add_argument(
        "--uninstall",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Remove the installed completion file (idempotent; safe to re-run).",
    )
    completion_parser.add_argument(
        "--dir",
        metavar="DIR",
        default=argparse.SUPPRESS,
        help="With --install/--uninstall, use DIR instead of the default path.",
    )
    completion_parser.add_argument(
        "--force",
        action="store_true",
        default=argparse.SUPPRESS,
        help="With --install, replace an existing completion file.",
    )
    # Same reachable-gate rationale as help: parse --json so the friendly
    # rejection can emit one JSON document instead of an argparse error.
    completion_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )

    template_parser = subparsers.add_parser(
        "template",
        parents=[parent],
        help="List or show the skill's bundled templates (read-only).",
        description="List every bundled template the skill ships (the ITERATE.md "
        "skeleton, the AI onboarding playbook, the decision-log structure) and "
        "print one verbatim. Read-only: never writes and never touches the "
        "project, so it works from any directory. This is the discoverable "
        "surface for the templates the generator otherwise consumes silently — "
        "see what structure onboarding produces, or copy a template to customise "
        "it for your own team.",
    )
    template_parser.add_argument(
        "template_action",
        nargs="?",
        choices=["list", "show"],
        default="list",
        help="Action to perform: 'list' (default) enumerates every bundled "
        "template; 'show NAME' prints one template's content verbatim.",
    )
    template_parser.add_argument(
        "template_name",
        nargs="?",
        default=None,
        help="Template to show (required with 'show'; accepts a filename or an "
        "alias such as 'iterate', 'playbook' or 'decisions').",
    )
    # Same reachable-gate rationale as help: parse --json so the friendly
    # rejection can emit one JSON document instead of an argparse error.
    template_parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )

    return parser


def _init_failure(message: str, json_output: bool, code: int = 1) -> int:
    """Report an ``iterate init`` failure honouring the ``--json`` contract.

    Mirrors ``_bundle_failure``: under ``--json`` stdout carries exactly one
    JSON document (with ``ok: false`` so a caller can branch on it), while the
    human-readable line goes to stderr.
    """
    if json_output:
        print(
            json.dumps(
                {"ok": False, "command": "init", "error": message},
                ensure_ascii=False,
            )
        )
    tui.error(message)
    return code


def _prune_dimension_sets(
    suggested: dict[str, dict[str, Any]], dimensions: list[str]
) -> dict[str, dict[str, Any]]:
    """Restrict suggested dimension sets to globally enabled dimensions.

    The wizard guarantees a blueprint never references a dimension the user
    disabled; ``init`` derives both lists from the same scan, so the same
    invariant must hold. Sets whose dimensions are all filtered out are
    dropped rather than persisted as empty (schema requires ``minItems: 1``).
    """
    enabled = set(dimensions)
    pruned: dict[str, dict[str, Any]] = {}
    for name, spec in suggested.items():
        dims = [d for d in spec.get("dimensions", []) if d in enabled]
        if dims:
            pruned[name] = {"dimensions": dims}
    return pruned


def _cmd_init(
    project_root: Path,
    *,
    yes: bool = False,
    dry_run: bool = False,
    json_output: bool = False,
    language: str | None = None,
    target_branch: str | None = None,
    goal: str | None = None,
) -> int:
    """Handle ``iterate init`` — non-interactive onboarding from scan defaults.

    Interactive ``onboard`` cannot be driven from CI, a script, or another
    skill (it blocks on prompts). ``init`` runs the same scanner and writes the
    same two artifacts with the same generator, but takes every value from the
    scan and the documented defaults. It is deliberately *fresh-project only*:
    an existing config is reported and left untouched (use ``onboard`` /
    ``refresh`` to change it), so a re-run in CI can never clobber a tuned
    project. An existing ITERATE.md is only rewritten when it carries the
    USER-OWNED markers, whose section is preserved.
    """
    from iterate_cli.dimension_sets import suggest_dimension_sets
    from iterate_cli.fingerprint import capture_fingerprints
    from iterate_cli.generator import (
        DEFAULT_GOAL,
        DEFAULT_LANGUAGE,
        DEFAULT_TARGET_BRANCH,
        OnboardingData,
    )
    from iterate_cli.scan import (
        scan_project,
        suggest_command_whitelist,
        suggest_dimensions,
        suggest_validation_commands,
    )

    config_path = project_root / CONFIG_YAML
    md_path = project_root / "ITERATE.md"

    if config_path.is_file():
        if load_onboarding_config(project_root) is None:
            return _init_failure(
                f"{config_path.name} exists but could not be parsed; refusing "
                "to overwrite it. Run `iterate doctor` to diagnose and fix the "
                "config first.",
                json_output,
            )
        message = (
            f"{config_path.name} already exists — this project is already "
            "initialized; nothing was changed. Use `iterate refresh` to update "
            "AI-maintained sections, `iterate onboard` to change settings, or "
            "`iterate doctor` to check health."
        )
        if json_output:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "command": "init",
                        "initialized": False,
                        "already_initialized": True,
                        "project": str(project_root),
                        "message": message,
                    },
                    ensure_ascii=False,
                )
            )
        else:
            tui.info(message)
        return 0

    existing_md: str | None = None
    if md_path.is_file():
        try:
            existing_md = md_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            return _init_failure(
                f"cannot read existing {md_path.name}: {exc}. Fix the file "
                "permissions/encoding and retry.",
                json_output,
            )
        if not has_valid_user_owned_markers(existing_md):
            return _init_failure(
                f"existing {md_path.name} is missing the USER-OWNED section "
                "markers; refusing to overwrite possibly hand-edited content. "
                "Restore <!-- ITERATE:USER-OWNED:START --> / ...END -->, or run "
                "`iterate reonboard` which backs the file up first.",
                json_output,
            )

    if language is not None and language not in ("zh", "en"):
        return _init_failure(
            f"unsupported language {language!r}; choose 'zh' or 'en'.",
            json_output,
            code=2,
        )
    if target_branch is not None and not target_branch.strip():
        return _init_failure(
            "--target-branch must not be empty.", json_output, code=2
        )
    if goal is not None and not goal.strip():
        return _init_failure("--goal must not be empty.", json_output, code=2)

    with tui.status("正在扫描项目 / Scanning project..."):
        scan = scan_project(project_root)
    dimensions = suggest_dimensions(scan)
    validation_commands = suggest_validation_commands(scan)
    command_whitelist = suggest_command_whitelist(scan)
    dimension_sets = _prune_dimension_sets(
        suggest_dimension_sets(scan), dimensions
    )
    fingerprints = capture_fingerprints(project_root)

    data = OnboardingData(
        project_root=project_root,
        channel="cli",
        scan=scan,
        dimensions=dimensions,
        dimension_sets=dimension_sets,
        target_branch=target_branch or DEFAULT_TARGET_BRANCH,
        validation_commands=validation_commands,
        command_whitelist=command_whitelist,
        fingerprints=fingerprints,
        language=language or DEFAULT_LANGUAGE,
        goal=goal or DEFAULT_GOAL,
    )

    plan: dict[str, Any] = {
        "project": str(project_root),
        "would_write": [md_path.name, config_path.name],
        "detected_languages": list(scan.detected_languages),
        "manifests": list(scan.manifests),
        "dimensions": list(dimensions),
        "dimension_sets": dimension_sets,
        "validation_commands": validation_commands,
        "command_whitelist": list(command_whitelist),
        "target_branch": data.target_branch,
        "language": data.language,
    }

    if dry_run:
        if json_output:
            print(
                json.dumps(
                    {"ok": True, "command": "init", "dry_run": True, **plan},
                    ensure_ascii=False,
                )
            )
            return 0
        tui.intro("Iterate Skill — Init preview")
        _render_init_plan(plan)
        tui.hint("Dry run: nothing was written. Re-run without --dry-run to apply.")
        return 0

    if not yes:
        # Order matters: a --json caller in CI gets the usage error (2) rather
        # than the generic non-TTY error, matching `update --json`.
        if json_output:
            return _init_failure(
                "--json implies a write, so it requires --yes (or use --dry-run "
                "to preview).",
                json_output,
                code=2,
            )
        if not _stdin_is_interactive():
            return _init_failure(
                "Non-interactive stdin detected; pass --yes to initialize this "
                "project (or --dry-run to preview).",
                json_output,
                code=2,
            )
        if not _confirm(
            f"Initialize {project_root}? This writes ITERATE.md and "
            "iterate.config.yaml.",
            default=True,
        ):
            tui.info("已取消 / Cancelled; nothing was written.")
            return 1

    try:
        iterate_md_path, written_config = write_onboarding_outputs(
            data, project_root, existing_md
        )
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return _init_failure(
            f"failed to write onboarding files: {exc}. Nothing was left "
            "half-written (the generator rolls back on failure); check "
            "directory permissions and retry.",
            json_output,
        )

    written = [iterate_md_path.name, written_config.name]
    if json_output:
        print(
            json.dumps(
                {
                    "ok": True,
                    "command": "init",
                    "initialized": True,
                    "dry_run": False,
                    "written": written,
                    **{k: v for k, v in plan.items() if k != "would_write"},
                    "next_actions": [
                        "iterate doctor",
                        "iterate show",
                        "iterate scan --json",
                        "iterate report",
                    ],
                },
                ensure_ascii=False,
            )
        )
        return 0

    tui.empty_line()
    tui.success("Project initialized (no prompts).")
    _render_init_plan(plan, show_targets=False)
    tui.key_value("Written", ", ".join(written))
    tui.empty_line()
    tui.hint("Next: `iterate doctor` to verify, `iterate show` to inspect.")
    return 0


def _render_init_plan(plan: dict[str, Any], *, show_targets: bool = True) -> None:
    """Render the detected stack / generated config summary for ``init``."""
    langs = ", ".join(plan.get("detected_languages") or []) or "— (none detected)"
    tui.key_value("Project", str(plan.get("project", "")))
    tui.key_value("Tech stack", langs)
    tui.key_value(
        "Dimensions", ", ".join(plan.get("dimensions") or []) or "—"
    )
    sets = plan.get("dimension_sets") or {}
    tui.key_value(
        "Dimension sets", ", ".join(sorted(sets)) if sets else "— (none)"
    )
    modules = plan.get("validation_commands") or {}
    if modules:
        tui.key_value(
            "Validation",
            "; ".join(f"{name}: {len(cmds)} command(s)" for name, cmds in modules.items()),
        )
    else:
        tui.key_value("Validation", "— (no commands detected)")
    tui.key_value("Target branch", str(plan.get("target_branch", "")))
    tui.key_value("Language", str(plan.get("language", "")))
    if show_targets and plan.get("would_write"):
        tui.key_value("Will write", ", ".join(plan["would_write"]))


def _cmd_onboard(project_root: Path) -> int:
    """Handle the 'onboard' subcommand with multi-path branching."""
    data = run_wizard(project_root)
    if data is NO_CHANGES_NEEDED:
        # Returning user explicitly declined all updates.
        tui.info("No changes made. Onboarding is already complete.")
        return 0
    if data is None:
        # User cancelled mid-flow (gate, basic wizard, or personalization
        # that was accepted but then aborted).
        return 1

    # Preserve the user-owned section of ITERATE.md when re-onboarding an
    # existing project, so manual edits and personalization content survive.
    existing_md: str | None = None
    existing_md_path = project_root / "ITERATE.md"
    if existing_md_path.is_file():
        try:
            existing_md = existing_md_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            # If ITERATE.md exists but cannot be read, regenerating from scratch
            # would silently drop the user-owned (manual) section. Refuse to
            # proceed rather than risk losing manual edits.
            tui.warning(f"未能读取现有 {existing_md_path.name}：{exc}")
            tui.info("为避免覆盖你的手动编辑区，已中止。请先修复该文件读取问题。")
            return 1
        # An ITERATE.md without the USER-OWNED markers cannot preserve manual
        # edits — regenerating would silently replace them with the template.
        # Refuse and point the user at `iterate reonboard` (which backs the
        # file up first) instead of overwriting possibly hand-edited content.
        if not has_valid_user_owned_markers(existing_md):
            tui.error(
                "Existing ITERATE.md is missing the USER-OWNED section markers; "
                "refusing to overwrite possibly hand-edited content."
            )
            tui.hint(
                "Restore the markers <!-- ITERATE:USER-OWNED:START --> / ...END -->, "
                "or run `iterate reonboard` which backs up the file first.",
                indent=2,
            )
            return 1

    # Preserve existing personalization when the user did not re-personalize,
    # so a basic-config update does not silently drop structured rules
    # (protected paths, risk areas, extra validation commands, etc.) or
    # free-form notes/conventions stored in ITERATE.md.
    if data.personalization is None:
        from iterate_cli.personalize import load_existing_personalization

        existing_config = load_onboarding_config(project_root) or {}
        existing_personalization = load_existing_personalization(
            project_root, existing_config
        )
        if not existing_personalization.is_empty():
            data.personalization = existing_personalization

    # A corrupt existing iterate.config.yaml must not be silently overwritten
    # by onboarding output (every other writer refuses; mirror that so
    # partially-recoverable hand edits are not discarded).
    config_path = project_root / CONFIG_YAML
    if config_path.is_file() and load_onboarding_config(project_root) is None:
        tui.error(
            "iterate.config.yaml exists but could not be parsed; refusing to "
            "overwrite it with onboarding output."
        )
        tui.hint(
            "Run 'iterate doctor' to diagnose and fix the config first.",
            indent=2,
        )
        return 1

    try:
        iterate_md, config_yaml = write_onboarding_outputs(
            data, project_root, existing_md
        )
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        # Writing either artifact failed (disk full, permissions, locked file,
        # a corrupt template, or a generated ITERATE.md missing the USER-OWNED
        # markers). Surface a clear message instead of a bare traceback; the
        # writer already rolled back partially-written files.
        tui.error(f"写入 onboarding 产物失败：{exc}")
        tui.warning(
            "未写入或已回滚 ITERATE.md / iterate.config.yaml，请检查目录权限后重试。"
        )
        return 1
    tui.empty_line()
    tui.success("Onboarding complete!")
    tui.key_value("Written", str(iterate_md))
    tui.key_value("Written", str(config_yaml))
    if data.personalization is not None:
        tui.key_value("Personalization", "applied")
    tui.empty_line()
    tui.hint("You can now use /iterate in your AI coding tool.")
    return 0


def _cmd_personalize(project_root: Path, clear: bool = False, yes: bool = False) -> int:
    """Handle the 'personalize' subcommand — direct personalization configuration.

    Without ``clear``, runs the 9-step personalization wizard (with existing
    content pre-loaded for editing). With ``clear``, removes all
    personalization (structured rules + ITERATE.md sections) after a
    confirmation prompt (bypassed with ``yes``).

    Args:
        project_root: Project root directory.
        clear: When True, clear personalization instead of running the wizard.
        yes: When True, skip the clear confirmation prompt.

    Returns:
        Exit code: 0 on success/nothing-to-clear, 1 on failure/cancel.
    """
    from iterate_cli.personalize import (
        CorruptConfigError,
        has_personalization,
        load_existing_personalization,
        run_personalize_wizard,
        save_personalization,
    )

    # ``--yes`` only has meaning with ``--clear`` (its own help says so).
    # Silently ignoring it let a user believe the interactive wizard had been
    # auto-confirmed; make it a usage error instead.
    if yes and not clear:
        tui.error(
            "--yes is only meaningful with --clear; the personalize wizard "
            "prompts for each step and has no confirmation to skip."
        )
        return 2

    # Personalization requires existing onboarding (ITERATE.md + config).
    if not is_onboarding_complete(project_root):
        tui.warning("Onboarding not yet completed. Run 'iterate onboard' first.")
        return 1

    config_path = project_root / "iterate.config.yaml"
    if not config_path.is_file():
        tui.warning("iterate.config.yaml not found. Run 'iterate onboard' first.")
        return 1

    if clear:
        return _cmd_personalize_clear(project_root, yes=yes, has=has_personalization)

    # Validate the config BEFORE running the 9-step wizard: the strict loader
    # is otherwise only reached at save time, so the user would complete every
    # prompt and then have all of it discarded by a CorruptConfigError.
    # `personalize --clear` and `onboard` both fail fast here too.
    try:
        from iterate_cli.personalize import load_config_strict

        load_config_strict(config_path)
    except CorruptConfigError as exc:
        tui.error(str(exc))
        tui.hint("Run `iterate doctor` for details.", indent=2)
        return 1

    # Load existing personalization for editing (structured from config +
    # free-form notes/conventions from ITERATE.md) so re-running the wizard
    # preserves previously entered content instead of wiping it.
    existing_config = load_onboarding_config(project_root) or {}
    existing_personalization = load_existing_personalization(
        project_root, existing_config
    )

    personalization = run_personalize_wizard(
        project_root,
        existing=existing_personalization,
    )
    if personalization is None:
        return 1

    # Save structured fields to config.yaml and free-form notes/conventions
    # to ITERATE.md atomically (with rollback on failure). A corrupt config
    # must not be rewritten over, so the strict loader's error is surfaced
    # cleanly instead of a bare traceback.
    try:
        config_path, iterate_md_path = save_personalization(
            project_root, personalization
        )
    except CorruptConfigError as exc:
        tui.error(str(exc))
        return 1
    except (OSError, UnicodeDecodeError) as exc:
        tui.error(f"Failed to write personalization: {exc}")
        return 1

    tui.empty_line()
    tui.success("Personalization saved!")
    tui.key_value("Updated", str(config_path))
    tui.key_value("Updated", str(iterate_md_path))
    return 0


def _cmd_personalize_clear(
    project_root: Path,
    yes: bool,
    has: Callable[[Path, dict[str, Any]], bool],
) -> int:
    """Handle ``iterate personalize --clear`` — reset all personalization.

    Args:
        project_root: Project root directory.
        yes: When True, skip the confirmation prompt.
        has: The ``has_personalization`` callable (injected for testability).

    Returns:
        Exit code: 0 on success/nothing-to-clear, 1 on failure/cancel.
    """
    from iterate_cli.personalize import (
        CorruptConfigError,
        clear_personalization,
        load_config_strict,
    )

    # A corrupt config is not "nothing to clear": silently treating it as such
    # would hide the damage. Surface it as a clean error (return 1) instead.
    try:
        config = load_config_strict(project_root / "iterate.config.yaml")
    except CorruptConfigError as exc:
        tui.error(str(exc))
        return 1
    except (OSError, UnicodeDecodeError) as exc:
        tui.error(f"Failed to read iterate.config.yaml: {exc}")
        return 1

    if not has(project_root, config):
        tui.info("No personalization to clear.")
        return 0

    if not yes:
        import builtins

        from iterate_cli.wizard import _ask_yes_no
        # Mirror `iterate update`: refuse before prompting rather than letting
        # builtins.input() raise EOFError into the generic handler. The old
        # path printed the question, hit EOF, then reported
        # "Input ended (Ctrl+D / EOF), nothing was written" — which never
        # mentions the `--yes` flag written for exactly this case, so a CI
        # caller had no way to learn how to proceed.
        if not _stdin_is_interactive():
            tui.hint(
                "Non-interactive stdin detected. Pass --yes to confirm "
                "clearing personalization without a prompt."
            )
            return 1

        confirmed = _ask_yes_no(
            "确认清空所有个性化配置? / Confirm clearing all personalization?",
            builtins.input,
            default=False,
        )
        if not confirmed:
            tui.info("已取消 / Cancelled.")
            # Cancel → 1: the docstring at the top of this command promises
            # "1 on failure/cancel", and `onboard`/`reonboard` already
            # returned 1 for a user cancel — returning 0 here made "user
            # said no" indistinguishable from "personalization cleared".
            return 1

    try:
        config_path, iterate_md_path = clear_personalization(project_root)
    except CorruptConfigError as exc:
        tui.error(str(exc))
        return 1
    except (OSError, UnicodeDecodeError) as exc:
        tui.error(f"Failed to clear personalization: {exc}")
        return 1

    tui.empty_line()
    tui.success("Personalization cleared!")
    tui.key_value("Updated", str(config_path))
    if iterate_md_path.is_file():
        tui.key_value("Updated", str(iterate_md_path))
    return 0


def _cmd_show(project_root: Path, json_output: bool = False) -> int:
    """Handle the 'show' subcommand — read-only resolved config inspection.

    Args:
        project_root: Project root directory.
        json_output: When True, emit a structured JSON report.

    Returns:
        Exit code: 0 on success.
    """
    from iterate_cli.show import run_show

    return run_show(project_root, json_output=json_output)


def _print_diff(diff: str, label: str) -> None:
    """Print a unified diff block with a compact header.

    The diff already carries ``---`` / ``+++`` file labels, so the header only
    names the file for human scanning; the diff body is printed verbatim so
    added/removed markers stay at column 0 and can be copy-pasted or fed to
    ``git apply --check``. Output goes to stdout (the data stream) so a
    pipeline can capture it.

    Args:
        diff: The unified diff text (from ``refresh.unified_diff``).
        label: Human-readable file label for the section header.
    """
    print(f"--- {label} ---")
    print(diff, end="" if diff.endswith("\n") else "\n")


def _cmd_refresh(
    project_root: Path,
    dry_run: bool = False,
    json_output: bool = False,
    show_diff: bool = False,
) -> int:
    """Handle the 'refresh' subcommand.

    Args:
        project_root: Project root directory.
        dry_run: When True, only preview what would change without writing.
        json_output: When True, emit a structured JSON report instead of TUI
            lines. With ``--dry-run --json`` the preview is reported without
            writing; with ``--json`` alone the refresh runs and reports what
            changed.
        show_diff: When True, print a unified diff of exactly what refresh
            would change and write nothing. Implies the preview path (a diff
            of a change you have not applied yet is what the user wants), so
            ``--diff`` is incompatible with an actual write: combining it with
            a real refresh would either lie about the write or show a diff of
            nothing. Under ``--json`` the diff strings ride in ``md_diff`` /
            ``config_diff``.

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
    from iterate_cli.refresh import incremental_refresh, preview_refresh

    def _json(error: str = "") -> dict[str, Any]:
        payload: dict[str, Any] = {
            "project": str(project_root),
            "ok": error == "",
            "dry_run": dry_run or show_diff,
            "diff": show_diff,
            "changed": False,
            "config_changed": False,
            "md_changed_lines": 0,
            "stats": {},
        }
        if error:
            payload["error"] = error
        return payload

    if not is_onboarding_complete(project_root):
        # stdout must be exactly one JSON document under --json; the human
        # warning on the same stream made `iterate refresh --json | jq` die
        # with a parse error, since tui.warning() writes to stdout.
        if json_output:
            print(json.dumps(_json("onboarding not completed"), ensure_ascii=False))
        else:
            tui.warning("Onboarding not yet completed. Run 'iterate onboard' first.")
        return 1

    if show_diff:
        # A diff is a preview: never write. Compute the would-be content and
        # render its unified diff so the user sees exactly what a refresh
        # would apply, not just how many lines.
        preview = preview_refresh(project_root, include_diff=True)
        if not preview["ok"]:
            if json_output:
                print(json.dumps(_json(preview["error"]), ensure_ascii=False))
            else:
                tui.error(
                    f"Refresh diff failed. Could not read ITERATE.md / "
                    f"iterate.config.yaml: {preview['error']}"
                )
            return 1
        if json_output:
            print(
                json.dumps(
                    {
                        "project": str(project_root),
                        "ok": True,
                        "dry_run": True,
                        "diff": True,
                        "changed": preview["changed"],
                        "config_changed": preview["config_changed"],
                        "md_changed_lines": preview["md_changed_lines"],
                        "stats": preview["stats"],
                        "md_diff": preview.get("md_diff", ""),
                        "config_diff": preview.get("config_diff", ""),
                    },
                    ensure_ascii=False,
                )
            )
            return 0
        md_diff = preview.get("md_diff", "")
        config_diff = preview.get("config_diff", "")
        if not md_diff and not config_diff:
            tui.success(
                "No changes needed — ITERATE.md and iterate.config.yaml are "
                "already up to date."
            )
            return 0
        tui.warning("Refresh would apply the following changes:")
        if md_diff:
            _print_diff(md_diff, "ITERATE.md")
        if config_diff:
            _print_diff(config_diff, "iterate.config.yaml")
        tui.empty_line()
        tui.hint(
            "Run 'iterate refresh' (without --diff) to apply these changes.",
            indent=2,
        )
        return 0

    if dry_run:
        preview = preview_refresh(project_root)
        if not preview["ok"]:
            if json_output:
                print(json.dumps(_json(preview["error"]), ensure_ascii=False))
            else:
                tui.error(
                    f"Refresh preview failed. Could not read ITERATE.md / iterate.config.yaml: "
                    f"{preview['error']}"
                )
            return 1
        if json_output:
            print(
                json.dumps(
                    {
                        "project": str(project_root),
                        "ok": True,
                        "dry_run": True,
                        "changed": preview["changed"],
                        "config_changed": preview["config_changed"],
                        "md_changed_lines": preview["md_changed_lines"],
                        "stats": preview["stats"],
                    },
                    ensure_ascii=False,
                )
            )
            return 0
        if preview["changed"]:
            stats = preview["stats"]
            tui.warning("Refresh would make the following changes:")
            tui.key_value(
                "ITERATE.md", f"{preview['md_changed_lines']} line(s) changed"
            )
            tui.bullet(
                f"+{stats.get('added', 0)} / -{stats.get('removed', 0)}",
                indent=4,
            )
            tui.key_value(
                "iterate.config.yaml",
                "would be updated" if preview["config_changed"] else "unchanged",
            )
            tui.empty_line()
            tui.hint(
                "Run 'iterate refresh' (without --dry-run) to apply these changes.",
                indent=2,
            )
        else:
            tui.success(
                "No changes needed — ITERATE.md and iterate.config.yaml are already up to date."
            )
        return 0

    if json_output:
        # Preview first to report accurate changed/line statistics, then apply.
        preview = preview_refresh(project_root)
        if not preview["ok"]:
            print(json.dumps(_json(preview["error"]), ensure_ascii=False))
            return 1
        success = incremental_refresh(project_root)
        if not success:
            print(json.dumps(_json("refresh failed (see stderr)"), ensure_ascii=False))
            return 1
        print(
            json.dumps(
                {
                    "project": str(project_root),
                    "ok": True,
                    "dry_run": False,
                    "changed": preview["changed"],
                    "config_changed": preview["config_changed"],
                    "md_changed_lines": preview["md_changed_lines"],
                    "stats": preview["stats"],
                    # Additive caveat: these numbers come from the PREVIEW
                    # scan taken before apply (apply re-scans independently),
                    # so a file edited between preview and apply makes what
                    # was actually written differ from these figures. Labelled
                    # instead of silently implying post-apply accuracy.
                    "stats_basis": "pre-apply",
                },
                ensure_ascii=False,
            )
        )
        return 0

    success = incremental_refresh(project_root)
    if success:
        tui.success("Incremental refresh complete.")
        tui.hint(
            "AI-maintained sections updated, user-owned sections preserved.", indent=2
        )
        return 0
    else:
        tui.error(
            "Refresh failed. Could not read or write ITERATE.md / iterate.config.yaml (see stderr)."
        )
        return 1


def _cmd_reonboard(project_root: Path) -> int:
    """Handle the 'reonboard' subcommand."""
    if not is_onboarding_complete(project_root):
        tui.warning("No existing onboarding found. Run 'iterate onboard' first.")
        return 1

    status = full_reonboard(project_root)
    if status == REONBOARD_COMPLETED:
        tui.success("Full re-onboarding complete.")
        tui.hint("Old files backed up with .bak-<timestamp> suffix.", indent=2)
        return 0
    elif status == REONBOARD_NO_CHANGES:
        tui.info("Re-onboarding not needed — no changes to apply.")
        tui.hint("旧文件未改动，临时备份已清理 / Old files are intact; the temporary backup was removed.", indent=2)
        return 0
    elif status == REONBOARD_CANCELLED:
        # Cancelling is a normal (non-error) user decision; mirror onboarding's
        # cancel message and exit code so scripts see "not written" clearly.
        tui.cancel()
        tui.hint(
            "Re-onboarding cancelled. Old files are intact (the temporary "
            "backup was removed — nothing was written).",
            indent=2,
        )
        return 1
    else:
        # REONBOARD_FAILED may be a backup failure (nothing was backed up) or
        # a write failure after a successful backup; say so accurately.
        tui.error(
            "Re-onboarding failed (see stderr). Old files are backed up "
            "only when the backup step succeeded."
        )
        return 1


def _count_personalization_rules(personalization: dict[str, Any]) -> int:
    """Count structured personalization rules for status display.

    Kept as the CLI-facing name (tests and ``_cmd_status`` use it); the shared
    implementation lives in :func:`iterate_cli.personalize.count_personalization_rules`
    so ``iterate report`` and ``iterate status`` always agree.

    Args:
        personalization: The ``personalization`` section of iterate.config.yaml.
            May be None or non-dict if the config was manually edited;
            in that case 0 is returned.

    Returns:
        Total number of structured personalization rules across all categories.
    """
    from iterate_cli.personalize import count_personalization_rules

    return count_personalization_rules(personalization)


def _cmd_scan(project_root: Path, json_output: bool = False) -> int:
    """Handle the 'scan' subcommand.

    Thin wrapper: the scanner and its renderer live in ``iterate_cli.scan`` so
    the same pure functions the wizard and refresh use are the ones this
    command reports. Read-only and non-gating — it returns 0 for any project
    that exists, including one where nothing was recognised.
    """
    return render_scan(collect_scan_data(project_root), json_output=json_output)


def _cmd_report(
    project_root: Path,
    *,
    out: str | None = None,
    strict: bool = False,
    json_output: bool = False,
    force: bool = False,
) -> int:
    """Handle ``iterate report`` — aggregated Markdown/JSON health report.

    The report itself is built by :mod:`iterate_cli.report`; this handler owns
    the CLI contract: protect iterate's own state files from ``--out``, write
    atomically, honour the "one JSON document on stdout" promise, and mirror
    ``doctor``'s exit code (errors block; ``--strict`` adds warnings).
    """
    from iterate_cli.generator import atomic_write
    from iterate_cli.report import build_report, render_markdown, report_json

    if out is not None and out.strip() == "":
        message = "--out must not be empty (omit it to print to stdout)."
        return _bundle_failure(message, json_output, code=2)

    payload = build_report(project_root, strict=strict)
    text = report_json(payload) if json_output else render_markdown(payload)
    code = 1 if payload["summary"]["blocking"] else 0

    if out is None or out == "-":
        sys.stdout.write(text)
        sys.stdout.flush()
        return code

    target = Path(out)
    protected = {
        (project_root / CONFIG_YAML).resolve(),
        (project_root / "ITERATE.md").resolve(),
    }
    if target.resolve() in protected:
        return _bundle_failure(
            f"refusing to overwrite {target.resolve()} — that is iterate's own "
            "state file, not a report. Choose another --out path.",
            json_output,
            code=2,
        )
    if target.exists() and not force:
        return _bundle_failure(
            f"refusing to overwrite existing file {target} (use --force to replace it).",
            json_output,
            code=2,
        )
    if not target.parent.is_dir():
        # A bad --out path is a usage error (exit 2), consistent with the
        # overwrite-refusal and protected-state refusals in this same function.
        return _bundle_failure(
            f"parent directory does not exist: {target.parent}",
            json_output,
            code=2,
        )
    try:
        atomic_write(target, text)
    except OSError as exc:
        return _bundle_failure(f"cannot write {target}: {exc}", json_output)

    # The document went to a file; stdout stays empty for scripts. The hint is
    # stderr-only so `report --out x > y` cannot interleave text.
    print(f"report: written to {target}", file=sys.stderr)
    return code


def _emit_json_failure(message: str, args: argparse.Namespace) -> None:
    """Emit one JSON error document when ``--json`` was requested.

    ``KeyboardInterrupt`` / ``EOFError`` used to exit with an empty stdout
    under ``--json``, so ``iterate status --json | jq`` reported a JSON parse
    error instead of the cancellation. Kept separate from the human hint so
    stdout still holds exactly one document on these paths.
    """
    if getattr(args, "json", False):
        try:
            print(
                json.dumps(
                    {"error": message, "cancelled": True}, ensure_ascii=False
                )
            )
        except BrokenPipeError:
            pass


def _bundle_failure(message: str, json_output: bool, code: int = 1) -> int:
    """Report an export/import failure honouring the ``--json`` contract.

    Under ``--json`` stdout must hold exactly one JSON document, so the error
    goes there and the human line goes to stderr (``tui.error`` is stderr-only).
    """
    if json_output:
        print(json.dumps({"error": message}, ensure_ascii=False))
    tui.error(message)
    return code


def _cmd_export(
    project_root: Path,
    *,
    out: str | None = None,
    force: bool = False,
    json_output: bool = False,
) -> int:
    """Handle ``iterate export`` — snapshot the project state as a bundle.

    ``--json`` (or ``--out -``) prints the bundle and writes nothing; otherwise
    the bundle is written to ``--out`` or to a timestamped file in the project
    root. The project itself is never modified, so this is safe on a dirty
    worktree and safe to run in CI.
    """
    from iterate_cli.portable import (
        BundleError,
        build_bundle,
        bundle_to_json,
        default_bundle_name,
        summarize_bundle,
    )

    if json_output and out not in (None, "-"):
        return _bundle_failure(
            "--json already prints the bundle on stdout; drop --out (or use "
            "--out alone to write a file).",
            json_output,
            code=2,
        )

    try:
        bundle = build_bundle(project_root)
    except BundleError as exc:
        return _bundle_failure(str(exc), json_output)

    text = bundle_to_json(bundle)
    from iterate_cli.portable import MAX_BUNDLE_BYTES

    if len(text.encode("utf-8", "replace")) > MAX_BUNDLE_BYTES:
        return _bundle_failure(
            f"the bundle is larger than {MAX_BUNDLE_BYTES // (1024 * 1024)} MiB "
            "and could not be imported back; trim ITERATE.md or export from a "
            "smaller project.",
            json_output,
        )
    if json_output or out == "-":
        # The bundle *is* the output here: write it raw so the caller can
        # redirect/pipeline it. json.dumps output is ASCII-safe JSON (UTF-8 by
        # contract), so no TUI/markup layer is wanted or applied.
        sys.stdout.write(text)
        sys.stdout.flush()
        return 0

    target = Path(out) if out else project_root / default_bundle_name()
    # --force must never destroy iterate's own state: writing the bundle JSON
    # over iterate.config.yaml (or ITERATE.md) was the only CLI path that
    # replaced a file without a backup, and it suggested importing the
    # resulting JSON as if it were a config.
    protected_targets = {
        (project_root / CONFIG_YAML).resolve(),
        (project_root / "ITERATE.md").resolve(),
    }
    if target.resolve() in protected_targets:
        return _bundle_failure(
            f"refusing to overwrite {target.resolve()} — that is iterate's own "
            "state file, not a bundle. Choose another --out path.",
            json_output,
            code=2,
        )
    if target.exists() and not force:
        return _bundle_failure(
            f"{target} already exists; pass --force to overwrite it or choose "
            "another --out path.",
            json_output,
            code=2,
        )
    if not target.parent.is_dir():
        # A bad --out path is a usage error (exit 2), matching report --out and
        # the other --out refusals instead of falling back to the generic 1.
        return _bundle_failure(
            f"parent directory does not exist: {target.parent}",
            json_output,
            code=2,
        )
    try:
        atomic_write(target, text)
    except OSError as exc:
        return _bundle_failure(f"cannot write {target}: {exc}", json_output)

    summary = summarize_bundle(bundle)
    if json_output:  # pragma: no cover - excluded by the usage check above
        print(json.dumps({"written": str(target)}, ensure_ascii=False))
        return 0

    tui.empty_line()
    tui.success(f"Bundle written: {target}")
    tui.key_value("Project", str(summary["project"] or ""))
    tui.key_value(
        "Config",
        f"{len(summary['config_keys'])} key(s) in "
        f"{len(summary['config_sections'])} section(s)",
    )
    tui.key_value(
        "ITERATE.md",
        f"included ({summary['iterate_md_lines']} line(s))"
        if summary["has_iterate_md"]
        else "not present — bundle carries config only",
    )
    tui.hint(f"Restore with `iterate import {target.name}`", indent=2)
    tui.hint(
        "Importing into a different repository? add --reset-fingerprints so the "
        "exporting project's manifests are not reported as drift.",
        indent=2,
    )
    return 0


def _render_import_changes(changes: dict[str, Any], limit: int = 30) -> None:
    """Render the config delta as aligned key/value rows.

    ``tui.key_value`` wraps long values with the continuation aligned to the
    value column; a hand-rolled comma list wrapped at the console edge instead
    and dumped its continuation at column 0, which read as a different row.
    """
    config = changes.get("config") or {}
    rows = (
        ("Changed", config.get("changed") or []),
        ("Added", config.get("added") or []),
        ("Removed", config.get("removed") or []),
    )
    printed = False
    for label, keys in rows:
        keys = [str(key) for key in keys]
        if not keys:
            continue
        printed = True
        shown = keys[:limit]
        suffix = f", … (+{len(keys) - limit} more)" if len(keys) > limit else ""
        tui.key_value(f"{label} ({len(keys)})", ", ".join(shown) + suffix)
    if not printed:
        tui.key_value("Config", "unchanged")


def _cmd_import(
    project_root: Path,
    *,
    bundle_path: str,
    dry_run: bool = False,
    yes: bool = False,
    reset_fingerprints: bool = False,
    json_output: bool = False,
) -> int:
    """Handle ``iterate import`` — validate a bundle, then apply it.

    Nothing is written until the bundle has passed structural and schema
    validation, and (unless ``--yes``) the user has confirmed the delta. Every
    existing file is backed up before it is replaced.
    """
    from iterate_cli.portable import (
        MAX_BUNDLE_BYTES,
        BundleError,
        apply_bundle,
        diff_against_project,
        parse_bundle_text,
        summarize_bundle,
        validate_bundle,
    )

    if not bundle_path:
        return _bundle_failure(
            "no bundle file given; usage: iterate import FILE", json_output, code=2
        )

    if bundle_path == "-":
        source = "<stdin>"
        try:
            # Cap the read itself: reading an unbounded stdin into memory is
            # exactly what the size limit exists to prevent, and checking the
            # length only after read_text()/read() has already allocated the
            # whole document is too late for a multi-GiB file. Read through the
            # underlying byte stream when available so the cap is BYTES (a
            # text-mode read(n) counts characters, letting a multi-byte CJK
            # bundle transiently buffer up to ~4x the cap); the authoritative
            # byte check in parse_bundle_text still applies either way.
            stdin_buffer = getattr(sys.stdin, "buffer", None)
            if stdin_buffer is not None:
                text = stdin_buffer.read(MAX_BUNDLE_BYTES + 1).decode(
                    "utf-8", errors="replace"
                )
            else:
                text = sys.stdin.read(MAX_BUNDLE_BYTES + 1)
        except (OSError, UnicodeDecodeError) as exc:
            return _bundle_failure(f"cannot read {source}: {exc}", json_output)
    else:
        source = bundle_path
        path = Path(bundle_path)
        if not path.is_file():
            return _bundle_failure(
                f"bundle not found: {path} (pass '-' to read from stdin)",
                json_output,
            )
        try:
            if path.stat().st_size > MAX_BUNDLE_BYTES:
                return _bundle_failure(
                    f"{path} is larger than {MAX_BUNDLE_BYTES // (1024 * 1024)} "
                    "MiB; that is not an iterate bundle.",
                    json_output,
                )
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            return _bundle_failure(f"cannot read {path}: {exc}", json_output)

    try:
        bundle = parse_bundle_text(text, source=source)
    except BundleError as exc:
        return _bundle_failure(str(exc), json_output)

    # parse_bundle_text() returns the document; warnings (unknown keys, schema
    # unavailable) are advisory and recomputed here so they can be reported.
    warnings = validate_bundle(bundle).warnings
    summary = summarize_bundle(bundle)
    changes = diff_against_project(
        project_root, bundle, reset_fingerprints=reset_fingerprints
    )

    if dry_run:
        if json_output:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "dry_run": True,
                        "project": str(project_root),
                        "source": source,
                        "bundle": summary,
                        "changes": changes,
                        "would_write": changes["would_write"],
                        "fingerprints_reset": bool(reset_fingerprints),
                        "warnings": warnings,
                    },
                    ensure_ascii=False,
                )
            )
            return 0
        tui.intro("Iterate Skill — Import preview")
        tui.key_value("Bundle", source)
        tui.key_value("Exported by", f"iterate {summary['skill_version']} ({summary['exported_at']})")
        tui.key_value("Project in bundle", str(summary["project"] or "—"))
        tui.key_value("Will write", ", ".join(changes["would_write"]))
        tui.section("Config changes / 配置变更")
        _render_import_changes(changes)
        tui.key_value("ITERATE.md", str(changes["iterate_md"]))
        if reset_fingerprints:
            tui.hint("Recorded fingerprints will be dropped (--reset-fingerprints).")
        for warning in warnings:
            tui.warning(warning)
        tui.hint("Dry run: nothing was written. Re-run without --dry-run to apply.")
        return 0

    if not yes:
        # Usage mistakes (a write requested via --json without --yes) are exit
        # 2 on every terminal; checking non-TTY first made the identical
        # invocation return 1 in CI and 2 on a TTY.
        if json_output:
            return _bundle_failure(
                "--json implies a write, so it requires --yes (like `iterate "
                "update --json`).",
                json_output,
                code=2,
            )
        if not _stdin_is_interactive():
            return _bundle_failure(
                "Non-interactive stdin detected; pass --yes to apply this "
                "import (or --dry-run to preview it).",
                json_output,
                code=2,
            )
        if not _confirm(
            f"Apply this bundle to {project_root}? Existing files are backed up.",
            default=False,
        ):
            if json_output:  # pragma: no cover - json needs --yes above
                print(json.dumps({"ok": False, "error": "cancelled"}, ensure_ascii=False))
            tui.info("已取消 / Cancelled; nothing was written.")
            return 1

    try:
        report = apply_bundle(
            project_root, bundle, reset_fingerprints=reset_fingerprints
        )
    except BundleError as exc:
        return _bundle_failure(str(exc), json_output)

    if json_output:
        print(
            json.dumps(
                {
                    "ok": True,
                    "dry_run": False,
                    "project": str(project_root),
                    "source": source,
                    "written": report["written"],
                    "backups": report["backups"],
                    "fingerprints_reset": report["fingerprints_reset"],
                    "changes": changes,
                    "warnings": warnings,
                },
                ensure_ascii=False,
            )
        )
        return 0

    tui.empty_line()
    tui.success("Bundle imported.")
    tui.key_value("Written", ", ".join(report["written"]))
    if report["backups"]:
        tui.key_value("Backups", ", ".join(report["backups"]))
    if report["fingerprints_reset"]:
        tui.hint("Fingerprints were reset; `iterate refresh` re-records them.")
    for warning in warnings:
        tui.warning(warning)
    tui.hint("Verify the result with `iterate doctor` (add --fix to repair).")
    return 0


def _cmd_completion(
    shell: str,
    parser: argparse.ArgumentParser,
    json_output: bool = False,
    install: bool = False,
    uninstall: bool = False,
    directory: str | None = None,
    force: bool = False,
) -> int:
    """Handle ``iterate completion <shell>``.

    The script goes to stdout untouched so it can be redirected straight into
    the shell's completion directory. Installation hints go to stderr only on
    an interactive terminal, so ``iterate completion zsh > _iterate`` never
    mixes prose into the generated file. With ``--install`` the script is
    written to the shell's conventional per-user path (or ``--dir``); with
    ``--uninstall`` that file is removed again.

    Args:
        shell: ``bash`` / ``zsh`` / ``fish`` (validated by argparse, re-checked
            here for programmatic callers).
        parser: Top-level parser to introspect.
        json_output: True when ``--json`` was passed. Without ``--install`` or
            ``--uninstall`` completion output is a shell script, not data, so
            that combination is a usage error; with either install flag it
            emits one result document.
        install: Write the script to disk instead of stdout.
        uninstall: Remove the installed script from disk instead of stdout.
        directory: Optional ``--dir`` override for ``--install``/``--uninstall``.
        force: Replace an existing completion file when true.

    Returns:
        Exit code: 0 on success, 2 for a usage error or unsupported shell,
        1 when an install/uninstall write fails.
    """
    from iterate_cli.completion import (
        SHELLS,
        install_completion,
        install_hint,
        render_completion,
        uninstall_completion,
    )

    if install and uninstall:
        return _bundle_failure(
            "--install and --uninstall are mutually exclusive.",
            json_output,
            code=2,
        )

    if not install and not uninstall and (directory is not None or force):
        return _bundle_failure(
            "--dir only makes sense with --install/--uninstall, and "
            "--force only with --install.",
            json_output,
            code=2,
        )

    if install:
        if directory is not None and not directory.strip():
            return _bundle_failure(
                "--dir must not be empty (omit it to use the default path).",
                json_output,
                code=2,
            )
        try:
            result = install_completion(
                shell,
                parser,
                directory=directory,
                force=force,
            )
        except FileExistsError as exc:
            return _bundle_failure(str(exc), json_output, code=2)
        except ValueError as exc:
            return _bundle_failure(str(exc), json_output, code=2)
        except OSError as exc:
            return _bundle_failure(f"cannot install completion: {exc}", json_output)
        if json_output:
            print(json.dumps(result, ensure_ascii=False))
        else:
            tui.success(f"Completion installed: {result['path']}")
            tui.hint(result["reload_hint"])
        return 0

    if uninstall:
        if force:
            return _bundle_failure(
                "--force only makes sense with --install.",
                json_output,
                code=2,
            )
        if directory is not None and not directory.strip():
            return _bundle_failure(
                "--dir must not be empty (omit it to use the default path).",
                json_output,
                code=2,
            )
        try:
            result = uninstall_completion(shell, directory=directory)
        except ValueError as exc:
            return _bundle_failure(str(exc), json_output, code=2)
        except OSError as exc:
            return _bundle_failure(
                f"cannot remove completion: {exc}", json_output
            )
        if json_output:
            print(json.dumps(result, ensure_ascii=False))
        else:
            if result["removed"]:
                tui.success(f"Completion removed: {result['path']}")
            else:
                tui.hint(
                    f"No completion file at {result['path']}; nothing to remove."
                )
            tui.hint(result["reload_hint"])
        return 0

    if json_output:
        message = (
            "--json is not supported for 'completion' without --install or "
            "--uninstall (it prints a shell script). Use `iterate report "
            "--json` for structured project data, or add --install/--uninstall "
            "to get one JSON result document."
        )
        print(json.dumps({"error": message}, ensure_ascii=False))
        tui.error(message)
        return 2

    try:
        script = render_completion(shell, parser)
    except ValueError as exc:
        message = str(exc)
        print(json.dumps({"error": message}, ensure_ascii=False))
        tui.error(message)
        return 2

    sys.stdout.write(script)
    sys.stdout.flush()
    # The hint must go to stderr: in `iterate completion zsh > _iterate` the
    # shell keeps stderr on the terminal, so a stdout hint would corrupt the
    # file the user is installing.
    if sys.stderr.isatty() and shell in SHELLS:
        print(install_hint(shell), file=sys.stderr)
    return 0


def _cmd_help(
    parser: argparse.ArgumentParser,
    topic: str | None,
    json_output: bool = False,
) -> int:
    """Handle ``iterate help [command]``.

    ``iterate --help`` already existed; what was missing is the *command*
    spelling every other CLI answers to, and per-command help without having to
    remember the ``--help`` flag position. An unknown topic is a usage error
    (exit 2) that names the closest command, matching how a mistyped top-level
    command is now reported.

    Args:
        parser: The top-level parser (source of the subcommand help texts).
        topic: Command name to describe, or None for the overview.
        json_output: True when ``--json`` was requested. Help is prose, so this
            is refused rather than silently emitting a JSON document that
            carries no help text.

    Returns:
        Exit code: 0 when help was printed; 2 for a ``--json`` misuse or an
        unknown topic.
    """
    if json_output:
        message = (
            "--json is not supported for 'help' (it prints human-readable help). "
            "Run `iterate help` for the text, or `iterate status/scan/doctor --json` "
            "for structured output."
        )
        print(json.dumps({"error": message}, ensure_ascii=False))
        tui.error(message)
        return 2

    if topic is None:
        parser.print_help()
        return 0

    subcommands = _subcommands(parser)
    sub = subcommands.get(topic)
    if sub is not None:
        sub.print_help()
        return 0

    suggestion = _did_you_mean(topic, list(subcommands))
    message = f"unknown command: '{topic}'"
    if suggestion is not None:
        message += f" — did you mean '{suggestion}'?"
    else:
        message += ". Run `iterate help` to list every command."
    tui.error(message)
    return 2


def _cmd_status(project_root: Path, json_output: bool = False) -> int:
    """Handle the 'status' subcommand.

    Output is routed through the TUI layer but keeps plain-text keywords
    (``Onboarded``, ``Not onboarded``, ``Drift``, ``No drift``,
    ``Personalization: N rule(s)``) so that automated tests and grep-based
    checks continue to work. Note that ``tui.warning``/``tui.error`` write to
    **stderr** (stdout is the data stream): a not-onboarded or drifted verdict
    is a warning, so grep on stdout alone will not see it — use
    ``--json`` (whose payload carries ``onboarded``/``drift``/
    ``drift_detected``/``drift_reason``) for machine checks. When
    ``json_output`` is True, a structured JSON blob is emitted instead.
    """
    # Structured gathering shared by both render modes. Onboarding state and
    # config are loaded exactly once so the JSON and TUI branches cannot drift
    # from each other (and re-reading the file mid-render cannot yield a stale
    # half-loaded snapshot).
    data: dict[str, Any] = {"project": str(project_root)}
    onboarded = is_onboarding_complete(project_root)
    config_path = project_root / CONFIG_YAML
    data["config_exists"] = config_path.is_file()
    # Load whenever the FILE exists — regardless of onboarding state. The old
    # `onboarded and config_exists` gate meant "config present, ITERATE.md
    # missing" (half-done onboarding, deleted ITERATE.md) reported
    # config_ok=false for a file that was never even parsed, and made the two
    # renderers disagree about the exit code. Parsing is what "config_ok"
    # describes; onboarding is a separate axis.
    config = (
        load_onboarding_config(project_root) if data["config_exists"] else None
    )
    data["config_ok"] = config is not None
    data["onboarded"] = onboarded

    # Stable key set: these keys are emitted in EVERY payload (onboarded or
    # not) so `--json` consumers can index them unconditionally instead of
    # guarding each with `if key in payload`. Defaults mirror the "no config
    # loaded" semantics.
    data["completed_at"] = "unknown"
    data["channel"] = "unknown"
    data["skill_version"] = "unknown"
    data["drift_check"] = True
    data["fingerprints"] = 0
    data["personalization_rules"] = 0
    data["drift"] = "unknown"
    data["drift_detected"] = None
    # A corrupt config is its own reason code, not the generic "unknown": a
    # consumer can then tell "could not check because the file is broken" from
    # "no baseline exists yet".
    data["drift_reason"] = (
        DRIFT_REASON_CORRUPT if (data["config_exists"] and config is None)
        else "unknown"
    )
    data["drifted_added"] = []
    data["drifted_removed"] = []
    data["drifted_changed"] = []

    drift = None
    # Distinguish a parsed-but-empty config ({}) from a corrupt/absent one:
    # an empty mapping is a legitimate parse, so the detail keys are still
    # emitted (with defaults) instead of the payload being silently truncated.
    if config is not None:
        onboarding = (
            config.get("onboarding")
            if isinstance(config.get("onboarding"), dict)
            else {}
        )
        data["completed_at"] = onboarding.get("completed_at", "unknown")
        data["channel"] = onboarding.get("channel", "unknown")
        data["skill_version"] = onboarding.get("skill_version", "unknown")
        drift_enabled = onboarding.get("drift_check", True)
        data["drift_check"] = drift_enabled
        raw_fingerprints = onboarding.get("fingerprints") or []
        data["fingerprints"] = (
            len(raw_fingerprints) if isinstance(raw_fingerprints, list) else 0
        )
        personalization = config.get("personalization") or {}
        data["personalization_rules"] = (
            _count_personalization_rules(personalization) if personalization else 0
        )

        # Only run drift detection for an ONBOARDED project (and only when the
        # check is enabled). Without ITERATE.md there is no baseline to drift
        # from, and computing it anyway made `status --json` emit
        # `drift_detected: true` with concrete drifted_* lists for a project
        # that `show --json` and the TUI branch below both describe as
        # "unknown" — one project state, two contradictory answers. Reuse the
        # already-loaded config instead of re-reading the file.
        drift = (
            check_onboarding_drift(project_root, config)
            if (onboarded and data["drift_check"])
            else None
        )
        # Machine-readable "why is there no drift result" code, derived from the
        # shared helper so status/show/fingerprint cannot disagree. A computed
        # result has no reason code: emitting "unknown" alongside
        # `drift_detected: false` made a healthy project look unverifiable.
        data["drift_reason"] = (
            None if drift is not None
            else drift_unavailable_code(project_root, config)
        )
        if not data["drift_check"]:
            # "Check disabled" must be distinguishable from a genuine
            # "unknown" state for JSON consumers (the TUI already renders it
            # correctly).
            data["drift"] = "disabled"
            data["drift_detected"] = None
        elif drift is None:
            data["drift"] = "unknown"
            data["drift_detected"] = None
        else:
            data["drift"] = drift_summary(drift)
            data["drift_detected"] = drift.has_drift
        # Machine-readable drift detail (B4): scripts can key off
        # drift_detected plus the concrete added/removed/changed lists
        # instead of parsing the human summary string.
        data["drifted_added"] = list(drift.added) if drift is not None else []
        data["drifted_removed"] = list(drift.removed) if drift is not None else []
        data["drifted_changed"] = list(drift.changed) if drift is not None else []

    if json_output:
        import json

        # ``default=str``: a hand-edited config can carry non-JSON YAML scalars
        # (an unquoted ``completed_at`` loads as a ``datetime.date``/datetime).
        # Without this, `status --json` raised TypeError and printed NO document
        # at all — breaking the "stdout holds exactly one JSON document"
        # contract on the one path CI relies on.
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        # A config that exists but could not be parsed is a failure, matching
        # the TUI renderer's exit code for the same condition so CI scripts
        # cannot silently treat a broken config as success.
        if data["config_exists"] and not data["config_ok"]:
            return 1
        return 0

    return _render_status_tui(project_root, data, config, drift)


def _render_status_tui(
    project_root: Path,
    data: dict[str, Any],
    config: dict[str, Any] | None,
    drift: Any,
) -> int:
    """Render the TUI view of ``_cmd_status`` data."""
    tui.intro("Iterate Skill — Status")
    tui.key_value("Project", str(project_root))
    tui.empty_line()

    if not data["onboarded"]:
        tui.warning("Status: Not onboarded")
        if data["config_exists"] and not data["config_ok"]:
            # Surface a corrupt/empty config even pre-onboarding, and exit 1 to
            # match the --json branch: one state, one exit code.
            tui.error(
                "Status: iterate.config.yaml is present but is empty or could "
                "not be parsed"
            )
            tui.hint("Run 'iterate doctor' for details.", indent=2)
            return 1
        tui.hint("Run 'iterate onboard' to initialize.", indent=2)
        return 0

    tui.success("Status: Onboarded")

    if config is None:
        if data["config_exists"]:
            tui.error(
                "Status: iterate.config.yaml is present but is empty or could "
                "not be parsed"
            )
            tui.hint("Run 'iterate doctor' for details.", indent=2)
            return 1
        tui.hint("(iterate.config.yaml not found — only ITERATE.md exists)", indent=2)
        return 0

    tui.key_value("Completed", str(data["completed_at"]))
    tui.key_value("Channel", str(data["channel"]))
    tui.key_value("Skill version", str(data["skill_version"]))

    # Drift configuration summary.
    drift_enabled = data["drift_check"]
    fp_count = data["fingerprints"]
    tui.key_value("Fingerprints", f"{fp_count} manifest(s)")
    tui.key_value("Drift check", "enabled" if drift_enabled else "disabled")

    # Show personalization summary (metadata ``version`` field excluded).
    if data["personalization_rules"]:
        # Use plain info() to keep 'Personalization: N rule(s)' as a
        # contiguous substring (tests assert this exact text).
        tui.info(f"Personalization: {data['personalization_rules']} rule(s)", indent=2)

    # Surface drift and actionable advice (already computed once above).
    if drift is None:
        if not drift_enabled:
            tui.key_value("Drift", "check disabled")
        elif fp_count == 0:
            tui.key_value("Drift", "no fingerprints recorded yet")
        else:
            tui.key_value("Drift", "unknown")
    elif drift.has_drift:
        tui.warning(f"Drift: {drift.summary()}", indent=2)
        tui.hint(drift.advice(), indent=4)
    else:
        tui.success("Drift: No drift detected", indent=2)

    return 0


def _cmd_doctor(
    project_root: Path,
    json_output: bool = False,
    fix: bool = False,
    strict: bool = False,
    json_out: str | None = None,
    check: list[str] | None = None,
    list_checks: bool = False,
) -> int:
    """Handle the 'doctor' subcommand — project health diagnostics.

    When ``fix`` is True, safe non-destructive config fixes are applied
    (with a timestamped backup) before diagnostics are re-run.

    When ``json_out`` is set, the structured report is additionally written
    to that file (its parent directory is created as needed).

    When ``strict`` is True, warnings flip the exit code to 1 (errors are
    always blocking); this lets CI gate on any non-clean state.

    When ``list_checks`` is True, every available check name is printed and
    nothing is run.

    When ``check`` is given, only those named checks run (the preamble a
    config-dependent check needs still runs silently, surfacing only errors).

    Args:
        project_root: Project root directory.
        json_output: When True, emit a structured JSON report.
        fix: When True, apply safe config fixes before running diagnostics.
        strict: When True, warnings are treated as failures.
        json_out: When set, export the JSON report to this path.
        check: Optional list of check names to run (None = all checks).
        list_checks: When True, list the available check names and exit.

    Returns:
        Exit code: 0 when healthy, 1 when errors are found (or warnings too
        under --strict).
    """
    from iterate_cli.doctor import (
        DOCTOR_CHECK_NAMES,
        export_report_json,
        render_report,
        run_doctor,
        run_doctor_fix,
    )

    if list_checks:
        if json_output:
            print(
                json.dumps(
                    {"ok": True, "checks": list(DOCTOR_CHECK_NAMES)},
                    ensure_ascii=False,
                )
            )
        else:
            tui.intro("Iterate Skill — Doctor checks")
            for name in DOCTOR_CHECK_NAMES:
                tui.key_value(name, "", indent=2)
            tui.hint(
                "Run one with `iterate doctor --check <name>`.",
                indent=2,
            )
        return 0

    # --check is repeatable and each value may itself be comma-separated.
    check_names: set[str] | None = None
    if check:
        check_names = {
            piece.strip()
            for value in check
            for piece in value.split(",")
            if piece.strip()
        }
        # `--check ""` / `--check ","` / `--check "   "` yield an EMPTY set
        # after stripping. An empty filter must never silently run zero checks
        # and exit 0 ("healthy") — that would make a CI gate pass without
        # validating anything. Treat it as the usage error it is.
        if not check_names:
            if json_output:
                print(
                    json.dumps(
                        {
                            "project": str(project_root),
                            "skill_version": __version__,
                            "healthy": False,
                            "blocking": True,
                            "strict": strict,
                            "has_errors": True,
                            "has_warnings": False,
                            "fixes": [],
                            "findings": [],
                            "error": "no check names given to --check",
                            "hint": "run `iterate doctor --list-checks`",
                        },
                        ensure_ascii=False,
                    )
                )
            else:
                tui.error("`--check` requires at least one check name.")
                tui.hint("Run `iterate doctor --list-checks` for the available names.", indent=2)
            return 2

    fixes: list[str] = []
    if fix:
        ok, fixes = run_doctor_fix(project_root)
        if not ok:
            if json_output:
                # Match the FULL DoctorReport JSON contract (project/
                # skill_version/healthy/blocking/strict/has_errors/
                # has_warnings/fixes/findings) so consumers can decode a
                # failed --fix with the same keys as a successful run — the
                # hand-built payload previously omitted the boolean signals.
                print(
                    json.dumps(
                        {
                            "project": str(project_root),
                            "skill_version": __version__,
                            "healthy": False,
                            "blocking": True,
                            "strict": strict,
                            "has_errors": True,
                            "has_warnings": False,
                            # run_doctor_fix returns the fixes it detected even
                            # when the write fails; surface them so a failed run
                            # carries the same keys/content as a successful one.
                            "fixes": fixes,
                            "findings": [
                                {
                                    "severity": "error",
                                    "check": "config",
                                    "message": (
                                        "doctor --fix failed: could not read or safely "
                                        "fix iterate.config.yaml (run `iterate doctor` "
                                        "without --fix for details)."
                                    ),
                                    "detail": "",
                                }
                            ],
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                )
                return 1
            tui.error(
                "doctor --fix: could not read or safely fix iterate.config.yaml (see stderr)."
            )
            return 1
        if not json_output:
            if fixes:
                tui.success(f"doctor --fix: applied {len(fixes)} safe fix(es).")
                for fix_note in fixes:
                    tui.bullet(fix_note, indent=4)
                # Transparency note: --fix rewrites the config via a YAML dump,
                # which drops hand-written comments. A backup IS taken
                # (*.doctorfix-*) but the output never said either thing, so an
                # operator could discover the comment loss only after the fact.
                tui.hint(
                    "iterate.config.yaml is rewritten as clean YAML — hand-written "
                    "comments are not preserved (pre-fix backup: *.doctorfix-* next "
                    "to the config).",
                    indent=4,
                )
                tui.empty_line()
            else:
                tui.success("doctor --fix: no safe fixes needed.")
                tui.empty_line()

    try:
        report = run_doctor(project_root, checks=check_names)
    except ValueError as exc:
        if json_output:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            tui.error(str(exc))
        return 2
    # Attach applied fixes to the structured report so JSON consumers (both
    # --json and --json-out) see them without the report being polluted by
    # TUI text or the fixes list being dropped from the exported file.
    report.fixes = fixes
    code = render_report(report, json_output=json_output, strict=strict)

    if json_out:
        try:
            export_report_json(
                report, Path(json_out).resolve(), strict=strict
            )
            if not json_output:
                tui.hint(f"doctor: JSON report written to {json_out}")
        except OSError as exc:
            tui.error(f"doctor: failed to write JSON report to {json_out}: {exc}")
            return 1

    return code


def _config_usage_error(message: str, json_output: bool) -> None:
    """Emit a config-subcommand usage error honouring the ``--json`` contract.

    ``--json`` promises "stdout holds exactly one JSON document" (see the
    global ``--json`` help); a usage refusal must keep that promise so
    ``iterate config set k --json | jq`` never sees an empty body.
    """
    if json_output:
        print(json.dumps({"error": message}, ensure_ascii=False))
    tui.error(message)


def _cmd_config(
    project_root: Path,
    action: str | None,
    key: str | None,
    value: str | None,
    json_output: bool = False,
    out: str | None = None,
    compact: bool = False,
    force: bool = False,
) -> int:
    """Handle the 'config' subcommand — non-interactive config inspection/edit.

    ``iterate config`` prints every settable value, ``iterate config get [k]``
    prints one (or all) resolved value(s), ``iterate config set k v``
    validates and writes a single value with a timestamped backup, and
    ``iterate config unset k`` removes a value so it falls back to its
    documented default. With ``--json``, read/get/set/unset emit a structured
    JSON object on stdout (for scripts/CI) instead of TUI lines.

    ``iterate config schema`` emits the canonical JSON Schema for
    ``iterate.config.yaml`` (``--out``/``--compact``/``--force`` apply only to
    this action) so editors, CI validators and other tooling can enforce the
    same config contract the CLI itself enforces.

    Args:
        project_root: Project root directory.
        action: The config action ("get", "set", "unset", "schema", or None
            to list all).
        key: Flat config key to read or write (None to list all keys).
        value: Raw CLI value to write (only used with "set").
        json_output: When True, emit JSON objects instead of TUI output.
        out: Schema output path (schema action only; None = stdout).
        compact: Emit single-line schema JSON (schema action only).
        force: Overwrite an existing ``out`` file (schema action only).

    Returns:
        Exit code: 0 on success, 1 on unknown key / invalid value / write
        failure; 2 on usage errors (missing/extra positional arguments).
    """
    from iterate_cli.configcmd import (
        run_config_get,
        run_config_schema,
        run_config_set,
        run_config_unset,
    )

    # The implicit-get reinterpretation below happens before the schema branch,
    # so flags meant for schema must not be silently swallowed by get/set/unset.
    if action != "schema" and (out is not None or compact or force):
        _config_usage_error(
            "--out/--compact/--force are only valid with "
            "'iterate config schema'",
            json_output,
        )
        return 2

    # Implicit `get`: `iterate config KEY` ≡ `iterate config get KEY`. The
    # first positional is normally the action, so when it is not one of the
    # known verbs (and is therefore a config key like `language`), shift
    # it into `key` and treat the action as "get".
    if action is not None and action not in ("get", "set", "unset", "schema"):
        if key is not None:
            # `config sett key value` used to be read as an implicit get and
            # answered "get takes no VALUE" — a message about a verb the user
            # never typed. Name the likely intended verb instead.
            suggestion = _did_you_mean(action, ("get", "set", "unset", "schema"))
            if suggestion:
                message = (
                    f"unknown config action {action!r} — did you mean "
                    f"{suggestion!r}? Usage: iterate config set KEY VALUE "
                    "(or omit the action and pass just a KEY to read it)."
                )
            else:
                message = (
                    f"unknown config action {action!r}; expected "
                    "get/set/unset/schema. Usage: iterate config set KEY VALUE, "
                    "or `iterate config KEY` to read one value."
                )
            _config_usage_error(message, json_output)
            return 2
        key = action
        action = "get"

    if action == "schema":
        if key is not None or value is not None:
            _config_usage_error(
                "Usage: iterate config schema  (schema takes no KEY/VALUE)",
                json_output,
            )
            return 2
        return run_config_schema(out=out, compact=compact, force=force)

    if action == "set":
        # Usage errors must be exit 2 everywhere (bare `iterate`, `--json` on
        # an interactive command, `update --json` without `--yes` all use 2), so
        # automation can tell "you invoked it wrong" apart from "the operation
        # failed". These two were the only ones returning 1 for a bad call.
        if key is None or value is None:
            _config_usage_error(
                "Usage: iterate config set KEY VALUE", json_output
            )
            return 2
        return run_config_set(project_root, key, value, json_output=json_output)

    if action == "unset":
        # Missing KEY (nothing to unset) or a stray VALUE (`unset k v` would
        # otherwise silently ignore `v` and exit 0, exactly like `config get
        # k stray` used to) are both invocation errors → exit 2.
        if key is None or value is not None:
            _config_usage_error(
                "Usage: iterate config unset KEY  (unset takes no VALUE)",
                json_output,
            )
            return 2
        return run_config_unset(project_root, key, json_output=json_output)

    if action == "get" and value is not None:
        # `config get language stray` silently ignored the extra positional
        # (it landed in `value`, which get never reads) and exited 0 — a
        # mistyped command looked like a success to scripts. Refuse it.
        _config_usage_error(
            "Usage: iterate config get [KEY]  (get takes no VALUE)", json_output
        )
        return 2

    # 'get' (explicit or implicit) lists all values when no key is given.
    return run_config_get(project_root, key, json_output=json_output)


def _cmd_guard(
    project_root: Path,
    guard_action: str | None,
    targets: list[str] | None,
    json_output: bool = False,
    dry_run: bool = False,
) -> int:
    """Handle the 'guard' subcommand — defensive-programming pre/post-edit checks.

    Args:
        project_root: Project root directory.
        guard_action: Which guard to run (``pre-check`` / ``post-check``).
        targets: For pre-check, paths that must exist; for post-check, module
            names to filter the validation commands.
        json_output: When True, emit a structured JSON object instead of TUI.
        dry_run: When True, preview exact commands without executing anything.

    Returns:
        Exit code: 0 when all checks pass, 1 otherwise.
    """
    from iterate_cli.guard import (
        render_guard_result,
        run_guard_postcheck,
        run_guard_precheck,
    )

    if guard_action == "pre-check":
        result = run_guard_precheck(project_root, targets or [], dry_run=dry_run)
    else:
        result = run_guard_postcheck(project_root, targets or None, dry_run=dry_run)
    return render_guard_result(result, json_output=json_output)


def _cmd_invariant(
    project_root: Path,
    json_output: bool = False,
    dry_run: bool = False,
) -> int:
    """Handle the 'invariant' subcommand — project-level invariant check.

    Args:
        project_root: Project root directory.
        json_output: When True, emit a structured JSON object instead of TUI.
        dry_run: When True, preview exact commands without executing anything.

    Returns:
        Exit code: 0 when every invariant holds, 1 otherwise.
    """
    from iterate_cli.guard import render_guard_result, run_invariant_check

    result = run_invariant_check(project_root, dry_run=dry_run)
    return render_guard_result(result, json_output=json_output)


def _cmd_fingerprint_list(
    project_root: Path, config: dict[str, Any] | None, json_output: bool
) -> int:
    """Print the fingerprints recorded at the last onboarding/refresh.

    Pure read of ``onboarding.fingerprints`` — no rescan, so it is fast and
    works with ``drift_check: false``. Complements ``verify`` by showing the
    BASELINE being compared against (path + SHA-256), which ``verify`` alone
    never prints.

    Args:
        project_root: Project root directory.
        config: Already-loaded config, or None when unreadable.
        json_output: When True, emit a structured JSON object instead of TUI.

    Returns:
        Exit code: 0 on success / no config to read; 1 only when the config
        exists but is corrupt (fail closed).
    """
    if config is None:
        code = drift_unavailable_code(project_root, config)
        reason = drift_unavailable_reason(project_root, config)
        if code != DRIFT_REASON_CORRUPT:
            # No config (fresh/not-onboarded project), drift disabled, or no
            # fingerprints recorded yet: an EMPTY baseline is informational,
            # not a failure. `fingerprint verify` already exits 0 here and
            # SKILL.md documents list as exit 0 "even if empty"; returning 1
            # for a simply-missing config (while verify returned 0 for the very
            # same state) was an inconsistency CI scripts tripped over.
            if json_output:
                print(
                    json.dumps(
                        {
                            "project": str(project_root),
                            "available": False,
                            "reason": reason,
                            "fingerprints": [],
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                )
            else:
                tui.intro(f"Iterate Skill — Fingerprint List / {project_root.name}")
                tui.info(f"No fingerprints recorded yet ({reason}).", indent=2)
                tui.hint(
                    "Run 'iterate onboard' to initialize, or 'iterate refresh' "
                    "to capture them.",
                    indent=4,
                )
            return 0
        # A corrupt config is not "no fingerprints recorded", it is an unknown
        # state — fail closed, matching `verify`.
        if json_output:
            print(
                json.dumps(
                    {
                        "project": str(project_root),
                        "available": False,
                        "reason": reason,
                        "fingerprints": [],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            # Title uses tui.intro (stdout, ◆ prefix) like every other
            # fingerprint path; only the actual error line goes to stderr.
            # Printing the title via tui.error once put "✗ Iterate Skill —
            # Fingerprint List" on stderr with no matching stdout header.
            tui.intro(f"Iterate Skill — Fingerprint List / {project_root.name}")
            tui.error(f"Could not read iterate.config.yaml: {reason}")
        return 1

    stored = get_stored_fingerprints(config)
    ignore_patterns = get_drift_ignore(config)
    if json_output:
        # isinstance narrowing: a hand-edited scalar `onboarding:` section
        # (`onboarding: legacy-scalar`) is truthy, survived the `or {}`, and
        # crashed this branch with AttributeError — the --json contract then
        # broke too (stdout emitted no JSON at all, just a traceback).
        onboarding_section = config.get("onboarding")
        onboarding = onboarding_section if isinstance(onboarding_section, dict) else {}
        print(
            json.dumps(
                {
                    "project": str(project_root),
                    "available": True,
                    "count": len(stored),
                    "drift_check_enabled": bool(onboarding.get("drift_check", True)),
                    "ignore_patterns": ignore_patterns,
                    "fingerprints": [
                        {"path": e.get("path"), "sha256": e.get("sha256")}
                        for e in stored
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    tui.intro(f"Iterate Skill — Fingerprint List / {project_root.name}")
    if not stored:
        tui.info("No fingerprints recorded yet.", indent=2)
        tui.hint("Run 'iterate refresh' (or 'iterate onboard') to capture them.", indent=4)
        return 0
    for entry in sorted(stored, key=lambda e: str(e.get("path", ""))):
        tui.key_value(
            str(entry.get("path", "")), str(entry.get("sha256", "")), indent=2
        )
    tui.empty_line()
    tui.hint(
        f"{len(stored)} manifest(s) recorded."
        + (f" {len(ignore_patterns)} ignore pattern(s)." if ignore_patterns else ""),
        indent=2,
    )
    return 0


def _cmd_fingerprint(
    project_root: Path, json_output: bool = False, action: str = "verify"
) -> int:
    """Handle the 'fingerprint' subcommand — verify or list manifest drift.

    Compares the fingerprints stored in iterate.config.yaml against the
    current project root via ``check_onboarding_drift``. Drift is
    non-blocking (an iteration can always continue), so this command is an
    informational health check: it exits 0 when no drift is detected and 1
    when added/removed/changed manifests are found.

    ``action="list"`` instead prints exactly what was RECORDED at the last
    onboarding/refresh without rescanning, so an operator can see the
    baseline (path + SHA-256) that ``verify`` is comparing against.

    Args:
        project_root: Project root directory.
        json_output: When True, emit a structured JSON object instead of TUI.
        action: "verify" (default) or "list".

    Returns:
        Exit code: 0 on success / drift-checking unavailable; 1 when drift is
        detected (verify) or the recorded fingerprints are unreadable (list).
    """
    from iterate_cli.refresh import check_onboarding_drift, load_onboarding_config

    # Load the config once and reuse: passing it into check_onboarding_drift
    # (sentinel-aware) skips a second load, which used to emit a SECOND
    # identical parse-error report for a corrupt config.
    config = load_onboarding_config(project_root)

    if action == "list":
        return _cmd_fingerprint_list(project_root, config, json_output)

    drift = check_onboarding_drift(project_root, config)

    if json_output:
        if drift is None:
            # Distinguish the three reasons drift checking is unavailable
            # (mirroring doctor's drift check) so a JSON consumer can tell
            # "not onboarded" from "check disabled" from "no fingerprints yet".
            code = drift_unavailable_code(project_root, config)
            reason = _drift_unavailable_reason(project_root, config)
            print(
                json.dumps(
                    {
                        "project": str(project_root),
                        "available": False,
                        "reason": reason,
                        "drift": False,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            # A corrupt config must FAIL CLOSED (exit 1): fingerprint is a
            # verification gate, and the previous unconditional 0 let CI treat
            # "config unreadable, drift unknown" as a pass while `status`/
            # `show` exited 1 for the same state. Non-corrupt unavailability
            # (not onboarded / disabled / no fingerprints) stays informational
            # (exit 0) — drift is non-blocking there by design. Branch on the
            # stable CODE, not on substrings of the human message: rewording
            # the reason text used to be able to flip this CI exit code
            # silently, with no test failing.
            return 1 if code == DRIFT_REASON_CORRUPT else 0
        print(
            json.dumps(
                {
                    "project": str(project_root),
                    "available": True,
                    "drift": drift.has_drift,
                    "summary": drift.summary(),
                    # Sorted to match the TUI renderer (which sorts every list)
                    # and to be deterministic regardless of config/scan order.
                    "added": sorted(drift.added),
                    "removed": sorted(drift.removed),
                    "changed": sorted(drift.changed),
                    "unchanged": sorted(drift.unchanged),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1 if drift.has_drift else 0

    tui.intro(f"Iterate Skill — Fingerprint Verify / {project_root.name}")

    if drift is None:
        tui.info("Fingerprint verification unavailable.", indent=2)
        code = drift_unavailable_code(project_root, config)
        if code == DRIFT_REASON_CORRUPT:
            # A corrupt config cannot be fixed by onboarding or by enabling
            # drift_check; point at doctor instead of the generic hint, and
            # fail closed (exit 1) to match the JSON branch above.
            tui.hint("Run 'iterate doctor' to diagnose the config.", indent=4)
            return 1
        if code == DRIFT_REASON_DISABLED:
            tui.hint(
                "Enable drift_check in iterate.config.yaml to verify fingerprints.",
                indent=4,
            )
        elif code == DRIFT_REASON_NO_FINGERPRINTS:
            # drift_check is already ON — telling this user to "run onboard or
            # enable drift_check" was wrong on both counts; the only thing
            # missing is a captured baseline.
            tui.hint(
                "Run 'iterate refresh' to capture fingerprints, then verify.",
                indent=4,
            )
        else:  # not onboarded / unknown
            tui.hint(
                "Run 'iterate onboard' first, or enable drift_check in "
                "iterate.config.yaml.",
                indent=4,
            )
        return 0

    if drift.has_drift:
        tui.warning("Drift detected:", indent=2)
        if drift.added:
            tui.bullet(f"added: {', '.join(sorted(drift.added))}", indent=4)
        if drift.removed:
            tui.bullet(f"removed: {', '.join(sorted(drift.removed))}", indent=4)
        if drift.changed:
            tui.bullet(f"changed: {', '.join(sorted(drift.changed))}", indent=4)
        tui.empty_line()
        tui.hint(
            "Drift is non-blocking. Run 'iterate refresh' to resync the "
            "knowledge base when the tech stack changed.",
            indent=2,
        )
        return 1

    tui.success("No drift detected.", indent=2)
    if drift.unchanged:
        tui.hint(
            f"{len(drift.unchanged)} manifest(s) verified: "
            f"{', '.join(sorted(drift.unchanged))}.",
            indent=4,
        )
    return 0


# ---------------------------------------------------------------------------
# Helpers shared by subcommand handlers
# ---------------------------------------------------------------------------


def _drift_unavailable_reason(
    project_root: Path, config: dict[str, Any] | None
) -> str:
    """Back-compat alias for ``refresh.drift_unavailable_reason``.

    The implementation moved next to ``check_onboarding_drift`` so ``status``,
    ``show`` and ``fingerprint`` share one definition.
    """
    return drift_unavailable_reason(project_root, config)


def _stdin_is_interactive() -> bool:
    """Return True when stdin is a real terminal (not piped/redirected)."""
    try:
        return sys.stdin.isatty()
    except (AttributeError, ValueError):
        return False


def _confirm(
    question: str,
    input_func: Callable[[str], str] = input,
    default: bool = False,
) -> bool:
    """Ask a yes/no question using the TUI question prompt (default [y/N])."""
    hint = "[Y/n]" if default else "[y/N]"
    if question:
        tui.question(question)
    while True:
        raw = input_func(f"  └ {hint} ").strip().lower()
        if not raw:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        tui.warning("请输入 y 或 n / Please enter y or n.", indent=4)


def _maybe_print_update_hint() -> None:
    """Emit a one-line update hint (advisory, best-effort). Never raises."""
    # Deliberately swallowed: a hint must never break ``iterate --version``,
    # so an import failure, network error or unsuitable terminal is ignored.
    with contextlib.suppress(Exception):
        from iterate_cli.updater import maybe_print_update_hint

        maybe_print_update_hint()


# ---------------------------------------------------------------------------
# ``iterate update`` subcommand
# ---------------------------------------------------------------------------


def _report_update_outcome(
    outcome: Any,
    *,
    json_output: bool = False,
    title_prefix: str = "",
) -> int:
    """Report the outcome of ``iterate update`` in TUI or JSON format."""
    if json_output:
        print(json.dumps(outcome.to_dict(), ensure_ascii=False, indent=2))
        if outcome.assistants_unknown or outcome.unreachable:
            return 1
        if outcome.assistants_failed:
            return 1
        # A download/integrity failure on a confirmed update means the update
        # did NOT happen; it must exit non-zero so automation does not treat
        # the environment as updated. (unreachable covers "could not check",
        # download_error covers "release download/verify/extract failed".)
        if outcome.download_error:
            return 1
        if (
            not outcome.cancelled
            and not outcome.up_to_date
            and outcome.cli_result is not None
            and not outcome.cli_result.success
        ):
            return 1
        return 0

    if outcome.assistants_unknown:
        # List the real registry, not `assistants_updated`: run_update returns
        # *before* updating any assistant when a name is unknown, so
        # `assistants_updated` was always empty here and the user was sent to
        # `--help` instead of the very list they needed to fix their typo.
        import iterate_cli.updater as _updater_registry

        tui.error(
            f"{title_prefix}Unknown assistant name(s): "
            f"{', '.join(sorted(outcome.assistants_unknown))}. "
            "Valid assistants: "
            + ", ".join(sorted(_updater_registry.ASSISTANT_SKILL_DIRS))
            + "."
        )
        return 1
    if outcome.unreachable:
        tui.error(
            f"{title_prefix}Could not check for updates: {outcome.download_error}"
        )
        return 1
    if outcome.up_to_date:
        tui.success(
            f"{title_prefix}You are running the latest version ({outcome.current})."
        )
        return 0
    if outcome.check_only:
        # `--check` with a NEWER release available must say so: the previous
        # `check_only or up_to_date` branch printed "running the latest
        # version" for every --check run, because run_update(check_only=True)
        # returns early with up_to_date=False whenever an update exists.
        # Exit stays 0 (check is informational; --json mirrors the same
        # fields), but the message reflects reality.
        tui.info(
            f"{title_prefix}Update available: {outcome.current} → {outcome.latest}."
        )
        tui.hint(
            "Run `iterate update --yes` to apply.", indent=2
        )
        return 0
    if outcome.cancelled:
        tui.info(f"{title_prefix}Update available but not applied.")
        tui.hint(
            "Run `iterate update --yes` to apply, or `iterate update --check` "
            "to view the latest version.",
            indent=2,
        )
        return 0

    if outcome.cli_result is not None:
        if outcome.cli_result.success:
            tui.success(f"{title_prefix}CLI updated: {outcome.cli_result.message}")
        else:
            tui.warning(
                f"{title_prefix}CLI update failed: {outcome.cli_result.message}"
            )
    if outcome.assistants_not_installed:
        # A valid --assistants name that matched no installed skill dir used to
        # produce a silent empty run (exit 0, no output) — indistinguishable
        # from "updated everything". Tell the operator which names simply have
        # no directory here.
        names = ", ".join(outcome.assistants_not_installed)
        tui.warning(
            f"{title_prefix}Requested assistant(s) not installed here: {names}"
        )
        tui.hint(
            "Run `iterate onboard` first to create those skill dirs.",
            indent=2,
        )
    if outcome.assistants_updated:
        names = ", ".join(outcome.assistants_updated)
        tui.success(f"{title_prefix}Assistant skill dirs updated: {names}")
    if outcome.assistants_failed:
        for name, reason in outcome.assistants_failed:
            tui.warning(f"{title_prefix}Assistant {name} failed to update: {reason}")
    if outcome.download_error:
        tui.warning(f"{title_prefix}Download error: {outcome.download_error}")

    any_failure = (
        outcome.cli_result is not None and not outcome.cli_result.success
    ) or bool(outcome.assistants_failed) or bool(outcome.download_error)
    return 1 if any_failure else 0


def _cmd_backup(
    project_root: Path,
    *,
    action: str = "list",
    backup_file: str | None = None,
    yes: bool = False,
    dry_run: bool = False,
    json_output: bool = False,
    keep: int | None = None,
    older_than: str | None = None,
) -> int:
    """Handle ``iterate backup`` — list, restore or prune timestamped backups.

    ``list`` (the default) is a pure read: it enumerates every recognisable
    backup in the project root and always exits 0, even when there are none
    (an empty result is informational, matching ``fingerprint list``). A
    corrupt config is not a barrier because a backup listing does not need to
    parse the config at all.

    ``restore`` is a write: it backs up the current target (tag ``restore``)
    first, then writes the backup content to the original path. It requires
    ``--yes`` when stdin is not a terminal, and refuses anything that does not
    look like an iterate backup so an arbitrary path can never be clobbered.

    ``prune`` is a write that deletes old backups under a retention policy
    (``--keep`` newest per base and/or ``--older-than`` age). It never touches
    the live files a backup protects, and only deletes files that look like
    iterate backups. ``--dry-run`` previews without deleting.
    """
    from iterate_cli.backup import (
        BackupError,
        backups_json,
        list_backups,
        parse_backup_age,
        prune_backups,
        restore_backup,
    )

    if action == "list":
        try:
            entries = list_backups(project_root)
        except BackupError as exc:
            if json_output:
                print(
                    json.dumps(
                        {"ok": False, "error": str(exc)}, ensure_ascii=False
                    )
                )
            else:
                tui.error(str(exc))
            return 1
        if json_output:
            print(backups_json(project_root, entries))
            return 0
        tui.intro(f"Iterate Skill — Backups / {project_root.name}")
        if not entries:
            tui.info(
                "No iterate backups found in this project directory.", indent=2
            )
            tui.hint(
                "Backups appear when a write command runs (config set/unset, "
                "doctor --fix, refresh, personalize, onboard, import, "
                "reonboard).",
                indent=4,
            )
            return 0
        tui.hint(
            f"{len(entries)} backup(s), newest first. Restore one with "
            "'iterate backup restore <file>'.",
            indent=2,
        )
        for entry in entries:
            tui.key_value(
                entry.path.name,
                f"{entry.label} · {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}"
                f" · {entry.size} B → {entry.base}",
                indent=2,
            )
        return 0

    # action == "prune"
    if action == "prune":
        if keep is None and older_than is None:
            message = (
                "backup prune needs at least one of --keep or --older-than "
                "(e.g. `iterate backup prune --keep 5`)"
            )
            if json_output:
                print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
            else:
                tui.error(message)
            return 2
        # Validate the policy BEFORE touching any file. These are invalid
        # argument values, so they must exit 2 like every other usage error —
        # `prune_backups` raises the same BackupError for them as it does for a
        # failed unlink, and the old single catch reported the argument typo as
        # exit 1 ("runtime failure"), contradicting the documented contract and
        # making `--keep 0` indistinguishable from a partial prune.
        policy_error: str | None = None
        if keep is not None and keep < 1:
            policy_error = "--keep must be at least 1 (0 would delete every backup)"
        elif older_than is not None:
            try:
                parse_backup_age(older_than)
            except BackupError as exc:
                policy_error = str(exc)
        if policy_error is not None:
            if json_output:
                print(
                    json.dumps({"ok": False, "error": policy_error}, ensure_ascii=False)
                )
            else:
                tui.error(policy_error)
            return 2
        try:
            outcome = prune_backups(
                project_root,
                keep=keep,
                older_than=older_than,
                dry_run=dry_run,
            )
        except BackupError as exc:
            if json_output:
                print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
            else:
                tui.error(str(exc))
            return 1

        if json_output:
            print(json.dumps(outcome, ensure_ascii=False))
            return 0

        if dry_run:
            tui.intro("Iterate Skill — Backup prune preview")
            tui.key_value("Total backups", str(outcome["total"]))
            tui.key_value("Would delete", str(len(outcome["deleted"])))
            tui.key_value("Would keep", str(len(outcome["kept"])))
            tui.hint(
                "Dry run: nothing was deleted. Re-run without --dry-run to prune."
            )
            return 0

        tui.empty_line()
        if outcome["deleted"]:
            tui.success(
                f"Pruned {len(outcome['deleted'])} backup(s); "
                f"{len(outcome['kept'])} kept."
            )
            for entry in outcome["deleted"]:
                tui.hint(f"deleted {entry['name']}", indent=2)
        else:
            tui.info(
                "No backups matched the retention policy; nothing was deleted."
            )
        return 0

    # action == "restore"
    if not backup_file:
        message = "no backup file given; usage: iterate backup restore <file>"
        if json_output:
            print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
        else:
            tui.error(message)
        return 2

    if not yes and not dry_run:
        if json_output:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "--json implies a write, so it requires --yes "
                        "(like `iterate update --json`).",
                    },
                    ensure_ascii=False,
                )
            )
            return 2
        if not _stdin_is_interactive():
            tui.error(
                "Non-interactive stdin detected; pass --yes to restore this "
                "backup (or --dry-run to preview it)."
            )
            return 2
        if not _confirm(
            f"Restore {backup_file} to its original name? The current file is "
            "backed up first.",
            default=False,
        ):
            tui.info("已取消 / Cancelled; nothing was written.")
            return 1

    try:
        outcome = restore_backup(
            project_root, backup_file, dry_run=dry_run
        )
    except BackupError as exc:
        if json_output:
            print(
                json.dumps(
                    {"ok": False, "error": str(exc)}, ensure_ascii=False
                )
            )
        else:
            tui.error(str(exc))
        return 1

    if json_output:
        print(json.dumps(outcome, ensure_ascii=False))
        return 0

    if dry_run:
        tui.intro("Iterate Skill — Backup restore preview")
        tui.key_value("Backup", outcome["backup"])
        tui.key_value("Restores", outcome["target"])
        tui.hint("Dry run: nothing was written. Re-run without --dry-run to restore.")
        return 0

    tui.empty_line()
    tui.success(f"Restored {outcome['backup']} → {outcome['target']}.")
    if outcome["pre_restore_backup"]:
        tui.hint(
            f"The previous file was backed up as {outcome['pre_restore_backup']} "
            "(restore it the same way to undo).",
            indent=2,
        )
    tui.hint(
        "Verify the result with `iterate doctor` (add --fix to repair).",
        indent=2,
    )
    return 0


def _cmd_update(
    project_root: Path,
    *,
    check_only: bool = False,
    yes: bool = False,
    json_output: bool = False,
    assistants: list[str] | None = None,
) -> int:
    """Handle the 'update' subcommand — self-update the CLI and skill dirs."""
    import iterate_cli.updater as updater_mod

    # --json for a write operation requires --yes (non-interactive explicit consent).
    if json_output and not yes and not check_only:
        # stdout must hold one JSON document on every path (the global --json
        # contract); previously this refusal wrote only to stderr, leaving
        # `iterate update --json | jq` with an empty body and a bare exit 2.
        message = (
            "--json for `iterate update` requires --yes (a write operation "
            "must be explicitly confirmed). Use --check to read-only compare "
            "versions without --yes."
        )
        print(
            json.dumps(
                {"error": message, "hint": "pass --yes or --check"},
                ensure_ascii=False,
            )
        )
        tui.error(message)
        return 2

    if check_only:
        # Forward `assistants` here too: dropping it meant a mistyped name
        # (e.g. `--assistants cluade`) exited 0 on the read-only `--check`
        # while the very same typo is a hard error on the apply path, which
        # also made the `outcome.assistants_unknown` term below unreachable.
        outcome = updater_mod.run_update(
            project_root=project_root,
            check_only=True,
            assistants=assistants,
        )
        if json_output:
            print(json.dumps(outcome.to_dict(), ensure_ascii=False, indent=2))
            return 0 if not (outcome.unreachable or outcome.assistants_unknown) else 1
        tui.intro("Iterate Skill — Update Check")
        return _report_update_outcome(outcome, json_output=False, title_prefix="\n")

    confirmed = yes
    if not confirmed:
        if not _stdin_is_interactive():
            tui.hint(
                "Non-interactive stdin detected. Pass --yes to apply the update "
                "automatically, or --check to only compare versions."
            )
            return 1
        # Interactive path: check first, confirm, then apply.
        outcome = updater_mod.run_update(
            project_root=project_root,
            check_only=True,
            assistants=assistants,
        )
        if outcome.unreachable:
            tui.error(f"\nCould not check for updates: {outcome.download_error}")
            return 1
        if outcome.assistants_unknown:
            # Same reason as the `--check` branch: refuse the mistyped name
            # before prompting for confirmation, instead of asking the user to
            # confirm an update that is guaranteed to fail.
            return _report_update_outcome(outcome, json_output=False, title_prefix="\n")
        if outcome.up_to_date:
            tui.success(f"\nYou are running the latest version ({outcome.current}).")
            return 0
        version_line = f"{outcome.current} → {outcome.latest}"
        tui.info(f"\nUpdate available: {version_line}")
        if not _confirm("Apply this update now?", default=False):
            tui.cancel()
            tui.hint("Update cancelled. Nothing was changed.", indent=2)
            # Cancel → 1, per main()'s documented contract ("0 for success,
            # 1 for error/cancel") and matching `onboard`/`reonboard`: a
            # script must not read "the update was applied" from exit 0
            # just because the operator said no.
            return 1
        confirmed = True

    outcome = updater_mod.run_update(
        project_root=project_root,
        confirmed=confirmed,
        assistants=assistants,
    )
    return _report_update_outcome(outcome, json_output=json_output, title_prefix="\n")
