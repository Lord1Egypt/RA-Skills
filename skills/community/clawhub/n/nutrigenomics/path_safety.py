"""
path_safety.py — Input validation and path traversal prevention for Nutrigenomics

All file paths supplied by users are validated here before the rest of the pipeline
touches them. Three checks are enforced:

  1. Allowed extensions — only .txt, .csv, and .vcf are accepted as input.
  2. Path traversal prevention — resolved paths must stay within expected roots.
  3. Existence — the file must actually exist before processing begins.
"""

import errno
import os
from pathlib import Path


# Extensions accepted as genetic data input
ALLOWED_INPUT_EXTENSIONS = {".txt", ".csv", ".vcf"}


# ── Resource limits ───────────────────────────────────────────────────────────
# A genetic file is untrusted input. Parsing is streamed, but the genotype table
# still grows with the number of variants, so streaming alone does not bound
# memory. These caps are far above any real consumer export (23andMe ~600k
# variants, ~25 MB; a whole-genome VCF is larger but still well inside them) and
# exist so that a crafted or corrupt file fails with a clear error instead of
# exhausting the machine.
MAX_INPUT_BYTES = 512 * 1024 * 1024      # 512 MB
MAX_VARIANTS = 10_000_000                # rows retained in the genotype table
MAX_LINE_BYTES = 64 * 1024               # one variant line; real ones are < 100 B
MAX_HEADER_LINES = 1000                  # lines inspected when sniffing the format


def _human_bytes(n: int) -> str:
    """Render a byte count readably at any magnitude."""
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} GB"


def check_input_size(path: Path) -> None:
    """Raise ValueError if the input file exceeds MAX_INPUT_BYTES."""
    size = path.stat().st_size
    if size > MAX_INPUT_BYTES:
        raise ValueError(
            f"Input file is {_human_bytes(size)}, above the "
            f"{_human_bytes(MAX_INPUT_BYTES)} limit. If this is a genuine genetic "
            f"file, split it or raise MAX_INPUT_BYTES in path_safety.py."
        )


def validate_input_file(input_file: str) -> Path:
    """
    Validate a user-supplied genetic data file path.

    Checks:
    - The path resolves without escaping the filesystem root (no null bytes, etc.)
    - The file extension is in the allowed list (.txt, .csv, .vcf)
    - The file exists on disk

    Args:
        input_file: Raw path string supplied by the caller.

    Returns:
        Resolved absolute Path object.

    Raises:
        ValueError: If the extension is not allowed or the path looks unsafe.
        FileNotFoundError: If the file does not exist.
    """
    try:
        path = Path(input_file).resolve()
    except Exception as exc:
        raise ValueError(f"Invalid file path: {input_file!r}") from exc

    # Reject null bytes and other control characters
    if "\x00" in str(path):
        raise ValueError("File path contains invalid characters.")

    if path.suffix.lower() not in ALLOWED_INPUT_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{path.suffix}'. "
            f"Accepted formats: {', '.join(sorted(ALLOWED_INPUT_EXTENSIONS))}."
        )

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")

    check_input_size(path)
    return path


def validate_output_dir(output_dir: str, workspace_root: Path) -> Path:
    """
    Validate and return a safe output directory path.

    The resolved output directory must be located inside workspace_root to
    prevent writes to arbitrary locations on the filesystem.

    Args:
        output_dir: Raw path string for the desired output directory.
        workspace_root: Resolved absolute Path that output must stay within.

    Returns:
        Resolved absolute Path to the output directory (created if absent).

    Raises:
        ValueError: If the path escapes workspace_root.
    """
    try:
        path = Path(output_dir).resolve()
    except Exception as exc:
        raise ValueError(f"Invalid output directory: {output_dir!r}") from exc

    workspace_root = workspace_root.resolve()

    # Ensure output stays within the workspace (prevents path traversal)
    try:
        path.relative_to(workspace_root)
    except ValueError:
        raise ValueError(
            f"Output directory '{path}' is outside the allowed workspace "
            f"'{workspace_root}'. Choose a directory inside your working folder."
        )

    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_panel_file(panel_path: str, skill_root: Path) -> Path:
    """
    Validate a custom SNP panel file path.

    The panel must reside within the skill's own directory to prevent loading
    arbitrary JSON files from elsewhere on the filesystem.

    Args:
        panel_path: Raw path string to the panel JSON file.
        skill_root: Resolved absolute Path to the skill's root directory.

    Returns:
        Resolved absolute Path to the panel file.

    Raises:
        ValueError: If the path escapes skill_root or is not a .json file.
        FileNotFoundError: If the file does not exist.
    """
    try:
        path = Path(panel_path).resolve()
    except Exception as exc:
        raise ValueError(f"Invalid panel file path: {panel_path!r}") from exc

    skill_root = skill_root.resolve()

    try:
        path.relative_to(skill_root)
    except ValueError:
        raise ValueError(
            f"Custom panel '{path}' is outside the skill directory '{skill_root}'. "
            "Panel files must be located within the skill folder."
        )

    if path.suffix.lower() != ".json":
        raise ValueError(
            f"Panel file must be a .json file, got '{path.suffix}'."
        )

    if not path.exists():
        raise FileNotFoundError(f"Panel file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Panel path is not a file: {path}")

    return path


def safe_open_write(path: Path, binary: bool = False):
    """
    Open ``path`` for writing, refusing to follow a symlink at the final component.

    ``Path.write_text`` and ``open(..., "w")`` follow symlinks, so an attacker who
    can pre-create a symlink at a predictable output filename (the output directory
    and file names are deterministic) can redirect the write anywhere the user can
    write — outside the directory validate_output_dir carefully confined us to.

    O_NOFOLLOW makes the open fail with ELOOP instead. O_EXCL is deliberately not
    used: overwriting a regular file on a re-run is legitimate and expected.
    """
    path = Path(path)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW

    # O_NOFOLLOW guards only the FINAL component, so a symlinked parent directory
    # would still redirect the write. Open the parent itself with O_NOFOLLOW and
    # O_DIRECTORY, then create the file relative to that descriptor: the fd pins a
    # real directory inode, so swapping the parent for a symlink afterwards cannot
    # move the write. (ClawHub audit: parent-directory symlink race.)
    try:
        dir_fd = os.open(
            str(path.parent), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        )
    except OSError as exc:
        if exc.errno in (errno.ELOOP, errno.ENOTDIR):
            raise ValueError(
                f"Refusing to write into '{path.parent}': it is a symbolic link, "
                f"not a real directory."
            ) from exc
        raise

    try:
        fd = os.open(path.name, flags, 0o600, dir_fd=dir_fd)
    except OSError as exc:
        if exc.errno in (errno.ELOOP, errno.EMLINK):
            raise ValueError(
                f"Refusing to write to '{path}': it is a symbolic link. "
                f"Remove it and re-run."
            ) from exc
        raise
    finally:
        os.close(dir_fd)

    return os.fdopen(fd, "wb" if binary else "w", encoding=None if binary else "utf-8")


def safe_write_text(path: Path, text: str) -> None:
    """Write text to ``path`` without following a symlink at the final component."""
    with safe_open_write(path) as fh:
        fh.write(text)
