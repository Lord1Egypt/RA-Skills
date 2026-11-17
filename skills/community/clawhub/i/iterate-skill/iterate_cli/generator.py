"""Onboarding output generator.

Renders ITERATE.md (project knowledge base) and iterate.config.yaml (project-level
overrides) from onboarding data. Supports incremental refresh by preserving
user-owned sections from an existing ITERATE.md.
"""

from __future__ import annotations

import os
import re
import shutil
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import uuid4

import yaml

from iterate_cli import __version__ as SKILL_VERSION
from iterate_cli.fingerprint import (
    FINGERPRINT_VERSION,
    FingerprintEntry,
    fingerprints_to_dict,
)
from iterate_cli.scan import ScanResult

if TYPE_CHECKING:
    from iterate_cli.personalize import PersonalizationData

# Partition markers in ITERATE.md.
AI_START_MARKER = "<!-- ITERATE:AI-MAINTAINED:START -->"
AI_END_MARKER = "<!-- ITERATE:AI-MAINTAINED:END -->"
USER_START_MARKER = "<!-- ITERATE:USER-OWNED:START -->"
USER_END_MARKER = "<!-- ITERATE:USER-OWNED:END -->"


def user_owned_bounds(content: str) -> tuple[int, int] | None:
    """Locate the USER-OWNED section markers in ``content``.

    Returns ``(start, end)`` where ``start`` is the index of the opening
    ``USER_START_MARKER`` and ``end`` is the index of the closing
    ``USER_END_MARKER`` — the whole block is
    ``content[start : end + len(USER_END_MARKER)]`` — or ``None`` when the
    markers are missing or degenerate.

    Robust against user text that embeds the literal marker string: the opening
    marker is searched for *after* the ``AI_END_MARKER`` partition, where the
    genuine user-owned block always lives, so a marker literal rendered into a
    generated AI section (project description, conventions, notes) can never be
    mistaken for it. The closing marker is taken as the last occurrence so a
    pasted marker literal inside the block cannot truncate it.

    Args:
        content: Full ITERATE.md content.

    Returns:
        ``(start, end)`` marker indices, or ``None`` when unusable.
    """
    # Generated content embeds user-supplied values in the AI-maintained area,
    # and those values may contain the marker text verbatim. A plain find()
    # would match that injected copy, splice mid-file and silently drop every
    # AI section below it. Anchor the search just past the AI partition.
    ai_end = content.rfind(AI_END_MARKER)
    search_from = ai_end + len(AI_END_MARKER) if ai_end != -1 else 0
    start_idx = content.find(USER_START_MARKER, search_from)
    if start_idx == -1:
        return None
    # Use the *last* occurrence of the END marker: user paste content may
    # legitimately contain the literal marker string (e.g. a pasted HTML
    # comment), and the true closing marker is the trailing one.
    end_idx = content.rfind(USER_END_MARKER)
    if end_idx == -1:
        return None
    # Strict ``end_idx > start_idx + len(USER_START_MARKER)`` (rather than
    # ``end_idx > start_idx``) rejects degenerate content where the two markers
    # are adjacent or the END marker overlaps the START marker text, which
    # yields an empty user-owned section.
    if end_idx <= start_idx + len(USER_START_MARKER):
        return None
    return start_idx, end_idx


def has_valid_user_owned_markers(content: str) -> bool:
    """Return True when ``content`` has ordered, non-overlapping USER-OWNED markers.

    "Valid" means both markers exist and the END marker appears strictly after
    the END of the START marker string, so the section is non-empty. See
    :func:`user_owned_bounds` for how the markers are located.

    Args:
        content: Full ITERATE.md content.

    Returns:
        True when the markers form a usable user-owned section.
    """
    return user_owned_bounds(content) is not None

# Matches the "完成时间 / Completed" row in the ITERATE.md Meta table.
_COMPLETED_AT_RE = re.compile(r"\| 完成时间 / Completed \| ([^|\n]+) \|")

# Matches exactly one ``{{PLACEHOLDER}}`` token in the ITERATE.md template.
_PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")


def _extract_completed_at(existing_md: str) -> str | None:
    """Extract the previous completion timestamp from an existing ITERATE.md.

    Used by incremental refresh so an unchanged refresh stays a byte-for-byte
    no-op instead of restamping ``{{COMPLETED_AT}}`` and producing a spurious
    diff. Returns ``None`` when the value cannot be found or is still the
    unresolved placeholder.
    """
    match = _COMPLETED_AT_RE.search(existing_md)
    if not match:
        return None
    value = match.group(1).strip()
    if not value or value == "{{COMPLETED_AT}}":
        return None
    return value

# Default values used when generating a fresh iterate.config.yaml.
DEFAULT_MAX_ROUNDS = 7
DEFAULT_ATOMIC_MAX_LINES = 20
DEFAULT_ATOMIC_MAX_ADJACENT_METHODS = 3
DEFAULT_GOAL = "Improve code quality and maintainability"
DEFAULT_LANGUAGE = "en"
# Top-level execution mode (mirrors config.schema.json's ``mode`` enum):
# ``iterate`` is the classic review-fix-converge loop, ``defensive`` opts into
# defensive-programming mode. Kept in sync by tests.
DEFAULT_MODE = "iterate"
MODE_VALUES: frozenset[str] = frozenset({"iterate", "defensive"})
DEFAULT_TARGET_BRANCH = "main"
DEFAULT_REVIEW_SCOPE = "full"
# Default chunk size for splitting the review scope into per-round batches.
DEFAULT_SCOPE_CHUNK_SIZE = 25

