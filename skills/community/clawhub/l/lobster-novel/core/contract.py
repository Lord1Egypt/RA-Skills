from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Event / Delta dataclasses
# ---------------------------------------------------------------------------


@dataclass
class ChapterCommitEvent:
    """A single narrative beat within a chapter."""

    event_type: str  # "dialogue" / "action" / "revelation" / "transition" / "emotional_beat"
    description: str
    entities_mentioned: list[str] = field(default_factory=list)
    strand: str = "quest"  # "quest" / "fire" / "constellation"


@dataclass
class StateDelta:
    """Tracked state changes produced by a chapter."""

    character_states: dict[str, str] = field(default_factory=dict)
    location: Optional[str] = None
    time_progression: Optional[str] = None
    items_changed: list[dict] = field(default_factory=list)
    relationship_changes: list[dict] = field(default_factory=list)


@dataclass
class EntityDelta:
    """New or updated entities introduced by a chapter."""

    new_characters: list[dict] = field(default_factory=list)
    new_locations: list[dict] = field(default_factory=list)
    new_items: list[dict] = field(default_factory=list)
    updated_entities: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# ChapterCommit
# ---------------------------------------------------------------------------


@dataclass
class ChapterCommit:
    """Full record of everything a chapter added, changed, or resolved."""

    chapter_number: int
    chapter_title: str
    word_count: int
    events: list[ChapterCommitEvent] = field(default_factory=list)
    state_delta: StateDelta = field(default_factory=StateDelta)
    entity_delta: EntityDelta = field(default_factory=EntityDelta)
    summary_text: str = ""
    hooks_created: list[str] = field(default_factory=list)
    hooks_resolved: list[str] = field(default_factory=list)
    strand_ratios: dict[str, float] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Recursively serialize to a plain dict suitable for JSON."""

        def _convert(obj: Any) -> Any:
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            if isinstance(obj, list):
                return [_convert(i) for i in obj]
            if isinstance(obj, dict):
                return {k: _convert(v) for k, v in obj.items()}
            return obj

        return _convert(asdict(self))

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ChapterCommit:
        """Deserialize a plain dict back into a ChapterCommit (and nested types).

        Raises ValueError if required keys are missing.
        """
        required = ["chapter_number", "chapter_title", "word_count"]
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"ChapterCommit.from_dict: missing required keys: {missing}")

        events = [ChapterCommitEvent(**e) for e in data.get("events", [])]

        sd = data.get("state_delta", {})
        state_delta = StateDelta(
            character_states=sd.get("character_states", {}),
            location=sd.get("location"),
            time_progression=sd.get("time_progression"),
            items_changed=sd.get("items_changed", []),
            relationship_changes=sd.get("relationship_changes", []),
        )

        ed = data.get("entity_delta", {})
        entity_delta = EntityDelta(
            new_characters=ed.get("new_characters", []),
            new_locations=ed.get("new_locations", []),
            new_items=ed.get("new_items", []),
            updated_entities=ed.get("updated_entities", []),
        )

        return ChapterCommit(
            chapter_number=data["chapter_number"],
            chapter_title=data["chapter_title"],
            word_count=data["word_count"],
            events=events,
            state_delta=state_delta,
            entity_delta=entity_delta,
            summary_text=data.get("summary_text", ""),
            hooks_created=data.get("hooks_created", []),
            hooks_resolved=data.get("hooks_resolved", []),
            strand_ratios=data.get("strand_ratios", {}),
            timestamp=data.get("timestamp", ""),
        )


# ---------------------------------------------------------------------------
# SeedContract  (initial novel setup)
# ---------------------------------------------------------------------------


class SeedContract:
    """Container for the initial novel setup, loaded from bible + outline."""

    def __init__(
        self,
        title: str = "",
        genre: str = "",
        style_template: str = "",
        world_settings: Optional[dict[str, Any]] = None,
        characters: Optional[dict[str, dict[str, Any]]] = None,
        plot_arcs: Optional[list[dict[str, Any]]] = None,
        rules: Optional[list[str]] = None,
        style_guidelines: Optional[list[str]] = None,
    ) -> None:
        self.title = title
        self.genre = genre
        self.style_template = style_template
        self.world_settings = world_settings or {}
        self.characters = characters or {}
        self.plot_arcs = plot_arcs or []
        self.rules = rules or []
        self.style_guidelines = style_guidelines or []

    @staticmethod
    def from_bible(bible) -> SeedContract:
        """Construct a SeedContract from a BibleManager instance.

        The *bible* object is expected to expose:
            bible.title
            bible.genre
            bible.style_template
            bible.get_world_settings()
            bible.get_characters()
            bible.get_plot_arcs()
            bible.get_rules()
            bible.get_style_guidelines()
        """
        return SeedContract(
            title=bible.title,
            genre=bible.genre,
            style_template=bible.style_template,
            world_settings=bible.get_world_settings(),
            characters=bible.get_characters(),
            plot_arcs=bible.get_plot_arcs(),
            rules=bible.get_rules(),
            style_guidelines=bible.get_style_guidelines(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "genre": self.genre,
            "style_template": self.style_template,
            "world_settings": self.world_settings,
            "characters": self.characters,
            "plot_arcs": self.plot_arcs,
            "rules": self.rules,
            "style_guidelines": self.style_guidelines,
        }


# ---------------------------------------------------------------------------
# RuntimeContract  (per-chapter guidance)
# ---------------------------------------------------------------------------


class RuntimeContract:
    """Generated before each chapter to guide the writer LLM."""

    def __init__(
        self,
        chapter_number: int = 0,
        chapter_title: str = "",
        outline_section: str = "",
        active_characters: Optional[list[str]] = None,
        active_hooks: Optional[list[dict[str, Any]]] = None,
        strand_targets: Optional[dict[str, float]] = None,
        style_constraints: Optional[list[str]] = None,
        entity_constraints: Optional[list[str]] = None,
        three_laws: Optional[list[str]] = None,
    ) -> None:
        self.chapter_number = chapter_number
        self.chapter_title = chapter_title
        self.outline_section = outline_section
        self.active_characters = active_characters or []
        self.active_hooks = active_hooks or []
        self.strand_targets = strand_targets or {}
        self.style_constraints = style_constraints or []
        self.entity_constraints = entity_constraints or []
        self.three_laws = three_laws or []

    @staticmethod
    def build(
        seed: SeedContract,
        chapter_num: int,
        recent_commits: list[ChapterCommit],
        story_state,
    ) -> RuntimeContract:
        """Construct a RuntimeContract from the seed contract, recent commit
        history, and current story state.

        Subclasses can override this method to implement custom planning
        logic; the default implementation stubs out sensible defaults from
        the seed contract.
        """
        contract = RuntimeContract(
            chapter_number=chapter_num,
            chapter_title=f"Chapter {chapter_num}",
            style_constraints=list(seed.style_guidelines),
            entity_constraints=list(seed.rules),
            three_laws=[
                "Do not kill, permanently injure, or romance a character without an explicit plot-arc directive.",
                "Do not introduce new characters, locations, or items that contradict the world settings.",
                "Do not resolve a hook before its minimum expected chapter count.",
            ],
        )
        contract.active_characters = list(seed.characters.keys())
        contract.strand_targets = _default_strand_targets()
        return contract

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter_number": self.chapter_number,
            "chapter_title": self.chapter_title,
            "outline_section": self.outline_section,
            "active_characters": self.active_characters,
            "active_hooks": self.active_hooks,
            "strand_targets": self.strand_targets,
            "style_constraints": self.style_constraints,
            "entity_constraints": self.entity_constraints,
            "three_laws": self.three_laws,
        }

    def format_writing_prompt(self) -> str:
        """Build the full writing prompt for the LLM.

        Three Laws are appended at the end of the prompt text.
        """
        lines: list[str] = []
        lines.append(f"# Chapter {self.chapter_number}: {self.chapter_title}")
        lines.append("")

        if self.outline_section:
            lines.append("## Outline Section")
            lines.append(self.outline_section)
            lines.append("")

        if self.active_characters:
            lines.append("## Active Characters")
            for cid in self.active_characters:
                lines.append(f"- {cid}")
            lines.append("")

        if self.active_hooks:
            lines.append("## Active Hooks")
            for hook in self.active_hooks:
                name = hook.get("name", hook.get("id", str(hook)))
                lines.append(f"- {name}")
            lines.append("")

        if self.strand_targets:
            lines.append("## Strand Targets")
            for strand, ratio in self.strand_targets.items():
                lines.append(f"- {strand}: {ratio:.0%}")
            lines.append("")

        if self.style_constraints:
            lines.append("## Style Constraints")
            for c in self.style_constraints:
                lines.append(f"- {c}")
            lines.append("")

        if self.entity_constraints:
            lines.append("## Entity Constraints")
            for c in self.entity_constraints:
                lines.append(f"- {c}")
            lines.append("")

        lines.append("## Guardrails — Anti-Hallucination Three Laws")
        for law in self.three_laws:
            lines.append(f"- **{law}**")
        lines.append("")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------


def _commit_path(project_dir: str, chapter_number: int) -> Path:
    return Path(project_dir) / ".commits" / f"{chapter_number:04d}.json"


def save_commit(commit: ChapterCommit, project_dir: str) -> None:
    """Persist *commit* as JSON under ``project_dir/.commits/``."""
    path = _commit_path(project_dir, commit.chapter_number)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = commit.to_dict()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_commit(chapter_number: int, project_dir: str) -> ChapterCommit:
    """Load a previously-saved commit by chapter number."""
    path = _commit_path(project_dir, chapter_number)
    data = json.loads(path.read_text(encoding="utf-8"))
    return ChapterCommit.from_dict(data)


def load_all_commits(project_dir: str) -> list[ChapterCommit]:
    """Load every commit in ``project_dir/.commits/`` sorted by chapter number."""
    commits_dir = Path(project_dir) / ".commits"
    if not commits_dir.is_dir():
        return []
    commits: list[ChapterCommit] = []
    for child in sorted(commits_dir.iterdir()):
        if child.suffix == ".json":
            data = json.loads(child.read_text(encoding="utf-8"))
            commits.append(ChapterCommit.from_dict(data))
    commits.sort(key=lambda c: c.chapter_number)
    return commits


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _default_strand_targets() -> dict[str, float]:
    """Sensible default strand distribution for an adventure/fantasy novel."""
    return {"quest": 0.40, "fire": 0.30, "constellation": 0.30}
