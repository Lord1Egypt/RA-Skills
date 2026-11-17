"""Defensive-programming guards and invariants (``iterate guard`` / ``iterate invariant``).

v3.0 defensive-programming mode ships three deterministic checks that a host
assistant can run around every coding step, so that "defensive" is enforced by
the CLI rather than by prompt discipline alone:

- ``iterate guard pre-check [paths...]`` — run BEFORE touching anything: verify
  the target paths exist, the git worktree is clean enough to start, required
  dependency manifests are present, and the configured validation commands are
  still metachar-safe. Exit code 0 = clear to proceed; 1 = do not start.
- ``iterate guard post-check [module...]`` — run AFTER an edit: execute exactly
  the configured ``validation.commands.<module>`` commands (the runtime
  authoritative whitelist) against the changed modules. Exit code 0 = the edit
  is safe; 1 = the edit must be reverted before continuing.
- ``iterate invariant`` — run BEFORE delivering: evaluate the project-level
  invariants declared under ``config.invariants`` (per-module command lists plus
  ``ensure`` file assertions). Exit code 0 = all invariants hold; 1 = at least
  one invariant is violated.

Safety rules carried over from the iterate security baseline:
- Commands are only ever executed when they EXACTLY match a configured
  ``validation.commands`` / ``invariants.commands`` entry (after trim). No
  command is ever composed, prefixed, or parameterised here.
- Fail-closed metachar enforcement: a command containing shell-chaining
  metacharacters (or empty after trim) is REFUSED at execution time — and
  flagged by ``pre-check`` / ``--dry-run`` — so a hand-edited or drift-polluted
  config can never chain extra shell through ``subprocess.run(..., shell=True)``.
- ``--dry-run`` prints the exact commands that WOULD run without executing them
  (fail-fast: unsafe commands are reported as failures, not run).
"""

from __future__ import annotations

import codecs
import os
import select
import shutil
import signal
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from iterate_cli.personalize import (
    FORBIDDEN_COMMAND_CHARS,
    CorruptConfigError,
    _is_known_safe_command,
    load_config_strict,
)
from iterate_cli.refresh import CONFIG_YAML
from iterate_cli.tui import tui

#: Exit code used when a guard/invariant check fails.
EXIT_FAIL = 1
#: Exit code used when everything passes.
EXIT_PASS = 0

#: Maximum output lines retained in memory per executed command. The guard only
#: needs a diagnostic tail, so a chatty build/test command cannot exhaust the
#: host's memory; only the last ``_OUTPUT_LINE_CAP`` lines are ever kept.
_OUTPUT_LINE_CAP = 200
#: Hard byte ceiling on streamed command output. Once the cumulative output
#: exceeds this cap the buffer stops growing (the pipe is still drained, so the
#: child never blocks on a full pipe).
_OUTPUT_BYTE_CAP = 1024 * 1024
#: Seconds to wait for the output-reader thread after the direct child exits.
#: Exposed as a module constant so tests can shorten it; production keeps a
#: generous value for a slow filesystem flush.
_DRAIN_JOIN_SECONDS = 5

#: Seconds to wait for the reader to stop after ``stop_drain`` is set (the
#: fallback path used when a descendant still holds the pipe open).
_DRAIN_UNBLOCK_SECONDS = 1

#: How long the reader parks in ``select`` between checks of the stop/child
#: flags. Small enough that shutdown is prompt, large enough to stay cheap.
_DRAIN_POLL_SECONDS = 0.05

#: After the direct child exits, keep consuming until the pipe has been quiet
#: for this long. A descendant can inherit stdout and keep the pipe open with
#: no further output; closing the descriptor the moment the child exits would
#: race the reader and lose bytes the child had already flushed. This grace
#: window lets those bytes land before the reader stops on its own.
_DRAIN_QUIET_SECONDS = 0.2

#: Bytes read per stream chunk while draining command output, via ``os.read``
#: after ``select`` reports the pipe readable. This is deliberately not
#: ``TextIOWrapper.read(n)``: that call blocks until it has accumulated ``n``
#: characters or the stream ends, so a command that writes a short line and
#: then leaves a descendant holding stdout open would have its output trapped
#: inside the wrapper. Chunked reads still keep memory bounded for a single
#: gigantic newline-free line.
_DRAIN_CHUNK_BYTES = 64 * 1024
#: Per-command timeout in seconds. A wedged validation/build command must not
#: block the host agent forever; on expiry the whole process group is killed.
_COMMAND_TIMEOUT_SECONDS = 600