# Accepted LLM reasoning-effort levels (mirrors config.stream's enum). ``None``
# means "follow the provider default". Kept in sync by tests.
REASONING_EFFORT_VALUES: frozenset[str] = frozenset({"low", "medium", "high"})
DEFAULT_REASONING_EFFORT: str | None = None

# Default user-owned section content when generating a fresh ITERATE.md.
DEFAULT_USER_OWNED_SECTION = """
## 自定义代码约定 / Custom Code Conventions

<!-- 在此添加你的项目特有的代码约定。刷新 onboarding 时本区内容会保留。 -->
<!-- Add your project-specific code conventions here. This section is preserved during refresh. -->

## 禁区与风险区 / Restricted & Risk Areas

<!-- 标记不可修改的文件、敏感目录、已知风险区。 -->
<!-- Mark files/dirs that should not be modified, sensitive areas, known risks. -->

## 手动批注 / Manual Annotations

<!-- 任何你想让 iterate 知道的额外信息。 -->
<!-- Any additional information you want iterate to know. -->
"""

# Template path: prefer bundled data (inside the installed package at
# iterate_cli/data/), fall back to the repo-relative templates/ dir so
# running from source still works. The bundled copy is shipped in the
# wheel via [tool.setuptools.package-data] in pyproject.toml.
_BUNDLED_TEMPLATE = Path(__file__).resolve().parent / "data" / "ITERATE.template.md"
_REPO_TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "ITERATE.template.md"
TEMPLATE_PATH = _BUNDLED_TEMPLATE if _BUNDLED_TEMPLATE.exists() else _REPO_TEMPLATE


