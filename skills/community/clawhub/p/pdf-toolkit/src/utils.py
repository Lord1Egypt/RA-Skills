import os
import shutil
import subprocess
from pathlib import Path


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def resolve_path(raw: str) -> Path:
    """Resolve a path string, expanding ~ and making it absolute."""
    return Path(raw).expanduser().resolve()


def require_file(path: Path, extensions: set[str] | None = None) -> str | None:
    """Return an error string if the path is not a readable file with an allowed extension."""
    if not path.exists():
        return f"File not found: {path}"
    if not path.is_file():
        return f"Not a file: {path}"
    if extensions and path.suffix.lower() not in extensions:
        allowed = ", ".join(sorted(extensions))
        return f"Unsupported file type '{path.suffix}'. Expected one of: {allowed}"
    return None


def ensure_output_dir(output: Path) -> str | None:
    """Create parent directories for an output path. Return error string on failure."""
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        return None
    except OSError as exc:
        return f"Cannot create output directory {output.parent}: {exc}"


# ---------------------------------------------------------------------------
# Page-range parsing
# ---------------------------------------------------------------------------


def parse_page_ranges(spec: str, total_pages: int) -> list[int] | str:
    """
    Parse a page-range spec like "1,3,5-8" into a sorted list of 0-based page indices.
    Pages are 1-indexed in the spec. Returns an error string on bad input.
    """
    indices: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            bounds = part.split("-", 1)
            try:
                start, end = int(bounds[0]), int(bounds[1])
            except ValueError:
                return f"Invalid page range: '{part}'"
            if start < 1 or end < start or end > total_pages:
                return f"Page range {part} is out of bounds (document has {total_pages} pages)"
            indices.update(range(start - 1, end))
        else:
            try:
                page = int(part)
            except ValueError:
                return f"Invalid page number: '{part}'"
            if page < 1 or page > total_pages:
                return (
                    f"Page {page} is out of bounds (document has {total_pages} pages)"
                )
            indices.add(page - 1)
    return sorted(indices)


# ---------------------------------------------------------------------------
# Argument parsing helpers
# ---------------------------------------------------------------------------


def get_flag(args: list[str], flag: str) -> str | None:
    """Return the value after --flag in args, or None if not present."""
    try:
        idx = args.index(flag)
        return args[idx + 1]
    except (ValueError, IndexError):
        return None


def has_flag(args: list[str], flag: str) -> bool:
    """Return True if --flag is present in args."""
    return flag in args


def get_positional_args(args: list[str]) -> list[str]:
    """Return all positional arguments (not starting with --)."""
    result = []
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg.startswith("--"):
            skip_next = True
        else:
            result.append(arg)
    return result


# ---------------------------------------------------------------------------
# Binary detection
# ---------------------------------------------------------------------------


def which(binary: str) -> str | None:
    """Return the full path to a binary if it exists on PATH, else None."""
    return shutil.which(binary)


def is_binary_available(binary: str) -> bool:
    """Return True if a system binary is available on PATH."""
    return which(binary) is not None


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------


def run_command(
    cmd: list[str], input_data: bytes | None = None, timeout: int = 60
) -> tuple[int, bytes, str]:
    """
    Run a subprocess command. Returns (returncode, stdout_bytes, stderr_str).
    Raises RuntimeError on timeout.
    """
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr.decode(errors="replace")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Command timed out after {timeout}s: {' '.join(cmd)}")
    except FileNotFoundError:
        raise RuntimeError(f"Binary not found: {cmd[0]}")


# ---------------------------------------------------------------------------
# Text cleanup
# ---------------------------------------------------------------------------


def clean_text(text: str) -> str:
    """Normalise whitespace: collapse blank lines to single blank line, strip trailing spaces."""
    lines = text.splitlines()
    cleaned = []
    prev_blank = False
    for line in lines:
        stripped = line.rstrip()
        is_blank = stripped == ""
        if is_blank and prev_blank:
            continue
        cleaned.append(stripped)
        prev_blank = is_blank
    return "\n".join(cleaned).strip()


def truncate_text(text: str, max_chars: int, label: str = "") -> str:
    """Truncate text to max_chars, appending a note if truncated."""
    if len(text) <= max_chars:
        return text
    suffix = (
        f"\n\n[{label + ': t' if label else 'T'}runcated at {max_chars:,} characters]"
    )
    return text[:max_chars] + suffix


# ---------------------------------------------------------------------------
# Binary content detection
# ---------------------------------------------------------------------------


def is_binary_content(data: bytes, sample: int = 512) -> bool:
    """Heuristic: return True if the first `sample` bytes contain null bytes."""
    return b"\x00" in data[:sample]
