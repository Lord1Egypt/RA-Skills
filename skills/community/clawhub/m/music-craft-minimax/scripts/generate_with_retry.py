#!/usr/bin/env python3
"""Run an mmx command with transient retry and a safer default timeout.

Each invocation uses an isolated temporary working directory (run_dir) so
that concurrent runs do not collide on output filenames. On success, the
generated file can optionally be moved to a caller-specified output path,
and a best-effort duration check (ffprobe) can warn if the output is
materially shorter than expected.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


TRANSIENT_MARKERS = (
    "code 5",
    "code 6",
    "request timed out",
    "network request failed",
    "network",
    "timeout",
)

# Duration-warning threshold: output is flagged if actual < expected * DURATION_WARN_RATIO
DURATION_WARN_RATIO = 0.7

# Maximum exponential backoff multiplier for retry delays
MAX_BACKOFF_MULTIPLIER = 16

# Cloud generations can finish writing the MP3 and then have the shell receive a
# signal. Treat these return codes as recoverable when this run created output.
SIGNAL_AFTER_SAVE_CODES = {-15, -9, 137, 143}

# Operational prompt-budget recommendation from the v1.3.0 field run. This is
# a warning only; the hard API limit remains higher and is enforced by the linter.
PROMPT_LENGTH_WARN_CHARS = 500

MP3_MIN_HEADER_BYTES = 4
MP3_FALLBACK_MIN_BYTES = 102400


def _has_timeout(args: list[str]) -> bool:
    return "--timeout" in args or any(arg.startswith("--timeout=") for arg in args)


def _is_transient(returncode: int, stderr: str) -> bool:
    lowered = stderr.lower()
    return returncode in {5, 6} or any(marker in lowered for marker in TRANSIENT_MARKERS)


def _prompt_text(args: list[str]) -> str | None:
    for index, arg in enumerate(args):
        if arg == "--prompt" and index + 1 < len(args):
            return args[index + 1]
        if arg.startswith("--prompt="):
            return arg.split("=", 1)[1]
    return None


def _warn_prompt_budget(args: list[str]) -> None:
    prompt = _prompt_text(args)
    if prompt and len(prompt) > PROMPT_LENGTH_WARN_CHARS:
        print(
            f"WARNING: prompt is {len(prompt)} characters; v1.3.0 cloud-batch "
            f"guidance recommends keeping standard prompts under "
            f"{PROMPT_LENGTH_WARN_CHARS} characters when possible.",
            file=sys.stderr,
        )


# Path-bearing flags whose values are relative-path strings that must be
# resolved from the caller's original cwd (not the isolated run_dir).
_RELATIVE_PATH_FLAGS = {"--lyrics-file", "--audio-file", "--out"}


def _resolve_relative_paths(args: list[str], original_cwd: Path) -> list[str]:
    """Resolve relative-path flag values to absolute paths using original_cwd.

    mmx path-bearing flags like --lyrics-file and --out accept relative paths,
    which would break when the command is run from the isolated run_dir.
    This function converts any relative-valued path flags to absolute paths
    using the original working directory so they work correctly.
    """
    resolved = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in _RELATIVE_PATH_FLAGS and i + 1 < len(args):
            resolved.append(arg)
            path_val = args[i + 1]
            # Only resolve paths that are not already absolute
            if not path_val.startswith("/") and not path_val.startswith("~"):
                resolved.append(str(original_cwd / path_val))
            else:
                resolved.append(path_val)
            i += 2
        elif any(arg.startswith(f"{flag}=") for flag in _RELATIVE_PATH_FLAGS):
            flag, path_val = arg.split("=", 1)
            if path_val and not path_val.startswith("/") and not path_val.startswith("~"):
                resolved.append(f"{flag}={original_cwd / path_val}")
            else:
                resolved.append(arg)
            i += 1
        else:
            resolved.append(arg)
            i += 1
    return resolved


def _flag_value(args: list[str], flag: str) -> str | None:
    for index, arg in enumerate(args):
        if arg == flag and index + 1 < len(args):
            return args[index + 1]
        if arg.startswith(f"{flag}="):
            return arg.split("=", 1)[1]
    return None


def _is_mmx_music_generation(args: list[str]) -> bool:
    return len(args) >= 2 and args[0] == "music" and args[1] in {"generate", "cover"}


def _missing_required_out(args: list[str], output_path: str | None) -> bool:
    return bool(output_path) and _is_mmx_music_generation(args) and _flag_value(args, "--out") is None


def _is_nonempty_file(path: Path) -> bool:
    try:
        return path.is_file() and path.stat().st_size > 0
    except OSError:
        return False


def _candidate_output_paths(command_args: list[str], output_path: str | None) -> list[Path]:
    candidates: list[Path] = []
    if output_path:
        candidates.append(Path(output_path))
    out_flag = _flag_value(command_args, "--out")
    if out_flag:
        candidates.append(Path(out_flag).expanduser())
    # Preserve order while removing duplicates.
    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    return unique


def _extract_saved_name(stdout: str) -> str | None:
    """Extract the saved-filename from mmx stdout.

    Handles two observed formats:
    - JSON:  {"saved": "music_2026-06-11-14-35-32.mp3"}
    - Plain: saved: music_2026-06-11-14-35-32.mp3
    """
    for line in stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("attempt"):
            continue
        # Try JSON first
        try:
            obj = json.loads(line)
            if isinstance(obj, dict) and "saved" in obj:
                return obj["saved"]
        except json.JSONDecodeError:
            pass
        # Try plain "saved: ..." format
        if line.startswith("saved:"):
            saved = line[len("saved:"):].strip()
            if saved:
                return saved
    return None


def _move_to_output(saved_path: Path, output_path: Path, overwrite: bool = False) -> None:
    """Move the generated file to the caller-specified output path."""
    if not overwrite and output_path.exists():
        raise FileExistsError(
            f"output already exists at {output_path}; use --overwrite to replace it"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(saved_path), str(output_path))


def _target_for_saved_name(
    saved_name: str,
    candidates: list[Path],
    original_cwd: Path,
) -> Path:
    """Choose a non-temp destination for a saved file.

    Prefer the explicit wrapper/CLI output path. Without one, preserve the
    saved filename in the caller's original cwd so tempdir cleanup cannot delete
    the only copy.
    """
    if candidates:
        return candidates[0]
    return original_cwd / Path(saved_name).name


def _output_snapshot(paths: list[Path]) -> dict[str, tuple[int, int] | None]:
    snapshot: dict[str, tuple[int, int] | None] = {}
    for path in paths:
        try:
            stat = path.stat()
        except OSError:
            snapshot[str(path)] = None
        else:
            snapshot[str(path)] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def _is_new_or_changed_nonempty(path: Path, before: dict[str, tuple[int, int] | None]) -> bool:
    try:
        stat = path.stat()
    except OSError:
        return False
    if not path.is_file() or stat.st_size <= 0:
        return False
    return before.get(str(path)) != (stat.st_size, stat.st_mtime_ns)


def _is_probeable_audio(path: Path) -> bool:
    ffprobe_bin = shutil.which("ffprobe")
    if not ffprobe_bin:
        try:
            size = path.stat().st_size
            with path.open("rb") as handle:
                header = handle.read(MP3_MIN_HEADER_BYTES)
        except OSError:
            return False
        if size < MP3_FALLBACK_MIN_BYTES:
            print(
                f"WARNING: ffprobe not found; refusing signal-saved output at {path} "
                f"because it is only {size} bytes (minimum {MP3_FALLBACK_MIN_BYTES}).",
                file=sys.stderr,
            )
            return False
        if header.startswith(b"ID3") or (
            len(header) >= 2 and header[0] == 0xFF and (header[1] & 0xE0) == 0xE0
        ):
            print(
                f"WARNING: ffprobe not found; accepting signal-saved output at {path} "
                "based on size and MP3 header only.",
                file=sys.stderr,
            )
            return True
        print(
            f"WARNING: ffprobe not found; cannot validate signal-saved output at {path}",
            file=sys.stderr,
        )
        return False
    try:
        result = subprocess.run(
            [
                ffprobe_bin,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            text=True,
            capture_output=True,
            timeout=10,
        )
        if result.returncode != 0:
            return False
        return float(result.stdout.strip()) > 0
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def _accept_saved_output_after_signal(
    returncode: int,
    candidates: list[Path],
    before_snapshot: dict[str, tuple[int, int] | None],
    output_path: str | None,
    overwrite: bool,
    expected_duration_seconds: int | None,
) -> bool:
    if returncode not in SIGNAL_AFTER_SAVE_CODES:
        return False
    for candidate in candidates:
        if _is_new_or_changed_nonempty(candidate, before_snapshot):
            if before_snapshot.get(str(candidate)) is not None and not overwrite:
                print(
                    f"WARNING: signal-saved output changed pre-existing file at {candidate}; "
                    "not accepting it as success without --overwrite.",
                    file=sys.stderr,
                )
                return False
            if not _is_probeable_audio(candidate):
                print(
                    f"WARNING: signal-saved output at {candidate} is not probeable; "
                    "not accepting it as success.",
                    file=sys.stderr,
                )
                return False
            final_path = candidate
            if output_path:
                final_path = Path(output_path)
                if candidate != final_path:
                    try:
                        _move_to_output(candidate, final_path, overwrite=overwrite)
                    except FileExistsError as exc:
                        print(
                            f"WARNING: {exc}; not accepting signal-saved output",
                            file=sys.stderr,
                        )
                        return False
            print(
                f"WARNING: mmx exited with signal-style code {returncode}, "
                f"but output exists at {final_path}; accepting saved file.",
                file=sys.stderr,
            )
            if expected_duration_seconds is not None:
                _warn_if_short(final_path, expected_duration_seconds)
            return True
    return False


def _preserve_success_output(
    saved_name: str | None,
    run_dir: Path,
    run_dir_snapshot: dict[str, tuple[int, int] | None],
    candidates: list[Path],
    candidate_snapshot: dict[str, tuple[int, int] | None],
    original_cwd: Path,
    output_path: str | None,
    overwrite: bool,
    expected_duration_seconds: int | None,
) -> bool:
    def warn_if_unprobeable(path: Path) -> None:
        if not _is_probeable_audio(path):
            print(
                f"WARNING: successful output at {path} could not be validated; "
                "preserving it because mmx exited successfully.",
                file=sys.stderr,
            )

    stale_saved_path: Path | None = None
    if saved_name:
        saved_path = run_dir / saved_name
        if _is_nonempty_file(saved_path):
            if not _is_new_or_changed_nonempty(saved_path, run_dir_snapshot):
                stale_saved_path = saved_path
            else:
                warn_if_unprobeable(saved_path)
                target = _target_for_saved_name(saved_name, candidates, original_cwd)
                try:
                    if saved_path != target:
                        _move_to_output(saved_path, target, overwrite=overwrite)
                except FileExistsError as exc:
                    print(f"WARNING: {exc}; output was not preserved", file=sys.stderr)
                    return False
                if expected_duration_seconds is not None:
                    _warn_if_short(target, expected_duration_seconds)
                return True

    for candidate in candidates:
        if not _is_new_or_changed_nonempty(candidate, candidate_snapshot):
            continue
        warn_if_unprobeable(candidate)
        final_path = candidate
        if output_path:
            target = _target_for_saved_name(saved_name, candidates, original_cwd)
            try:
                if candidate != target:
                    _move_to_output(candidate, target, overwrite=overwrite)
            except FileExistsError as exc:
                print(f"WARNING: {exc}; output was not preserved", file=sys.stderr)
                return False
            final_path = target
        if expected_duration_seconds is not None:
            _warn_if_short(final_path, expected_duration_seconds)
        return True

    return False



def _recover_internal_output_after_signal(
    returncode: int,
    run_dir: Path,
    run_dir_snapshot: dict[str, tuple[int, int] | None],
    candidates: list[Path],
    original_cwd: Path,
    overwrite: bool,
    expected_duration_seconds: int | None,
) -> bool:
    if returncode not in SIGNAL_AFTER_SAVE_CODES:
        return False
    generated = sorted(
        (
            path
            for path in run_dir.glob("*.mp3")
            if _is_new_or_changed_nonempty(path, run_dir_snapshot)
        ),
        key=lambda path: path.stat().st_mtime_ns,
        reverse=True,
    )
    if not generated:
        return False

    target = candidates[0] if candidates else original_cwd / generated[0].name
    if not _is_probeable_audio(generated[0]):
        print(
            f"WARNING: signal-recovered output at {generated[0]} is not probeable; "
            "not accepting it as success.",
            file=sys.stderr,
        )
        return False
    try:
        _move_to_output(generated[0], target, overwrite=overwrite)
    except FileExistsError as exc:
        print(f"WARNING: {exc}; not accepting signal-recovered output", file=sys.stderr)
        return False

    print(
        f"WARNING: mmx exited with signal-style code {returncode}, "
        f"but a generated MP3 was recovered from the run directory and moved to {target}.",
        file=sys.stderr,
    )
    if expected_duration_seconds is not None:
        _warn_if_short(target, expected_duration_seconds)
    return True


def _warn_if_short(output_path: Path | None, expected_seconds: int) -> None:
    """Best-effort duration check using ffprobe; silently skips if ffprobe is unavailable."""
    if output_path is None or not output_path.exists():
        return
    ffprobe_bin = shutil.which("ffprobe")
    if not ffprobe_bin:
        return
    try:
        result = subprocess.run(
            [
                ffprobe_bin,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(output_path),
            ],
            text=True,
            capture_output=True,
            timeout=10,
        )
        if result.returncode != 0:
            return
        duration_str = result.stdout.strip()
        actual_seconds = float(duration_str)
        if actual_seconds <= 0:
            return
        if actual_seconds < expected_seconds * DURATION_WARN_RATIO:
            print(
                f"WARNING: output duration ({actual_seconds:.0f}s) is materially shorter "
                f"than expected ({expected_seconds}s). MiniMax lyric-heavy generations "
                f"often produce 120-150s even when longer is requested.",
                file=sys.stderr,
            )
    except (ValueError, subprocess.TimeoutExpired):
        pass


def run_with_retry(
    mmx_bin: str,
    command_args: list[str],
    attempts: int,
    retry_delay: float,
    output_path: str | None = None,
    expected_duration_seconds: int | None = None,
    overwrite: bool = False,
) -> int:
    if _missing_required_out(command_args, output_path):
        print(
            "ERROR: --output-path does not replace mmx --out. Pass the same final "
            "audio path to the mmx command with --out, and keep --output-path for "
            "post-run preservation/verification.",
            file=sys.stderr,
        )
        return 2

    if not _has_timeout(command_args):
        command_args = [*command_args, "--timeout", "600"]

    _warn_prompt_budget(command_args)

    # Resolve relative paths before entering the isolated run_dir so that
    # path-bearing flags like --lyrics-file, --audio-file, and --out work
    # relative to the caller's original cwd, not the temp directory.
    original_cwd = Path.cwd()
    command_args = _resolve_relative_paths(command_args, original_cwd)

    with tempfile.TemporaryDirectory() as run_dir:
        for attempt in range(1, attempts + 1):
            cmd = [mmx_bin, *command_args]
            output_candidates = _candidate_output_paths(command_args, output_path)
            before_snapshot = _output_snapshot(output_candidates)
            run_dir_path = Path(run_dir)
            run_dir_snapshot = _output_snapshot(list(run_dir_path.glob("*.mp3")))
            print(f"attempt {attempt}/{attempts}: {' '.join(cmd)}", file=sys.stderr)
            result = subprocess.run(cmd, text=True, capture_output=True, cwd=run_dir)
            stdout = result.stdout
            if stdout:
                print(stdout, end="")
            if result.returncode == 0:
                saved_name = _extract_saved_name(stdout)
                if _preserve_success_output(
                    saved_name,
                    run_dir_path,
                    run_dir_snapshot,
                    output_candidates,
                    before_snapshot,
                    original_cwd,
                    output_path,
                    overwrite,
                    expected_duration_seconds,
                ):
                    return 0
                if saved_name or output_candidates:
                    print(
                        "ERROR: mmx exited successfully but no generated output file "
                        "could be preserved.",
                        file=sys.stderr,
                    )
                    return 1
                if expected_duration_seconds is not None:
                    _warn_if_short(Path(output_path) if output_path else None, expected_duration_seconds)
                return 0
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            saved_name = _extract_saved_name(stdout)
            if result.returncode in SIGNAL_AFTER_SAVE_CODES and saved_name:
                saved_path = Path(run_dir) / saved_name
                if (
                    _is_new_or_changed_nonempty(saved_path, run_dir_snapshot)
                    and _is_probeable_audio(saved_path)
                ):
                    target = _target_for_saved_name(saved_name, output_candidates, original_cwd)
                    try:
                        if saved_path != target:
                            _move_to_output(saved_path, target, overwrite=overwrite)
                    except FileExistsError as exc:
                        print(
                            f"WARNING: {exc}; not accepting signal-saved output",
                            file=sys.stderr,
                        )
                        return result.returncode
                    if expected_duration_seconds is not None:
                        _warn_if_short(target, expected_duration_seconds)
                    return 0
            if _accept_saved_output_after_signal(
                result.returncode,
                output_candidates,
                before_snapshot,
                output_path,
                overwrite,
                expected_duration_seconds,
            ):
                return 0
            if _recover_internal_output_after_signal(
                result.returncode,
                run_dir_path,
                run_dir_snapshot,
                output_candidates,
                original_cwd,
                overwrite,
                expected_duration_seconds,
            ):
                return 0
            if attempt == attempts or not _is_transient(result.returncode, result.stderr):
                return result.returncode
            backoff = min(retry_delay * (3 ** (attempt - 1)), retry_delay * MAX_BACKOFF_MULTIPLIER)
            time.sleep(backoff)
    # The for-loop always returns or re-raises; this line is unreachable.
    assert False, "unreachable"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run mmx with retry on transient failures")
    parser.add_argument("--mmx-bin", default="mmx", help="Path to mmx binary")
    parser.add_argument("--attempts", type=int, default=3, help="Maximum attempts (default: 3)")
    parser.add_argument("--retry-delay", type=float, default=5.0, help="Initial retry delay seconds")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow the output file to be overwritten if it already exists",
    )
    parser.add_argument(
        "--output-path",
        help="Move the generated file here after success (isolates each run from filename collisions)",
    )
    parser.add_argument(
        "--expected-duration-seconds",
        type=int,
        help="Warn if the output is materially shorter than this value (best-effort, ffprobe optional)",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command after --, e.g. -- music generate ...")
    args = parser.parse_args(argv)

    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("missing mmx command after --")
    return run_with_retry(
        args.mmx_bin,
        command,
        args.attempts,
        args.retry_delay,
        output_path=args.output_path,
        expected_duration_seconds=args.expected_duration_seconds,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    raise SystemExit(main())