@dataclass
class OnboardingData:
    """All data needed to generate onboarding outputs."""

    project_root: Path
    channel: str  # "cli" or "ai"
    scan: ScanResult
    project_description: str = ""
    code_conventions: str = ""
    dimensions: list[str] = field(default_factory=list)
    dimension_sets: dict[str, dict] = field(default_factory=dict)
    target_branch: str = DEFAULT_TARGET_BRANCH
    review_scope: str = DEFAULT_REVIEW_SCOPE
    push_per_round: bool = False
    validation_commands: dict[str, list[str]] = field(default_factory=dict)
    command_whitelist: list[str] = field(default_factory=list)
    fingerprints: list[FingerprintEntry] = field(default_factory=list)
    iterate_notes: str = ""
    language: str = DEFAULT_LANGUAGE
    goal: str = DEFAULT_GOAL
    max_rounds: int = DEFAULT_MAX_ROUNDS
    reasoning_effort: str | None = DEFAULT_REASONING_EFFORT
    atomic_max_lines: int = DEFAULT_ATOMIC_MAX_LINES
    atomic_max_adjacent_methods: int = DEFAULT_ATOMIC_MAX_ADJACENT_METHODS
    use_worktree: bool = False
    auto_merge: bool = False
    output_schema_validation: bool = True
    evidence_validation: bool = True
    coverage_validation: bool = True
    scope_chunk_size: int = DEFAULT_SCOPE_CHUNK_SIZE
    drift_ignore: list[str] = field(default_factory=list)
    #: User's deliberate drift-check switch. Preserved across re-onboarding —
    #: an operator who set ``drift_check: false`` used to get it silently
    #: flipped back to true by any wizard-driven regeneration, because the
    #: loader never read it and generate_config_yaml hardcoded ``True``.
    drift_check: bool = True
    #: Top-level execution mode. Preserved across re-onboarding — the wizard
    #: used to rebuild the config from a fixed key set with no ``mode`` key at
    #: all, so ``iterate onboard``/``reonboard`` silently reverted a project
    #: switched to ``defensive`` back to the ``iterate`` default.
    mode: str = DEFAULT_MODE
    #: Project-level defensive-programming invariants (``ensure`` file
    #: assertions + per-module ``commands``), or ``None`` when the project has
    #: no invariants section. Preserved across re-onboarding for the same
    #: reason as ``mode``.
    invariants: dict[str, Any] | None = None
    personalization: PersonalizationData | None = None

    def completed_at(self) -> str:
        """ISO 8601 timestamp of onboarding completion."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_reasoning_effort(value: object) -> str | None:
    """Coerce an arbitrary value to an accepted reasoning-effort level.

    Hand-edited configs may hold anything; return ``None`` (the provider
    default) for values outside the accepted set so a bad value never
    persists as a typo in the regenerated config.
    """
    if isinstance(value, str) and value in REASONING_EFFORT_VALUES:
        return value
    return None


def normalize_mode(value: object) -> str:
    """Coerce an arbitrary value to an accepted top-level ``mode``.

    A hand-edited ``mode: turbo`` (or a scalar/null) must not flow back into
    the regenerated config, where it would violate the schema enum and leave
    doctor flagging a value the wizard just reported as "loaded". Falls back
    to :data:`DEFAULT_MODE` (``iterate``), matching the schema default.
    """
    if isinstance(value, str) and value in MODE_VALUES:
        return value
    return DEFAULT_MODE


#: Module ids accepted in ``invariants.commands`` (mirrors the schema's
#: ``propertyNames`` pattern; no shell metacharacters allowed).
_INVARIANT_MODULE_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def normalize_invariants(
    raw: object,
    on_drop: Callable[[str], None] | None = None,
) -> dict[str, Any] | None:
    """Normalize an arbitrary ``invariants`` value to a schema-valid mapping.

    A hand-edited/partially-broken ``invariants`` section must not be
    re-persisted verbatim: the wizard re-serializes the config on save, so a
    non-mapping value, a whitespace-only command, or a duplicate ``ensure``
    entry would produce a config that ``iterate doctor`` keeps flagging even
    though the wizard just reported it as "loaded" (same class of defect as
    ``dimensions`` / ``validation.commands``).

    Args:
        raw: The raw ``invariants`` value from a config.
        on_drop: Optional callback invoked with each dropped module name (or
            ``"ensure"``). Callers that WRITE the normalized result back to
            disk MUST pass this (e.g. ``tui.warning``) so silently deleting a
            hand-written entry on the next save is announced rather than
            being invisible data loss.

    Returns:
        A normalized ``{"ensure": [...], "commands": {...}}`` mapping, or
        ``None`` when nothing usable survives — the caller then omits the key
        entirely, matching a config that never declared invariants.
    """
    if not isinstance(raw, dict):
        return None
    result: dict[str, Any] = {}

    raw_ensure = raw.get("ensure")
    if isinstance(raw_ensure, list):
        ensure: list[str] = []
        for entry in raw_ensure:
            if not isinstance(entry, str):
                continue
            text = entry.strip()
            if not text or text in ensure:
                continue
            ensure.append(text)
        if ensure:
            result["ensure"] = ensure

    raw_commands = raw.get("commands")
    if isinstance(raw_commands, dict):
        commands: dict[str, list[str]] = {}
        for module, cmds in raw_commands.items():
            if not isinstance(module, str) or not _INVARIANT_MODULE_RE.match(module):
                if on_drop is not None:
                    on_drop(str(module))
                continue
            if not isinstance(cmds, list):
                if on_drop is not None:
                    on_drop(module)
                continue
            # Keep command text verbatim (guards match configured entries
            # exactly) but drop empty/whitespace-only entries, mirroring
            # guard._invariant_commands.
            cleaned = [c for c in cmds if isinstance(c, str) and c.strip()]
            if not cleaned:
                if on_drop is not None:
                    on_drop(module)
                continue
            commands[module] = cleaned
        if commands:
            result["commands"] = commands

    return result or None


def generate_iterate_md(data: OnboardingData, completed_at: str | None = None) -> str:
    """Render the ITERATE.md content from onboarding data and template.

    If ``data.personalization`` is set, the user-owned section is populated
    with personalization content (conventions, notes, risk areas, etc.).
    Otherwise the default user-owned section template is used.

    Args:
        data: OnboardingData with scan results and user inputs.
        completed_at: Optional explicit completion timestamp to place in the
            Meta table. When ``None``, a fresh timestamp is generated. Refresh
            passes the previous value so an unchanged refresh is a no-op.

    Returns:
        Complete ITERATE.md file content as a string.

    Raises:
        FileNotFoundError: If the template file is missing.
    """
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    replacements: dict[str, str] = {
        "{{COMPLETED_AT}}": completed_at or data.completed_at(),
        "{{CHANNEL}}": data.channel,
        "{{SKILL_VERSION}}": SKILL_VERSION,
        "{{FINGERPRINT_VERSION}}": FINGERPRINT_VERSION,
        "{{PROJECT_ROOT}}": str(data.project_root),
        "{{PROJECT_OVERVIEW}}": _render_project_overview(data),
        "{{TECH_STACK}}": _render_tech_stack(data),
        "{{MODULE_MAP}}": _render_module_map(data),
        "{{RECOMMENDED_DIMENSIONS}}": _render_dimensions(data),
        "{{RECOMMENDED_DIMENSION_SETS}}": _render_dimension_sets(data),
        "{{ITERATE_NOTES}}": _render_iterate_notes(data),
    }

    # Single pass over the template: a substituted value may itself contain a
    # {{PLACEHOLDER}} literal (a user-entered project description or code
    # convention), and a sequential str.replace loop would expand that injected
    # copy on a later iteration, duplicating whole sections. re.sub never
    # rescans the text it inserts.
    content = _PLACEHOLDER_RE.sub(
        lambda match: replacements.get(match.group(0), match.group(0)),
        template,
    )

    # If personalization data is present, replace the default user-owned
    # section with the personalised content.
    if data.personalization is not None:
        user_md = data.personalization.to_user_md_sections()
        if user_md.strip():
            content = _replace_user_owned_section(content, user_md)

    return content


def generate_config_yaml(data: OnboardingData) -> str:
    """Render the iterate.config.yaml content with onboarding section.

    Args:
        data: OnboardingData with scan results and user inputs.

    Returns:
        Complete iterate.config.yaml file content as a string.
    """
    onboarding: dict[str, Any] = {
        "version": FINGERPRINT_VERSION,
        "completed_at": data.completed_at(),
        "channel": data.channel,
        "skill_version": SKILL_VERSION,
        "drift_check": data.drift_check,
        "fingerprints": fingerprints_to_dict(data.fingerprints),
        # Persist user-entered text so returning users who decline basic
        # update don't lose their previously entered description/conventions.
        "project_description": data.project_description,
        "code_conventions": data.code_conventions,
    }
    # Persist drift-ignore patterns so a fresh onboarding/re-onboarding does not
    # silently drop them (they are honoured by drift detection and fingerprinting).
    if data.drift_ignore:
        onboarding["drift_ignore"] = list(data.drift_ignore)

    config: dict[str, Any] = {
        "goal": data.goal,
        "max_rounds": data.max_rounds,
        "reasoning_effort": data.reasoning_effort,
        "language": data.language,
        "mode": data.mode,
        "dimensions": data.dimensions,
        "dimension_sets": data.dimension_sets if data.dimension_sets else {},
        "review": {"scope": data.review_scope},
        "atomic": {
            "max_lines": data.atomic_max_lines,
            "max_adjacent_methods": data.atomic_max_adjacent_methods,
        },
        "git": {
            "target_branch": data.target_branch,
            "use_worktree": data.use_worktree,
            "push_per_round": data.push_per_round,
            "auto_merge": data.auto_merge,
        },
        "validation": {
            "commands": data.validation_commands,
        },
        "reviewer": {
            "output_schema_validation": data.output_schema_validation,
            "evidence_validation": data.evidence_validation,
            "coverage_validation": data.coverage_validation,
            "scope_chunk_size": data.scope_chunk_size,
        },
        "onboarding": onboarding,
    }
    # The schema requires command_whitelist to be non-empty when present
    # (minItems: 1). Emitting ``command_whitelist: []`` would make the freshly
    # written config schema-invalid and doctor complain about a file we just
    # generated, so omit the key entirely when there is nothing to whitelist —
    # matching refresh.py / personalize.py.
    if data.command_whitelist:
        config["validation"]["command_whitelist"] = list(data.command_whitelist)

    # Preserve the project-level invariants section across regeneration. It is
    # omitted entirely when the project has none (``None``), matching a config
    # that never declared invariants — ``iterate invariant`` then degrades to
    # ``validation.commands``.
    if data.invariants is not None:
        config["invariants"] = data.invariants

    # Merge personalization structured fields into config.
    if data.personalization is not None:
        from iterate_cli.personalize import merge_personalization_into_config

        config = merge_personalization_into_config(config, data.personalization)

    return yaml.safe_dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False)


def fsync_dir(directory: Path) -> None:
    """Best-effort ``fsync`` of a directory entry after a rename.

    ``fsync`` on the file persists its bytes, but the *rename* that publishes
    it is a directory mutation: without a directory fsync a power loss can
    still lose the link (the file "vanishes" though the write returned
    success). Directories cannot be opened/fsynced on every platform (Windows),
    and a failure here must never fail an otherwise successful write, so both
    operations are suppressed.
    """
    try:
        dir_fd = os.open(directory, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(dir_fd)
    except OSError:
        pass
    finally:
        os.close(dir_fd)


def atomic_write(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write ``content`` to ``path`` atomically (temp file + ``os.replace``).

    Creating the temp file in the same directory keeps the rename on one
    mount point, and ``os.replace`` is atomic on POSIX, so readers never
    observe a partially written file. The temp file is removed on failure.

    Args:
        path: Destination file path.
        content: Full file content.
        encoding: Text encoding (default UTF-8).

    Raises:
        OSError: If the write or the final replace fails.
    """
    # Follow a symlinked destination and replace the *target*, not the link.
    # `os.replace(tmp, path)` on a symlink would swap the link for a regular
    # file, silently detaching dotfile-style setups (e.g. iterate.config.yaml
    # symlinked to ~/dotfiles): the real file keeps stale content and the
    # project points at a copy. Resolving first makes the atomic replace happen
    # at the real path while the symlink stays intact.
    if path.is_symlink():
        path = Path(os.path.realpath(path))
    # Use a process-unique, collision-resistant temp name so concurrent calls
    # (even within the same process) never write the same temp file.
    tmp_path = path.with_name(f".{path.name}.tmp-{os.getpid()}-{uuid4().hex[:8]}")
    # Preserve the original file's permission bits (e.g. 0600 for a config
    # that was manually restricted): os.replace swaps in the temp file whose
    # mode defaults to the umask, silently loosening permissions otherwise.
    try:
        original_mode = path.stat().st_mode & 0o777
    except OSError:
        original_mode = None
    # Create the temp file ourselves with O_EXCL|O_NOFOLLOW *and* the final mode
    # from the first byte: O_EXCL|O_NOFOLLOW stops a pre-seeded symlink at the
    # (randomised) temp path from redirecting the write, and opening with the
    # destination's own mode means a restricted file (e.g. 0600) is never
    # transiently world-readable during the write window. New files use 0o666 so
    # the umask still decides their mode, matching prior behaviour.
    create_mode = original_mode if original_mode is not None else 0o666
    open_flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(tmp_path, open_flags, create_mode)
        try:
            handle = os.fdopen(fd, "w", encoding=encoding)
        except BaseException:
            # fdopen did not take ownership; close the raw descriptor ourselves.
            os.close(fd)
            raise
        with handle:
            handle.write(content)
            # Flush + fsync before the rename so a crash after os.replace
            # cannot leave a truncated file at the destination path.
            handle.flush()
            os.fsync(handle.fileno())
        if original_mode is not None:
            os.chmod(tmp_path, original_mode)
        os.replace(tmp_path, path)
        # Make the RENAME durable too: fsync on the file only persists its
        # contents, so a power loss right after os.replace could still lose
        # the link itself (file "vanishes" though the write reported success).
        # fsyncing the parent directory closes that window. Best-effort and
        # self-contained: directories cannot be opened on some platforms
        # (Windows), and a failed dir-fsync must never fail a write whose
        # bytes already landed.
        fsync_dir(path.parent)
    except BaseException:
        # Clean up on *any* failure (not just OSError): a UnicodeEncodeError
        # from a limited ``encoding`` reaches here too and must not leave a
        # stray temp file behind. KeyboardInterrupt/SystemExit propagate after
        # cleanup.
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError as cleanup_err:
            _log_tmp_cleanup_failure(tmp_path, cleanup_err)
        raise


