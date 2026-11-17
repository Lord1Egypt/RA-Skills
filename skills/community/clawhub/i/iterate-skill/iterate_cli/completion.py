"""Shell completion generation for the iterate CLI.

Before this module existed, users had to remember every subcommand and flag
(and every flag's position) — ``iterate --help`` was the only discovery path,
and pressing Tab completed filenames instead of commands. ``iterate completion
<shell>`` prints a ready-to-install completion script for bash, zsh or fish,
generated from the *same* argparse parser that powers ``--help`` so the two can
never disagree about which commands/options exist.

The generated scripts are dependency-free (no bash-completion / zsh plugin
needed) and complete:
- the command list at position 1 (with the parser's own one-line help),
- every option of the selected command (hidden options excluded),
- fixed value choices (for example ``init --language zh|en``),
- directories for ``-p/--project`` and files for path arguments,
- command names after ``iterate help``.
"""

from __future__ import annotations

import argparse
import os
import shlex
from pathlib import Path
from typing import Any

from iterate_cli.generator import atomic_write

#: Shells with a renderer, in the order shown by ``--help``.
SHELLS: tuple[str, ...] = ("bash", "zsh", "fish")

#: Filename each shell's loader expects in its completion directory.
INSTALL_FILENAMES: dict[str, str] = {
    "bash": "iterate",
    "zsh": "_iterate",
    "fish": "iterate.fish",
}

#: Option destinations that take a filesystem path.
_DIR_OPTION_DESTS: frozenset[str] = frozenset({"project"})
_FILE_OPTION_DESTS: frozenset[str] = frozenset({"out", "json_out", "bundle"})


def _subparsers(parser: argparse.ArgumentParser) -> Any | None:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action
    return None


def _one_line(text: str | None, limit: int = 96) -> str:
    """Collapse a parser description/help into one short, quote-safe line."""
    if not text:
        return ""
    line = " ".join(str(text).split())
    if len(line) > limit:
        cut = line[:limit].rsplit(" ", 1)[0].rstrip(",.;:")
        line = f"{cut}…"
    return line


def _command_help(subparser: argparse.ArgumentParser) -> str:
    """Return the one-line help registered via ``add_parser(help=...)``."""
    # argparse stores these on the subparsers action (`_choices_actions`);
    # description is the fallback for parsers built without `help=`.
    return _one_line(subparser.description)


def _command_entries(
    parser: argparse.ArgumentParser,
) -> list[tuple[str, str, argparse.ArgumentParser]]:
    """Return ``(name, short_help, parser)`` for every subcommand, in order."""
    action = _subparsers(parser)
    if action is None:
        return []
    helps: dict[str, str] = {}
    for choice_action in getattr(action, "_choices_actions", []):
        helps[getattr(choice_action, "dest", "")] = getattr(
            choice_action, "help", ""
        ) or ""
    entries = []
    for name, sub in action.choices.items():
        help_text = _one_line(helps.get(name)) or _command_help(sub)
        entries.append((name, help_text, sub))
    return entries


def _option_specs(
    subparser: argparse.ArgumentParser,
) -> list[dict[str, Any]]:
    """Describe a subcommand's visible options for the shell renderers."""
    specs: list[dict[str, Any]] = []
    for action in subparser._actions:
        if isinstance(
            action,
            (
                argparse._HelpAction,
                argparse._VersionAction,
                argparse._CountAction,
            ),
        ):
            continue
        if not action.option_strings:
            continue
        if action.help is argparse.SUPPRESS:
            continue
        takes_value = not isinstance(
            action, (argparse._StoreTrueAction, argparse._StoreFalseAction)
        )
        specs.append(
            {
                "options": list(action.option_strings),
                "dest": action.dest,
                "takes_value": takes_value,
                "choices": [str(c) for c in action.choices]
                if getattr(action, "choices", None)
                else [],
                "help": _one_line(action.help, 80),
            }
        )
    return specs


def _quote_single(text: str) -> str:
    """Quote text for a single-quoted shell string."""
    return text.replace("\\", "\\\\").replace("'", "'\\''")