#: Shell-chaining metacharacters that must never appear in an executable
#: command string. Same canonical set as personalize.FORBIDDEN_COMMAND_CHARS /
#: doctor.COMMAND_METACHARS / scripts/validate.py (kept in sync by
#: tests/test_validate.py). Enforced fail-closed at execution time so a
#: hand-edited or drift-polluted config can never smuggle chained commands into
#: ``subprocess.run(..., shell=True)``.
COMMAND_METACHARS: frozenset[str] = frozenset(FORBIDDEN_COMMAND_CHARS)

#: Commands that execute under ``shell=True`` via a shell builtin, so no
#: external binary needs to exist on PATH. ``shutil.which`` cannot resolve
#: these, and the pre-check must not report a tool as missing for them.
SHELL_BUILTINS: frozenset[str] = frozenset(
    {
        ":",
        ".",
        "[",
        "alias",
        "bg",
        "bind",
        "break",
        "builtin",
        "caller",
        "cd",
        "command",
        "compgen",
        "complete",
        "continue",
        "declare",
        "dirs",
        "disown",
        "echo",
        "enable",
        "eval",
        "exec",
        "exit",
        "export",
        "false",
        "fc",
        "fg",
        "getopts",
        "hash",
        "help",
        "history",
        "jobs",
        "kill",
        "let",
        "local",
        "logout",
        "popd",
        "printf",
        "pushd",
        "pwd",
        "read",
        "readonly",
        "return",
        "set",
        "shift",
        "shopt",
        "source",
        "suspend",
        "test",
        "times",
        "trap",
        "true",
        "type",
        "typeset",
        "ulimit",
        "umask",
        "unalias",
        "unset",
        "wait",
    }
)


def _command_is_safe(command: str) -> bool:
    """True when ``command`` may be executed: non-empty, metachar-free, and
    starting with a known-safe tool prefix.

    Empty/whitespace-only commands are rejected too, so a stray blank entry
    cannot yield a false "exit 0 = validated" green light. The known-safe
    prefix re-check mirrors the persist-time validator
    (``personalize._is_known_safe_command``), so a hand-edited or
    drift-polluted config that bypasses the wizard cannot smuggle
    metachar-free but arbitrary executables (``rm -rf .``, ``curl ...``) into
    ``subprocess.run(..., shell=True)``.
    """
    if not command.strip() or any(ch in COMMAND_METACHARS for ch in command):
        return False
    return _is_known_safe_command(command)

#: Dependency manifests that indicate "this module's toolchain is ready".
_KNOWN_MANIFESTS: dict[str, tuple[str, ...]] = {
    "python": ("pyproject.toml", "setup.py", "requirements.txt", "Pipfile", "poetry.lock"),
    "typescript": ("package.json", "tsconfig.json", "yarn.lock", "pnpm-lock.yaml", "package-lock.json"),
    "swift": ("Package.swift",),
    "rust": ("Cargo.toml",),
    "go": ("go.mod",),
}


@dataclass
class GuardResult:
    """Aggregated result of a guard/invariant check.

    Attributes:
        name: Short label for the check (e.g. ``guard-pre`` / ``guard-post``).
        passed: True when every item passed; False otherwise.
        items: Per-item outcomes (label, ok, detail).
        dry_run: True when commands were only previewed, not executed.
    """

    name: str
    passed: bool = True
    items: list[tuple[str, bool, str]] = field(default_factory=list)
    dry_run: bool = False


def _load_project_config(project_root: Path) -> dict[str, Any]:
    """Load the project config, raising a clean error when it is unreadable.

    Returns an empty dict when the config file is absent (fresh project) so the
    guards degrade gracefully instead of crashing on a missing file.

    Args:
        project_root: Project root directory.

    Returns:
        Parsed config mapping (``{}`` when the file is missing).

    Raises:
        CorruptConfigError: When the file exists but is not valid YAML.
        OSError: When the file cannot be read.
    """
    return load_config_strict(project_root / CONFIG_YAML)


def _git_root(project_root: Path) -> Path | None:
    """Resolve the repository root containing ``project_root``, or None.

    Uses ``git rev-parse --show-toplevel`` and caches nothing; a repo-less
    project yields None and the git check is reported as skipped.
    """
    if not shutil.which("git"):
        return None
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            errors="replace",
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    root = proc.stdout.strip()
    return Path(root) if root else None