def backup_file(path: Path, tag: str) -> Path:
    """Copy ``path`` to a unique timestamped sibling backup.

    Backup names include a short random suffix on top of the UTC second: two
    writes in the same second (a loop, a CI retry, or refresh + personalize)
    used to reuse the same path, so the second ``copy2`` overwrote the only
    pre-change snapshot.

    Args:
        path: File to back up (must exist).
        tag: Short operation tag (e.g. ``refresh`` / ``personalize``).

    Returns:
        The backup path.

    Raises:
        OSError: If the copy fails. Callers must treat this as fatal before
            rewriting the original — a write without a recoverable backup is
            exactly the data-loss case this helper exists to prevent.
    """
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = path.with_name(f"{path.name}.{tag}-{stamp}-{uuid4().hex[:6]}")
    shutil.copy2(path, backup)
    return backup


def _log_tmp_cleanup_failure(tmp_path: Path, exc: OSError) -> None:
    """Log to stderr when a temp file left over after a failed write cannot be removed."""
    import sys

    print(
        f"Failed to remove temporary file {tmp_path}: {exc}",
        file=sys.stderr,
    )


def _log_rollback_failure(path: Path, original_err: OSError) -> None:
    """Log when rolling back an already-written file during a two-file write fails.

    After ``config_path`` write fails and the ITERATE.md rollback also fails, the
    two files may be inconsistent. Instead of silently proceeding, surface both
    errors so the caller/user can investigate.
    """
    import sys

    print(
        f"Failed to roll back {path} after write error: {original_err}. "
        f"The files may be inconsistent.",
        file=sys.stderr,
    )