def _bash_words(values: list[str]) -> str:
    return " ".join(values)


def _case_pattern(command: str, options: list[str]) -> str:
    """Build a shell ``case`` pattern matching ``cmd`` + any option.

    Every alternative repeats the ``cmd:`` prefix because bash has no plain
    ``(a|b)`` grouping (that needs extglob); repeating works identically in
    bash and zsh, e.g. ``init:--language|init:-l``.
    """
    return "|".join(f"{command}:{option}" for option in options)


def _render_bash(parser: argparse.ArgumentParser) -> str:
    commands = _command_entries(parser)
    names = [name for name, _, _ in commands]

    # Option words per command, plus fixed-choice value completion.
    option_cases: list[str] = []
    value_cases: list[str] = []
    for name, _, sub in commands:
        words: list[str] = []
        for spec in _option_specs(sub):
            words.extend(spec["options"])
            if spec["choices"]:
                value_cases.append(
                    f"        {_case_pattern(name, spec['options'])}) "
                    f"COMPREPLY=( $(compgen -W \"{_bash_words(spec['choices'])}\" "
                    f'-- "$cur") ); return 0 ;;'
                )
            if spec["dest"] in _DIR_OPTION_DESTS:
                value_cases.append(
                    f"        {_case_pattern(name, spec['options'])}) "
                    "_iterate_complete_dirs; return 0 ;;"
                )
            elif spec["dest"] in _FILE_OPTION_DESTS:
                value_cases.append(
                    f"        {_case_pattern(name, spec['options'])}) "
                    "_iterate_complete_files; return 0 ;;"
                )
        if words:
            option_cases.append(
                f"        {name}) opts=\"{_bash_words(words)}\" ;;"
            )

    lines = [
        "# bash completion for iterate",
        "# Install: `iterate completion bash --install` (or save as",
        "# ~/.local/share/bash-completion/completions/iterate).",
        "_iterate_complete_files() {",
        "    local IFS=$'\\n'",
        '    COMPREPLY=( $(compgen -f -- "$cur") )',
        "}",
        "",
        "_iterate_complete_dirs() {",
        "    local IFS=$'\\n'",
        '    COMPREPLY=( $(compgen -d -- "$cur") )',
        "}",
        "",
        "_iterate_completion() {",
        "    local cur prev cmd opts",
        '    cur="${COMP_WORDS[COMP_CWORD]}"',
        '    prev="${COMP_WORDS[COMP_CWORD-1]}"',
        f'    local commands="{" ".join(names)}"',
        '    local global_opts="-h --help -V -v --version --no-banner --json -p --project"',
        "",
        "    if [[ ${COMP_CWORD} -eq 1 ]]; then",
        '        if [[ "$cur" == -* ]]; then',
        '            COMPREPLY=( $(compgen -W "$global_opts" -- "$cur") )',
        "        else",
        '            COMPREPLY=( $(compgen -W "$commands $global_opts" -- "$cur") )',
        "        fi",
        "        return 0",
        "    fi",
        "",
        '    cmd="${COMP_WORDS[1]}"',
        '    opts=""',
        '    case "$cmd" in',
        *option_cases,
        "    esac",
        "",
        '    if [[ "$cur" == -* ]]; then',
        '        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )',
        "        return 0",
        "    fi",
        "",
        "    # Fixed value choices / path arguments follow the selected command.",
        '    case "$cmd:$prev" in',
        *value_cases,
        "    esac",
        "",
        '    if [[ "$cmd" == "help" ]]; then',
        '        COMPREPLY=( $(compgen -W "$commands" -- "$cur") )',
        "        return 0",
        "    fi",
        "    case \"$cmd\" in",
        "        import) _iterate_complete_files ;;",
        "    esac",
        "    return 0",
        "}",
        "",
        "complete -F _iterate_completion iterate",
        "",
    ]
    return "\n".join(lines)


def _zsh_escape_desc(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("'", "'\\''")
    )


