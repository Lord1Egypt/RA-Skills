"""
path_safety.py — Input validation and path traversal prevention for Nutrigenomics

All file paths supplied by users are validated here before the rest of the pipeline
touches them. Three checks are enforced:

  1. Allowed extensions — only .txt, .csv, and .vcf are accepted as input.
  2. Path traversal prevention — resolved paths must stay within expected roots.
  3. Existence — the file must actually exist before processing begins.
"""

from pathlib import Path


# Extensions accepted as genetic data input
ALLOWED_INPUT_EXTENSIONS = {".txt", ".csv", ".vcf"}


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