def _warn_missing_user_markers() -> None:
    """Warn on stderr when re-onboarding an ITERATE.md without USER-OWNED markers.

    The user-owned section cannot be preserved, so hand-edited content in that
    file would be replaced by the default template. We refuse to do this
    silently and advise the user how to proceed.
    """
    from iterate_cli.tui import tui

    tui.error(
        "Existing ITERATE.md is missing the USER-OWNED section markers; "
        "hand-edited content will not be preserved. Restore the markers "
        "<!-- ITERATE:USER-OWNED:START --> / ...END --> and re-run, or back up "
        "the file first."
    )


def write_onboarding_outputs(
    data: OnboardingData,
    output_dir: Path,
    existing_md: str | None = None,
) -> tuple[Path, Path]:
    """Write ITERATE.md and iterate.config.yaml to the output directory.

    When ``existing_md`` is provided (re-onboarding an existing project), the
    user-owned section of ITERATE.md is preserved so manual edits survive, and
    any new personalization content is merged in. This keeps ``onboard``
    consistent with ``refresh`` (which also preserves user-owned sections).

    Args:
        data: OnboardingData with scan results and user inputs.
        output_dir: Directory to write files to (usually the project root).
        existing_md: Optional content of a pre-existing ITERATE.md whose
            user-owned section should be preserved. If None, the default user
            section (or personalization content) is used.

    Returns:
        Tuple of (iterate_md_path, config_yaml_path).

    Raises:
        OSError: If files cannot be written.
        ValueError: If the freshly generated ITERATE.md lacks the USER-OWNED
            markers (damaged/outdated bundled template). Writing it would
            either discard the preserved user section (splice target missing)
            or produce an ITERATE.md that ``iterate personalize`` can never
            update again — refuse before touching the filesystem instead, as
            ``generate_refreshed_md`` already does for the refresh path.
    """
    iterate_md_path = output_dir / "ITERATE.md"
    config_path = output_dir / "iterate.config.yaml"

    if existing_md is None:
        iterate_md_content = generate_iterate_md(data)
    else:
        # Re-onboarding an existing project: regenerate AI-maintained sections,
        # keep the user-owned section (manual edits), and merge in any new
        # personalization content so notes/conventions are also updated.
        fresh = generate_iterate_md(data)
        if not has_valid_user_owned_markers(existing_md):
            _warn_missing_user_markers()
        user_content = extract_user_owned_section(existing_md)
        if data.personalization is not None:
            from iterate_cli.personalize import merge_user_sections

            new_personalization_md = data.personalization.to_user_md_sections()
            user_content = merge_user_sections(user_content, new_personalization_md)
        iterate_md_content = _replace_user_owned_section(fresh, user_content)

    # Validate the OUTPUT (not just the input): a template without markers
    # silently won the splice (_replace_user_owned_section returns the content
    # unchanged when markers are absent) and the user's manual section just
    # vanished — no warning, no error, byte-identical to a "successful" run.
    if not has_valid_user_owned_markers(iterate_md_content):
        raise ValueError(
            "Generated ITERATE.md is missing the USER-OWNED section markers; "
            "refusing to write. The bundled template appears damaged or out "
            "of date — reinstall the skill, or restore "
            "<!-- ITERATE:USER-OWNED:START --> / ...END --> in "
            "templates/ITERATE.template.md and retry."
        )

    config_yaml = generate_config_yaml(data)

    # Snapshot both destinations before replacing them. Onboarding rewrites
    # ITERATE.md's AI sections and drops YAML comments, so a re-onboard must
    # always be recoverable; ``reonboard`` already did this explicitly, but
    # plain ``onboard``/``init`` reaching an existing file did not. A failed
    # backup aborts the write (no unrecoverable rewrite).
    md_backup: Path | None = None
    for destination in (iterate_md_path, config_path):
        if destination.is_file():
            try:
                backup_path = backup_file(destination, "onboard")
                if destination == iterate_md_path:
                    md_backup = backup_path
            except OSError as exc:
                raise OSError(
                    f"failed to back up {destination} before onboarding: {exc}"
                ) from exc

    atomic_write(iterate_md_path, iterate_md_content)
    try:
        atomic_write(config_path, config_yaml)
    except OSError as write_err:
        # Roll back the already-written ITERATE.md so the two files stay
        # consistent (best effort; the error is re-raised for the caller).
        # Restore the exact pre-existing content from the snapshot actually
        # taken above — the authoritative "file existed before" signal. Branch
        # on the backup (not on ``existing_md``, which a TOCTOU between the
        # caller's existence check and this write can leave stale) so a
        # just-backed-up file is never deleted instead of restored.
        try:
            if md_backup is not None:
                shutil.copy2(md_backup, iterate_md_path)
            elif iterate_md_path.exists():
                iterate_md_path.unlink()
        except OSError:
            _log_rollback_failure(iterate_md_path, write_err)
        raise

    return iterate_md_path, config_path