def _render_zsh(parser: argparse.ArgumentParser) -> str:
    commands = _command_entries(parser)
    command_entries = []
    for name, help_text, _ in commands:
        if help_text:
            command_entries.append(
                f"        '{name}:{_zsh_escape_desc(help_text)}'"
            )
        else:
            command_entries.append(f"        '{name}'")

    option_cases: list[str] = []
    value_cases: list[str] = []
    for name, _, sub in commands:
        opts = []
        for spec in _option_specs(sub):
            for option in spec["options"]:
                if spec["help"]:
                    opts.append(
                        f"            '{option}[{_zsh_escape_desc(spec['help'])}]'"
                    )
                else:
                    opts.append(f"            '{option}'")
            if spec["choices"]:
                value_cases.append(
                    f"        {_case_pattern(name, spec['options'])}) "
                    f"_values 'value' {' '.join(spec['choices'])}; return ;;"
                )
            if spec["dest"] in _DIR_OPTION_DESTS:
                value_cases.append(
                    f"        {_case_pattern(name, spec['options'])}) "
                    "_directories; return ;;"
                )
            elif spec["dest"] in _FILE_OPTION_DESTS:
                value_cases.append(
                    f"        {_case_pattern(name, spec['options'])}) "
                    "_files; return ;;"
                )
        if opts:
            option_cases.extend(
                [f"        {name})", "            opts=(", *opts, "            )", "            ;;"]
            )

    lines = [
        "#compdef iterate",
        "# zsh completion for iterate",
        "# Install: `iterate completion zsh --install` (writes _iterate to",
        "# ~/.zfunc or ~/.oh-my-zsh/completions and prints the fpath hint).",
        "",
        "_iterate() {",
        "    local -a commands",
        "    commands=(",
        *command_entries,
        "    )",
        "",
        "    if (( CURRENT == 2 )); then",
        "        _describe -t commands 'iterate command' commands",
        "        return",
        "    fi",
        "",
        "    local cmd=${words[2]}",
        "    local -a opts",
        '    opts=()',
        '    case "$cmd" in',
        *option_cases,
        "    esac",
        "",
        '    if [[ ${words[CURRENT]} == -* ]]; then',
        "        _describe -t options 'option' opts",
        "        return",
        "    fi",
        "",
        "    # Value completion for options that take an argument.",
        '    case "$cmd:${words[CURRENT-1]}" in',
        *value_cases,
        "    esac",
        "",
        '    if [[ "$cmd" == "help" ]]; then',
        "        _describe -t commands 'iterate command' commands",
        "        return",
        "    fi",
        '    if [[ "$cmd" == "import" ]]; then',
        "        _files",
        "        return",
        "    fi",
        "}",
        "",
        'if [ "$funcstack[1]" = "_iterate" ]; then',
        '    _iterate "$@"',
        "else",
        "    compdef _iterate iterate",
        "fi",
        "",
    ]
    return "\n".join(lines)


def _render_fish(parser: argparse.ArgumentParser) -> str:
    commands = _command_entries(parser)
    names = [name for name, _, _ in commands]
    lines = [
        "# fish completion for iterate",
        "# Install: `iterate completion fish --install` (or redirect to",
        "# ~/.config/fish/completions/iterate.fish).",
        "",
        "# Subcommands (only at the first positional argument; -f suppresses",
        "# filename completion where a command name is expected).",
    ]
    for name, help_text, _ in commands:
        desc = _quote_single(help_text)
        lines.append(
            "complete -c iterate -f -n '__fish_use_subcommand' "
            f"-a {name} -d '{desc}'"
        )
    lines.extend(
        [
            "",
            "# `iterate help <command>` takes a command name.",
            (
                "complete -c iterate -f "
                "-n '__fish_seen_subcommand_from help' -a "
                f"'{' '.join(names)}'"
            ),
            "",
        ]
    )
    for name, _, sub in commands:
        lines.append(f"# {name}")
        condition = f"__fish_seen_subcommand_from {name}"
        for spec in _option_specs(sub):
            desc = _quote_single(spec["help"])
            for option in spec["options"]:
                if option.startswith("--"):
                    flag = f"-l {option[2:]}"
                elif option.startswith("-") and len(option) == 2:
                    flag = f"-s {option[1:]}"
                else:
                    continue
                parts = [f"complete -c iterate -n '{condition}'", flag]
                if desc:
                    parts.append(f"-d '{desc}'")
                if spec["takes_value"]:
                    parts.append("-r")
                    if spec["choices"]:
                        parts.append(f"-a '{' '.join(spec['choices'])}'")
                lines.append(" ".join(parts))
        lines.append("")
    return "\n".join(lines) + "\n"