def _git_worktree_is_clean(git_root: Path) -> tuple[bool, str]:
    """Report whether the worktree has uncommitted tracked changes.

    Untracked files do NOT fail the check (they are common mid-task); only
    modified/deleted tracked files are treated as "dirty" so a defensive start
    can tell the host assistant the starting point is not clean.

    Returns:
        (clean, detail) where detail is a short summary of dirty entries.
    """
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(git_root),
            capture_output=True,
            text=True,
            errors="replace",
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False, "git status failed"
    if proc.returncode != 0:
        return False, "git status failed"
    dirty = [line for line in proc.stdout.splitlines() if line and not line.startswith("??")]
    if not dirty:
        return True, "worktree clean"
    return False, f"{len(dirty)} tracked change(s) (e.g. {dirty[0][:60]})"


def _manifest_ready(project_root: Path, module: str) -> tuple[bool, str]:
    """Check whether a module's dependency manifest(s) exist in the project."""
    manifests = _KNOWN_MANIFESTS.get(module)
    if not manifests:
        return True, f"no manifest defined for module '{module}'"
    found = [name for name in manifests if (project_root / name).is_file()]
    if found:
        return True, "found " + ", ".join(found)
    return False, "none of " + ", ".join(manifests) + " found"


def _validation_commands(config: dict[str, Any]) -> dict[str, list[str]]:
    """Return the runtime-authoritative validation commands mapping.

    Tolerates a hand-edited config where ``validation.commands`` is missing,
    not a mapping, or where a module value is not a list: non-list values are
    skipped (never iterated character-by-character) and empty/whitespace-only
    command strings are dropped. Every remaining command degrades to "no
    commands configured" when the section is unusable.
    """
    validation = config.get("validation")
    if not isinstance(validation, dict):
        return {}
    commands = validation.get("commands")
    if not isinstance(commands, dict):
        return {}
    result: dict[str, list[str]] = {}
    for mod, cmds in commands.items():
        if not isinstance(cmds, list):
            continue
        cleaned = [str(c) for c in cmds if isinstance(c, str) and c.strip()]
        if cleaned:
            result[str(mod)] = cleaned
    return result


def _invariant_commands(config: dict[str, Any]) -> dict[str, list[str]]:
    """Return the ``invariants.commands`` mapping (v3.0 defensive mode).

    Absent/malformed ``invariants`` section yields an empty dict, which makes
    ``iterate invariant`` degrade to the configured ``validation.commands``
    (see ``_validation_commands``) so old configs stay valid. Non-list module
    values and empty command strings are skipped (same rules as above).
    """
    invariants = config.get("invariants")
    if not isinstance(invariants, dict):
        return {}
    commands = invariants.get("commands")
    if not isinstance(commands, dict):
        return {}
    result: dict[str, list[str]] = {}
    for mod, cmds in commands.items():
        if not isinstance(cmds, list):
            continue
        cleaned = [str(c) for c in cmds if isinstance(c, str) and c.strip()]
        if cleaned:
            result[str(mod)] = cleaned
    return result


def _invariant_ensure(config: dict[str, Any]) -> list[str]:
    """Return the ``invariants.ensure`` file-assertion list (v3.0 defensive mode)."""
    invariants = config.get("invariants")
    if not isinstance(invariants, dict):
        return []
    ensure = invariants.get("ensure")
    if not isinstance(ensure, list):
        return []
    return [str(entry) for entry in ensure if isinstance(entry, str)]


def _kill_process_tree(proc: subprocess.Popen[Any]) -> None:
    """Best-effort SIGKILL of ``proc`` and its whole process group.

    Commands execute under ``shell=True`` with ``start_new_session=True``, so
    ``proc.pid`` is the session/process-group leader. Killing the group covers
    the shell AND any child processes it spawned (a bare ``proc.kill()`` would
    orphan the children, leaving a runaway build). Failures are ignored: the
    caller always reports a timeout either way.
    """
    try:
        if os.name == "posix":
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            return
        # Windows: no os.killpg/signal.SIGKILL and start_new_session is a
        # no-op there, so the process group is not isolated; kill the leader.
        proc.kill()
        return
    except ProcessLookupError:
        # The group (or its leader) is already gone — the command exited
        # between the timeout firing and this call. NOTHING is left to kill,
        # so falling through to proc.kill() would only raise again.
        return
    except (AttributeError, OSError):
        # AttributeError: interpreter/platform without os.getpgid (Windows
        #   Pythons reached via a monkeypatched posix path). OSError (e.g.
        #   PermissionError): killpg refused — try the leader directly as a
        #   last resort so the command we own still stops.
        pass
    try:
        proc.kill()
    except (ProcessLookupError, OSError):
        # The leader exited while we were falling back. This is the normal
        # outcome of a command that finished just as the timeout hit — letting
        # ProcessLookupError escape here turned a benign race in the timeout
        # path into an unhandled traceback out of `iterate guard`.
        pass