def extract_user_owned_section(existing_md: str) -> str:
    """Extract the user-owned section content from an existing ITERATE.md.

    Args:
        existing_md: The full content of an existing ITERATE.md file.

    Returns:
        The user-owned section content (without the marker comments).
        If markers are not found, returns the default user-owned section.
    """
    bounds = user_owned_bounds(existing_md)
    if bounds is None:
        return DEFAULT_USER_OWNED_SECTION
    start_idx, end_idx = bounds

    # Extract content between markers (after the start marker line). The
    # closing marker is the trailing one (see user_owned_bounds), so a marker
    # literal pasted inside the block cannot truncate the section.
    after_start = existing_md[start_idx + len(USER_START_MARKER):end_idx]
    return after_start.strip("\n")


def _replace_user_owned_section(content: str, new_user_content: str) -> str:
    """Replace the user-owned section in ITERATE.md content.

    Args:
        content: The full ITERATE.md content with markers.
        new_user_content: New content to place between the markers.

    Returns:
        Updated content with the user-owned section replaced.
    """
    bounds = user_owned_bounds(content)
    if bounds is None:
        return content
    start_idx, end_idx = bounds

    before = content[: start_idx + len(USER_START_MARKER)]
    after = content[end_idx:]
    if not new_user_content.strip():
        # Empty replacement must not leave a stray blank line between the
        # marker comments.
        return f"{before}\n{after}"
    return f"{before}\n{new_user_content}\n{after}"