def render_completion(shell: str, parser: argparse.ArgumentParser) -> str:
    """Render a completion script for ``shell``.

    Args:
        shell: One of :data:`SHELLS` (``bash`` / ``zsh`` / ``fish``).
        parser: The top-level argparse parser to introspect.

    Returns:
        The complete script, ending in a newline.

    Raises:
        ValueError: When ``shell`` is not supported. The CLI maps this to a
            usage error (exit 2) with the supported values.
    """
    if shell == "bash":
        return _render_bash(parser)
    if shell == "zsh":
        return _render_zsh(parser)
    if shell == "fish":
        return _render_fish(parser)
    raise ValueError(
        f"unsupported shell {shell!r}; choose one of: {', '.join(SHELLS)}"
    )


def install_hint(shell: str) -> str:
    """Return the one-line install instruction for ``shell``."""
    if shell == "bash":
        return (
            "Install: run `iterate completion bash --install` (or save the "
            "output to ~/.local/share/bash-completion/completions/iterate)."
        )
    if shell == "zsh":
        return (
            "Install: run `iterate completion zsh --install` (writes _iterate "
            "to ~/.zfunc or ~/.oh-my-zsh/completions, then prints the fpath hint)."
        )
    if shell == "fish":
        return (
            "Install: run `iterate completion fish --install` (or redirect to "
            "~/.config/fish/completions/iterate.fish)."
        )
    return ""


def default_install_path(shell: str, env: dict[str, str] | None = None) -> Path:
    """Return the conventional per-user completion file for ``shell``.

    bash and fish load these paths automatically when their standard
    completion support is enabled. zsh has no single auto-loaded user path, so
    prefer Oh My Zsh's completions directory when it exists and otherwise use
    the widely documented ``~/.zfunc``; :func:`reload_hint` tells the user how
    to put that directory on ``$fpath``.
    """
    if shell not in INSTALL_FILENAMES:
        raise ValueError(
            f"unsupported shell {shell!r}; choose one of: {', '.join(SHELLS)}"
        )
    values = os.environ if env is None else env
    home = Path(values.get("HOME") or Path.home())
    filename = INSTALL_FILENAMES[shell]
    if shell == "bash":
        data_home = Path(values.get("XDG_DATA_HOME") or home / ".local" / "share")
        return data_home / "bash-completion" / "completions" / filename
    if shell == "fish":
        config_home = Path(values.get("XDG_CONFIG_HOME") or home / ".config")
        return config_home / "fish" / "completions" / filename
    omz = home / ".oh-my-zsh" / "completions"
    if omz.is_dir():
        return omz / filename
    return home / ".zfunc" / filename


def reload_hint(shell: str, target: Path) -> str:
    """Return a shell-specific instruction for activating an installed file."""
    quoted = shlex.quote(str(target))
    if shell == "bash":
        return f"Open a new shell, or run: source {quoted}"
    if shell == "fish":
        return "Open a new fish shell; fish loads this file automatically."
    if target.parent.name == ".zfunc":
        parent = shlex.quote(str(target.parent))
        return (
            "Add `fpath=(" + parent + " $fpath)` before "
            "`compinit` in ~/.zshrc, then open a new shell."
        )
    return "Run `compinit` (or open a new shell) to load the completion."