def _run_command(command: str, project_root: Path) -> tuple[int, str]:
    """Run one exact command under the project root.

    Never composes or prefixes commands: the caller guarantees ``command`` is an
    exact match from the configured validation/invariant lists. Fail-closed: a
    command containing shell-chaining metacharacters (or empty after trim) is
    refused without being executed, so a hand-edited or drift-polluted config
    can never execute chained shell.

    Defense-in-depth note (documented tradeoff): the metacharacter gate rejects
    ``; | & $ ` < > ( )`` and backslashes, so command substitution, piping,
    redirection and chaining are impossible — but the gate is *tool-name based*
    (see ``_is_known_safe_command``), so a metachar-free command whose first
    token is an allowlisted recipe-driven tool (``make``, ``cmake --build``,
    ``npm run``, ``gradle``, …) still runs whatever recipe the project's own
    Makefile/package.json declares. That is the intended purpose of a project
    validation command; it is not injection. It does mean a project's
    ``iterate.config.yaml`` (and its build scripts) is a **code-execution
    vector on that checkout**: only run ``guard``/``doctor``/``invariant`` on a
    tree whose config and build scripts you have reviewed, and never on an
    untrusted PR checkout without review.

    Output is drained through a bounded line buffer (last ``_OUTPUT_LINE_CAP``
    lines / ``_OUTPUT_BYTE_CAP`` bytes), so a chatty build or test command
    cannot drive the host process into unbounded memory growth; only a
    diagnostic tail is ever returned. Stdout and stderr are merged so a failing
    command's error text lands in the same contiguous tail.

    Args:
        command: Exact command string to execute.
        project_root: Working directory for the process.

    Returns:
        (returncode, output-tail) where output-tail is a bounded snippet of
        stdout/stderr (for diagnostics).
    """
    if not _command_is_safe(command):
        return EXIT_FAIL, f"refused: unsafe command {command!r} (shell metacharacter or empty)"

    lines: list[str] = []
    lines_lock = threading.Lock()
    try:
        proc = subprocess.Popen(
            command,
            cwd=str(project_root),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return EXIT_FAIL, f"could not execute: {exc}"

    child_done = threading.Event()
    stop_drain = threading.Event()

    def _drain() -> None:
        assert proc.stdout is not None
        fd = proc.stdout.fileno()
        # Chunked (not readline) draining: a tool that emits one gigantic
        # newline-free line (progress deltas, minified output) would otherwise
        # materialize the whole line in memory and silently bypass the byte
        # cap. Retention is TAIL-first: only the last _OUTPUT_LINE_CAP lines,
        # the last _OUTPUT_BYTE_CAP bytes of completed lines, and the tail of
        # a still-open line (carry) are kept — the fatal error a build prints
        # right before dying lives at the END of the output, so overflowing
        # the cap must discard the oldest content, never the newest.
        carry = ""
        retained = 0  # chars currently held in `lines` (approximate bytes)
        #: An incremental decoder, because a chunk boundary can split a multi-byte
        #: character; decoding each chunk on its own would turn it into U+FFFD and the
        #: wrapper's ``errors="replace"`` would not be there to stop it.
        decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

        def _trim_lines() -> None:
            nonlocal retained
            while lines and (
                len(lines) > _OUTPUT_LINE_CAP or retained > _OUTPUT_BYTE_CAP
            ):
                retained -= len(lines.pop(0)) + 1

        def _consume(raw: bytes) -> None:
            """Decode one chunk and fold it into the bounded line tail."""
            nonlocal carry, retained
            chunk = decoder.decode(raw, final=not raw)
            if not chunk:
                return
            carry += chunk
            if "\n" in carry:
                complete, _, carry = carry.rpartition("\n")
                new_lines = complete.split("\n")
                with lines_lock:
                    lines.extend(new_lines)
                    retained += sum(len(line) + 1 for line in new_lines)
                    _trim_lines()
            # Keep only the tail of a still-open line (half-line before the
            # next newline arrives) so a newline-free flood stays bounded.
            if len(carry) > _OUTPUT_BYTE_CAP:
                carry = carry[-_OUTPUT_BYTE_CAP:]

        quiet_deadline: float | None = None
        # `select` on a pipe fd is POSIX-only; on Windows it raises. Detect
        # that once and fall back to sleep-based polling so the bounded output
        # capture works everywhere instead of degrading to an EMPTY tail.
        select_works = True
        try:
            os.set_blocking(fd, False)
        except (OSError, ValueError):
            pass
        while True:
            if stop_drain.is_set():
                # The caller is shutting us down (the direct child exited but
                # a descendant still holds the pipe, or the join timed out).
                # Sweep whatever is already in the pipe before leaving, so
                # bytes the child flushed just before exiting are never lost.
                # Bounded: a descendant that keeps writing cannot pin us here,
                # and we stop at the first EAGAIN rather than waiting.
                for _ in range(64):
                    try:
                        raw = os.read(fd, _DRAIN_CHUNK_BYTES)
                    except (BlockingIOError, OSError, ValueError):
                        break
                    if not raw:
                        _consume(b"")
                        break
                    _consume(raw)
                break
            if child_done.is_set() and quiet_deadline is None:
                quiet_deadline = time.monotonic() + _DRAIN_QUIET_SECONDS
            readable = False
            if select_works:
                try:
                    readable, _, _ = select.select(
                        [fd], [], [], _DRAIN_POLL_SECONDS
                    )
                except (OSError, ValueError):
                    select_works = False
            if not readable and not select_works:
                # Windows/no-select fallback: wait briefly then attempt a
                # non-blocking read. EAGAIN just means "not yet"; keep polling
                # until the quiet deadline or shutdown.
                time.sleep(_DRAIN_POLL_SECONDS)
                try:
                    raw = os.read(fd, _DRAIN_CHUNK_BYTES)
                except BlockingIOError:
                    if (
                        quiet_deadline is not None
                        and time.monotonic() >= quiet_deadline
                    ):
                        break
                    continue
                except (OSError, ValueError):
                    break
                if not raw:
                    _consume(b"")
                    break
                _consume(raw)
                if child_done.is_set():
                    quiet_deadline = time.monotonic() + _DRAIN_QUIET_SECONDS
                continue
            if readable:
                try:
                    raw = os.read(fd, _DRAIN_CHUNK_BYTES)
                except (OSError, ValueError):
                    break
                if not raw:
                    _consume(b"")
                    break
                _consume(raw)
                if child_done.is_set():
                    quiet_deadline = time.monotonic() + _DRAIN_QUIET_SECONDS
            elif quiet_deadline is not None and time.monotonic() >= quiet_deadline:
                # The direct child is gone and the pipe has been quiet long
                # enough that a flush would have arrived. A descendant may
                # still hold the descriptor, but every byte written before the
                # child exited has been consumed, so stop without closing the
                # read end (closing first is what used to drop that tail).
                break
        if carry:
            with lines_lock:
                lines.append(carry)
                retained += len(carry)
                _trim_lines()

    thread = threading.Thread(target=_drain, daemon=True)
    thread.start()

    def _finish_drain() -> bool:
        """Join the reader, telling it to stop if a descendant holds the pipe.

        Returns True when the reader exited. ``proc.wait()`` only proves the
        direct child exited; a grandchild that inherited stdout keeps the pipe
        open, so the reader will not see EOF. Rather than closing the read end
        (which races the reader and can drop bytes the child already flushed),
        signal the reader to stop; it performs a final non-blocking sweep of
        the pipe and exits bounded.
        """
        child_done.set()
        thread.join(timeout=_DRAIN_JOIN_SECONDS)
        if thread.is_alive():
            stop_drain.set()
            thread.join(timeout=_DRAIN_UNBLOCK_SECONDS)
        if not thread.is_alive() and proc.stdout is not None:
            # The reader is gone; close our end so the descriptor is not
            # leaked. Safe now: all pending bytes were swept above.
            try:
                proc.stdout.close()
            except (OSError, ValueError):
                pass
        return not thread.is_alive()

    try:
        returncode = proc.wait(timeout=_COMMAND_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        _kill_process_tree(proc)
        try:
            # Bounded wait even after the kill: if both killpg and the
            # proc.kill() fallback failed (EPERM / race), an unbounded
            # wait() here would hang `iterate guard` forever.
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            pass
        _finish_drain()
        return EXIT_FAIL, f"command timed out after {_COMMAND_TIMEOUT_SECONDS}s"
    drain_finished = _finish_drain()
    # Per-line truncation BEFORE joining: a single megabyte-wide noise line
    # would otherwise consume the whole 400-char budget on its own and push
    # the (short) fatal error line out of the tail entirely — the exact
    # "kept the noise, lost the error" failure the tail-first retention
    # above exists to prevent.
    with lines_lock:
        snapshot = list(lines[-3:])
    tail = " | ".join(line.rstrip("\n")[:160] for line in snapshot)
    if not drain_finished:
        note = "output reader did not exit: a child may still hold stdout"
        tail = f"{tail} | {note}" if tail else note
    return returncode, tail[:400]


def _command_entries(commands_by_module: dict[str, list[str]], modules: list[str] | None) -> list[tuple[str, str]]:
    """Flatten (module, command) entries, optionally filtered by module names."""
    entries: list[tuple[str, str]] = []
    for module, cmds in commands_by_module.items():
        if modules and module not in modules:
            continue
        for cmd in cmds:
            entries.append((module, cmd))
    return entries


def run_guard_precheck(project_root: Path, paths: list[str], dry_run: bool = False) -> GuardResult:
    """Run the pre-edit guard: targets exist, git clean, manifests ready, commands safe.

    Args:
        project_root: Project root directory.
        paths: Target paths (files/dirs) that must exist before editing.
        dry_run: When True, preview commands without executing anything.

    Returns:
        A GuardResult with one item per check.
    """
    result = GuardResult(name="guard-pre", dry_run=dry_run)
    result.passed = True

    # 1. Target paths exist.
    # Keep (target, resolved) *pairs* end-to-end: filtering a bare list of
    # resolved paths would silently misalign it against ``paths`` in the
    # existence check below, reporting one filename for another's verdict.
    project_root_resolved = project_root.resolve()
    target_pairs: list[tuple[str, Path]] = [
        (p, (Path(p) if Path(p).is_absolute() else project_root / p).resolve()) for p in paths
    ]
    # Refuse targets that escape the project root, even when the user passed an
    # absolute path: ``run_guard_precheck`` guards edits inside the project, so
    # an out-of-tree target is a misconfiguration, not a legitimate one.
    in_root_pairs: list[tuple[str, Path]] = []
    for target, resolved in target_pairs:
        if resolved.is_relative_to(project_root_resolved):
            in_root_pairs.append((target, resolved))
        else:
            result.items.append(
                (
                    "targets within project root",
                    False,
                    f"outside project root: {target!r} resolves to {str(resolved)!r}",
                )
            )
            result.passed = False
    missing = [target for target, resolved in in_root_pairs if not resolved.exists()]
    if missing:
        result.items.append(("targets exist", False, "missing: " + ", ".join(missing)))
        result.passed = False
    elif len(in_root_pairs) == len(paths):
        result.items.append(("targets exist", True, f"{len(paths)} path(s) present"))

    # 2. Git worktree clean (only when inside a git repo).
    git_root = _git_root(project_root)
    if git_root is None:
        result.items.append(("git clean", True, "no git repo — skipped"))
    else:
        clean, detail = _git_worktree_is_clean(git_root)
        result.items.append(("git clean", clean, detail))
        if not clean:
            result.passed = False

    # 3. Dependency manifests ready.
    try:
        config = _load_project_config(project_root)
    except (CorruptConfigError, OSError, UnicodeDecodeError) as exc:
        result.items.append(("config readable", False, str(exc)))
        result.passed = False
        return result

    validation = _validation_commands(config)
    modules = list(validation.keys())
    if not modules:
        result.items.append(
            ("manifests ready", True, "no validation modules configured — skipped")
        )
    else:
        ready = []
        any_missing = False
        for module in modules:
            ok, detail = _manifest_ready(project_root, module)
            if not ok:
                # Report every missing manifest, not just the first: a host AI
                # that lists multiple modules must see each failure instead of
                # a silently truncated report.
                any_missing = True
                result.items.append((f"manifest[{module}]", False, detail))
                result.passed = False
                continue
            ready.append(detail)
        if not any_missing:
            result.items.append(
                ("manifests ready", True, "; ".join(ready) or "no manifests defined")
            )

    # 4. Validation commands are configured AND safe (metachar-free), so the
    #    promised "post-check will only run safe commands" actually holds.
    entries = _command_entries(validation, None)
    if not entries:
        # Fail-closed consistency with ``guard post-check``: an *onboarded*
        # project (a non-empty iterate.config.yaml exists) that declares no
        # ``validation.commands`` would make the promised post-check — and
        # therefore the defensive delivery gate — deterministically fail.
        # Handing out ``exit 0 = clear to start`` here would mislead a host AI
        # that relies on the pre-check/post-check exit-code contract. A brand
        # new project with no config yet degrades gracefully instead (there is
        # nothing on disk to validate yet).
        if config:
            result.items.append(
                (
                    "validation commands",
                    False,
                    ("no validation commands configured — post-check would fail closed; add"
                     " validation.commands to iterate.config.yaml"),
                )
            )
            result.passed = False
        else:
            result.items.append(
                ("validation commands", True, "none configured — not onboarded yet")
            )
    else:
        unsafe = [f"{m}:{c!r}" for m, c in entries if not _command_is_safe(c)]
        if unsafe:
            result.items.append(
                ("validation commands", False, "unsafe command(s): " + "; ".join(unsafe))
            )
            result.passed = False
        else:
            result.items.append(
                ("validation commands", True, f"{len(entries)} command(s) configured and metachar-safe (run via post-check)")
            )

    # 5. Validation command tools must actually be resolvable on PATH. Commands
    #    execute under ``shell=True``, so known shell builtins (true, test,
    #    echo, ...) are allowed even when ``shutil.which`` finds no binary. A
    #    genuinely missing executable (e.g. a tool uninstalled since onboarding)
    #    means the promised post-check would fail with a non-zero exit — surface
    #    that BEFORE the edit, not after.
    if entries:
        missing_tools = []
        for module, command in entries:
            stripped = command.strip()
            if not stripped:
                continue
            first = stripped.split(maxsplit=1)[0]
            if first in SHELL_BUILTINS:
                continue
            if shutil.which(first) is None:
                missing_tools.append(f"{module}: {first!r}")
        if missing_tools:
            result.items.append(
                (
                    "tools available",
                    False,
                    "missing executable(s): " + "; ".join(missing_tools),
                )
            )
            result.passed = False
        else:
            result.items.append(
                ("tools available", True, "every configured command's tool is on PATH")
            )

    return result


def run_guard_postcheck(project_root: Path, modules: list[str] | None, dry_run: bool = False) -> GuardResult:
    """Run the post-edit guard: execute exactly the configured validation commands.

    Args:
        project_root: Project root directory.
        modules: Optional module filter (``iterate guard post-check python``).
        dry_run: When True, preview the exact commands without executing them.

    Returns:
        A GuardResult with one item per (module, command).
    """
    result = GuardResult(name="guard-post", dry_run=dry_run)
    result.passed = True
    try:
        config = _load_project_config(project_root)
    except (CorruptConfigError, OSError, UnicodeDecodeError) as exc:
        result.items.append(("config readable", False, str(exc)))
        result.passed = False
        return result

    validation = _validation_commands(config)
    entries = _command_entries(validation, modules)
    # Requested-but-unconfigured modules must be reported, never silently
    # skipped: a host AI that lists multiple modules must not believe an
    # unconfigured module was validated.
    requested_missing = [
        module for module in (modules or []) if module not in validation
    ]
    if requested_missing:
        for module in requested_missing:
            result.items.append(
                (f"{module}", False, "requested but not configured in validation.commands")
            )
            result.passed = False

    if not entries:
        wanted = ", ".join(requested_missing or modules or ["any module"])
        result.items.append(
            ("validation commands", False, f"no commands configured for {wanted}")
        )
        result.passed = False
        return result

    for module, command in entries:
        if dry_run:
            if not _command_is_safe(command):
                result.items.append(
                    (f"{module}", False, f"refused: unsafe command {command!r} (shell metacharacter or empty)")
                )
                result.passed = False
            else:
                result.items.append((f"{module}", True, f"would run: {command}"))
            continue
        code, tail = _run_command(command, project_root)
        ok = code == 0
        detail = f"{command} → exit {code}"
        if tail:
            detail += f" | {tail}"
        result.items.append((f"{module}", ok, detail))
        if not ok:
            result.passed = False
    return result


def run_invariant_check(project_root: Path, dry_run: bool = False) -> GuardResult:
    """Run project-level invariants (``iterate invariant``).

    Checks, in order:
    1. ``invariants.ensure`` file assertions (each declared path must exist).
    2. ``invariants.commands.<module>`` command lists (exact match, executed).
    When no ``invariants`` section is configured, degrades to the configured
    ``validation.commands`` so pre-v3.0 configs remain valid.

    Args:
        project_root: Project root directory.
        dry_run: When True, preview commands without executing anything.

    Returns:
        A GuardResult with one item per assertion/command.
    """
    result = GuardResult(name="invariant", dry_run=dry_run)
    result.passed = True
    try:
        config = _load_project_config(project_root)
    except (CorruptConfigError, OSError, UnicodeDecodeError) as exc:
        result.items.append(("config readable", False, str(exc)))
        result.passed = False
        return result

    # 1. File assertions (invariants.ensure). Paths must be project-relative:
    #    an absolute path (or one resolving outside the project root) would
    #    assert on files the skill does not own, so it is reported as a
    #    failure rather than checked.
    root_resolved = project_root.resolve()
    for entry in _invariant_ensure(config):
        if Path(entry).is_absolute():
            result.items.append(
                (f"ensure:{entry}", False, f"absolute path not allowed: {entry}")
            )
            result.passed = False
            continue
        target = (project_root / entry).resolve()
        if not target.is_relative_to(root_resolved):
            result.items.append(
                (f"ensure:{entry}", False, f"path escapes project root: {entry}")
            )
            result.passed = False
            continue
        ok = target.is_file()
        result.items.append((f"ensure:{entry}", ok, "present" if ok else f"missing: {entry}"))
        if not ok:
            result.passed = False

    # 2. Invariant commands; fall back to validation.commands ONLY when the
    #    invariants section is absent or not a mapping (design §6: "无
    #    invariants 段时退化为..."). A project that deliberately declares
    #    invariants with ensure-only (no commands) must NOT silently re-run the
    #    full validation.commands as invariants.
    commands = _invariant_commands(config)
    source = "invariants.commands"
    if not isinstance(config.get("invariants"), dict):
        commands = _validation_commands(config)
        source = "validation.commands (invariants fallback)"
    entries = _command_entries(commands, None)
    if not entries:
        result.items.append((source, True, "no invariant commands configured"))
        return result

    for module, command in entries:
        if dry_run:
            if not _command_is_safe(command):
                result.items.append(
                    (f"{module} ({source})", False, f"refused: unsafe command {command!r} (shell metacharacter or empty)")
                )
                result.passed = False
            else:
                result.items.append((f"{module} ({source})", True, f"would run: {command}"))
            continue
        code, tail = _run_command(command, project_root)
        ok = code == 0
        detail = f"{command} → exit {code}"
        if tail:
            detail += f" | {tail}"
        result.items.append((f"{module} ({source})", ok, detail))
        if not ok:
            result.passed = False
    return result


def render_guard_result(result: GuardResult, json_output: bool = False) -> int:
    """Render a GuardResult and return the process exit code.

    Args:
        result: The check result to display.
        json_output: When True, emit a structured JSON object instead of TUI lines.

    Returns:
        0 when everything passed, 1 otherwise.
    """
    if json_output:
        import json

        print(
            json.dumps(
                {
                    "check": result.name,
                    "passed": result.passed,
                    "dry_run": result.dry_run,
                    "items": [
                        {"label": label, "ok": ok, "detail": detail}
                        for label, ok, detail in result.items
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return EXIT_PASS if result.passed else EXIT_FAIL

    if result.dry_run:
        if result.name == "guard-pre":
            # pre-check is static validation: it never runs a command, so a
            # "DRY-RUN preview (nothing executed)" banner implied that the
            # normal path *does* execute something, and made the no-op flag
            # look like it changed the outcome. Say what is actually true.
            tui.info(
                "guard-pre is read-only: it never executes commands, "
                "so --dry-run does not change what runs.",
                indent=2,
            )
        else:
            tui.warning(f"{result.name}: DRY-RUN preview (nothing executed)", indent=2)
    if result.passed:
        tui.success(f"{result.name}: PASS")
    else:
        tui.error(f"{result.name}: FAIL")
    for label, ok, detail in result.items:
        if ok:
            tui.bullet(f"{label}: {detail}", indent=4)
        else:
            tui.warning(f"{label}: {detail}", indent=4)
    return EXIT_PASS if result.passed else EXIT_FAIL