def generate_refreshed_md(data: OnboardingData, existing_md: str) -> str:
    """Generate a refreshed ITERATE.md, preserving user-owned sections.

    This is used for incremental refresh: the AI-maintained sections are
    regenerated from new scan data, while user-owned sections are kept
    exactly as the user left them. The previous completion timestamp is
    preserved so an unchanged refresh stays a byte-for-byte no-op.

    Personalization content in the user-owned section is NOT regenerated
    during refresh — ``iterate personalize`` already keeps config.yaml
    and ITERATE.md in sync, so refresh only needs to preserve the
    existing user-owned section verbatim. To update personalization
    content in ITERATE.md, run ``iterate personalize``.

    Args:
        data: Updated OnboardingData with fresh scan results.
        existing_md: The existing ITERATE.md content to preserve user sections from.

    Returns:
        Complete refreshed ITERATE.md content.

    Raises:
        ValueError: If the existing ITERATE.md (or the generated content) is
            missing the USER-OWNED markers, so refresh refuses to overwrite
            possibly hand-edited content instead of silently discarding it.
    """
    # Locate markers in the existing file.
    existing_bounds = user_owned_bounds(existing_md)
    if existing_bounds is None:
        raise ValueError(
            "ITERATE.md is missing the USER-OWNED section markers; refusing to "
            "overwrite possibly hand-edited content. Restore the markers "
            "<!-- ITERATE:USER-OWNED:START --> / ...END --> or run "
            "`iterate reonboard` to regenerate the file."
        )
    e_start, e_end = existing_bounds

    # Generate fresh content with default user section, reusing the previous
    # completion timestamp so an unchanged refresh is a byte-for-byte no-op.
    fresh = generate_iterate_md(data, completed_at=_extract_completed_at(existing_md))

    # Preserve the user-owned block verbatim (start marker through end marker,
    # including its original blank-line layout) so an unchanged refresh is a
    # byte-for-byte no-op instead of silently rewriting whitespace.
    user_block = existing_md[e_start : e_end + len(USER_END_MARKER)]

    # Locate markers in the freshly regenerated content. user_owned_bounds
    # anchors the opening marker after the AI partition so user-supplied text
    # that embeds the marker literal in a generated AI section cannot be
    # mistaken for the real user-owned block (which would splice mid-file and
    # drop every AI section below it).
    fresh_bounds = user_owned_bounds(fresh)
    if fresh_bounds is None:
        raise ValueError(
            "Generated ITERATE.md is missing the USER-OWNED markers; "
            "refresh aborted."
        )
    f_start, f_end = fresh_bounds

    # Splice the verbatim user block into the regenerated AI-maintained parts.
    return fresh[:f_start] + user_block + fresh[f_end + len(USER_END_MARKER):]


def _render_project_overview(data: OnboardingData) -> str:
    """Render the project overview section."""
    lines: list[str] = []

    if data.project_description:
        lines.append(data.project_description)
    elif data.scan.detected_languages:
        langs = ", ".join(data.scan.detected_languages)
        lines.append(f"项目使用 {langs} 开发。")
        lines.append(f"Project developed with {langs}.")
    else:
        lines.append("（待补充 / To be filled）")
        lines.append("Project description not yet provided.")

    if data.code_conventions:
        lines.append("")
        lines.append("### 代码约定 / Code Conventions")
        lines.append("")
        lines.append(data.code_conventions)

    return "\n".join(lines)


def _render_tech_stack(data: OnboardingData) -> str:
    """Render the tech stack section."""
    scan = data.scan
    lines: list[str] = []

    if scan.detected_languages:
        lines.append("**语言 / Languages:** " + ", ".join(scan.detected_languages))
    else:
        lines.append("**语言 / Languages:** 未检测到 / None detected")

    if scan.detected_package_managers:
        lines.append("**包管理器 / Package Managers:** " + ", ".join(scan.detected_package_managers))

    if scan.manifests:
        lines.append("")
        lines.append("**Manifest 文件 / Manifest Files:**")
        for m in scan.manifests:
            lines.append(f"- `{m}`")

    if scan.has_ci:
        lines.append("")
        lines.append("**CI/CD:** 已配置 / Configured")
    else:
        lines.append("")
        lines.append("**CI/CD:** 未检测到 / Not detected")

    return "\n".join(lines)


def _render_module_map(data: OnboardingData) -> str:
    """Render the module map section."""
    scan = data.scan
    lines: list[str] = []

    if not scan.top_level_dirs:
        lines.append("（未检测到顶层目录 / No top-level directories detected）")
        return "\n".join(lines)

    lines.append("| 目录 / Directory | 用途 / Purpose |")
    lines.append("|---|---|")

    for d in scan.top_level_dirs:
        purpose = _guess_dir_purpose(d)
        lines.append(f"| `{d}/` | {purpose} |")

    if scan.has_specs:
        lines.append("")
        lines.append("**规范目录 / Specs:** 已检测到 / Detected")
    if scan.has_tests:
        lines.append("")
        lines.append("**测试目录 / Tests:** 已检测到 / Detected")

    return "\n".join(lines)


def _guess_dir_purpose(dir_name: str) -> str:
    """Guess the purpose of a top-level directory by name."""
    purpose_map = {
        "src": "源码 / Source code",
        "lib": "库代码 / Library code",
        "app": "应用入口 / Application entry",
        "api": "API 层 / API layer",
        "routes": "路由 / Routes",
        "controllers": "控制器 / Controllers",
        "handlers": "请求处理 / Request handlers",
        "server": "服务端 / Server",
        "tests": "测试 / Tests",
        "test": "测试 / Tests",
        "docs": "文档 / Documentation",
        "config": "配置 / Configuration",
        "scripts": "脚本 / Scripts",
        "tools": "工具 / Tools",
        "assets": "静态资源 / Static assets",
        "public": "公共资源 / Public assets",
        "static": "静态文件 / Static files",
        "templates": "模板 / Templates",
        "migrations": "数据库迁移 / Database migrations",
        "locales": "国际化 / Internationalization",
        "vendor": "第三方依赖 / Third-party",
        "cmd": "命令行入口 / CLI entry",
        "internal": "内部包 / Internal packages",
        "pkg": "公开包 / Public packages",
    }
    return purpose_map.get(dir_name, "其他 / Other")