def install_completion(
    shell: str,
    parser: argparse.ArgumentParser,
    *,
    directory: str | None = None,
    force: bool = False,
) -> dict[str, Any]:
    """Write the completion script to the shell's per-user completion path.

    Args:
        shell: ``bash`` / ``zsh`` / ``fish``.
        parser: Top-level parser used to render the script.
        directory: Optional directory override; the shell's conventional
            filename is still used inside it.
        force: Replace an existing file when true.

    Returns:
        A JSON-serialisable summary (``shell``, ``path``, ``bytes``,
        ``reload_hint``).

    Raises:
        ValueError: Unsupported shell.
        FileExistsError: The target exists and ``force`` is false.
        OSError: The directory cannot be created or the file cannot be written.
    """
    if shell not in INSTALL_FILENAMES:
        raise ValueError(
            f"unsupported shell {shell!r}; choose one of: {', '.join(SHELLS)}"
        )
    script = render_completion(shell, parser)
    if directory:
        target = Path(directory).expanduser() / INSTALL_FILENAMES[shell]
    else:
        target = default_install_path(shell)
    if target.exists() and not force:
        raise FileExistsError(
            f"{target} already exists; pass --force to replace it."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(target, script)
    return {
        "shell": shell,
        "path": str(target),
        "bytes": len(script.encode("utf-8")),
        "reload_hint": reload_hint(shell, target),
    }


def unload_hint(shell: str, target: Path) -> str:
    """Return a shell-specific instruction for deactivating a removed file."""
    if shell == "bash":
        return (
            "Open a new shell (or remove any manual `source` line you added); "
            "the completion is no longer loaded."
        )
    if shell == "fish":
        return "Open a new fish shell; the completion is no longer loaded."
    if target.parent.name == ".zfunc":
        parent = shlex.quote(str(target.parent))
        return (
            "Remove `fpath=(" + parent + " $fpath)` from ~/.zshrc, then "
            "open a new shell; the completion is no longer loaded."
        )
    return "Open a new shell; the completion is no longer loaded."


def uninstall_completion(
    shell: str,
    *,
    directory: str | None = None,
) -> dict[str, Any]:
    """Remove the completion script from the shell's per-user path.

    This is the inverse of :func:`install_completion`: it deletes exactly the
    file that install would have written (the shell's conventional per-user
    path, or ``directory`` when given), never an arbitrary path. It is
    idempotent — removing an already-absent file is a success, reported by
    ``removed=False`` — so ``iterate completion bash --uninstall`` is safe to
    re-run, and safe to run before ever installing.

    Args:
        shell: ``bash`` / ``zsh`` / ``fish``.
        directory: Optional directory override; the shell's conventional
            filename is still used inside it.

    Returns:
        A JSON-serialisable summary (``shell``, ``path``, ``removed``,
        ``reload_hint``).

    Raises:
        ValueError: Unsupported shell.
        OSError: The file cannot be removed.
    """
    if shell not in INSTALL_FILENAMES:
        raise ValueError(
            f"unsupported shell {shell!r}; choose one of: {', '.join(SHELLS)}"
        )
    if directory:
        target = Path(directory).expanduser() / INSTALL_FILENAMES[shell]
    else:
        target = default_install_path(shell)
    existed = target.exists()
    if existed:
        try:
            target.unlink()
        except OSError as exc:
            raise OSError(f"cannot remove completion file {target}: {exc}") from exc
    return {
        "shell": shell,
        "path": str(target),
        "removed": existed,
        "reload_hint": unload_hint(shell, target),
    }


def validate_script_syntax(shell: str, script: str) -> str | None:
    """Best-effort syntax check used by tests; returns an error or ``None``.

    Kept in the module (rather than the test) so both the test suite and a
    future ``iterate completion --check`` path can share the exact same
    command. Missing shells are reported as ``None`` (nothing to check).
    """
    import shutil
    import subprocess

    binary = shutil.which(shell)
    if binary is None:
        return None
    # bash, zsh and fish all accept `-n` to syntax-check a script without
    # executing it (the completion script is shell-agnostic enough that the
    # same check works for every supported shell).
    cmd = [binary, "-n"]
    try:
        result = subprocess.run(
            cmd,
            input=script,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover
        return str(exc)
    if result.returncode != 0:
        return (result.stderr or result.stdout).strip()
    return None