def _render_dimensions(data: OnboardingData) -> str:
    """Render the recommended dimensions section."""
    if not data.dimensions:
        return "（未配置 / Not configured）"

    lines: list[str] = []
    lines.append("以下维度已启用（可在 `iterate.config.yaml` 中调整）：")
    lines.append("The following dimensions are enabled (adjustable in `iterate.config.yaml`):")
    lines.append("")

    # 与 config/dimensions.yaml 中的 priority 保持一致，修改时需同步更新。
    # Keep in sync with config/dimensions.yaml — duplicate by design to avoid
    # a runtime dependency on the dimensions yaml files.
    priority_map = {
        "correctness": "critical",
        "security": "critical",
        "performance": "high",
        "architecture": "high",
        "spec-compliance": "high",
        "frontend-backend": "high",
        "style-tests": "medium",
        "tech-debt": "medium",
        "ui-ux": "medium",
    }

    for dim in data.dimensions:
        priority = priority_map.get(dim, "medium")
        lines.append(f"- `{dim}` (priority: {priority})")

    return "\n".join(lines)


def _render_dimension_sets(data: OnboardingData) -> str:
    """Render the recommended dimension-set blueprints section.

    Each named set lists its dimensions and any scope-specific focus overrides.
    The global ``dimensions`` list above stays the default for whole-project
    review; these sets are used when a goal targets a specific scope.
    """
    if not data.dimension_sets:
        return "（未配置 / Not configured）"

    lines: list[str] = []
    lines.append("以下命名维度集可按审查范围选用（作用于 `iterate.config.yaml` 的 `dimension_sets`）：")
    lines.append("The following named dimension sets are selectable by review scope (see `dimension_sets` in `iterate.config.yaml`):")
    lines.append("")

    for name, spec in data.dimension_sets.items():
        dims = spec.get("dimensions") or []
        lines.append(f"- **`{name}`**: " + ", ".join(f"`{d}`" for d in dims))
        focus = spec.get("focus") or {}
        if focus:
            for dim, text in focus.items():
                lines.append(f"  - *{dim} focus*: {text}")

    lines.append("")
    lines.append("> 全局审查使用上方 `dimensions` 列表；指定范围内未命中以上任一律时，本轮按该范围重定义维度。")
    lines.append("> Whole-project review uses the `dimensions` list above; for an unmapped scope, dimensions are re-defined for the current run.")
    return "\n".join(lines)


def _render_iterate_notes(data: OnboardingData) -> str:
    """Render the iterate notes section."""
    notes: list[str] = []

    # Always include base notes.
    notes.append("### 通用 / General")
    notes.append("- 审查时跳过自动生成文件（dist/, build/, *.generated.*）。")
    notes.append("- 不要修改锁文件（package-lock.json, poetry.lock, Cargo.lock 等）。")
    notes.append("- 每轮修复后运行 validation.commands，失败即回滚。")
    notes.append("")

    # Add tech-stack-specific notes.
    for lang in data.scan.detected_languages:
        if lang == "Python":
            notes.append("### Python")
            notes.append("- `__init__.py` 导出变更可能影响下游模块。")
            notes.append("- 类型注解缺失不应视为原子问题。")
            notes.append("- dataclass / pydantic 字段变更属于架构问题。")
            notes.append("")
        elif lang in ("JavaScript/TypeScript", "TypeScript"):
            notes.append("### JavaScript / TypeScript")
            notes.append("- API 路由变更属于架构问题。")
            notes.append("- 组件 props 变更属于架构问题。")
            notes.append("- `any` 类型修复应结合上下文，不可盲目收窄。")
            notes.append("")
        elif lang == "Swift":
            notes.append("### Swift")
            notes.append("- `Sendable` / `@MainActor` 标注变更属于架构问题。")
            notes.append("- SwiftUI View 属性变更可能破坏调用方。")
            notes.append("- 避免修改 `*.xcodeproj` 文件。")
            notes.append("")
        elif lang == "Go":
            notes.append("### Go")
            notes.append("- 接口方法变更属于架构问题。")
            notes.append("- goroutine 泄漏是 correctness 维度重点。")
            notes.append("- `init()` 副作用变更需特别关注。")
            notes.append("")
        elif lang == "Rust":
            notes.append("### Rust")
            notes.append("- `unsafe` 块变更属于架构问题。")
            notes.append("- trait 实现变更属于架构问题。")
            notes.append("- 所有权/生命周期变更属于架构问题。")
            notes.append("")

    # Add user-provided notes if any.
    if data.iterate_notes:
        notes.append("### 用户自定义注意点 / User Custom Notes")
        notes.append(data.iterate_notes)

    return "\n".join(notes)
