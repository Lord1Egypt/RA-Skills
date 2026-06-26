from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .contract import ChapterCommit


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class CharacterState:
    """Tracks a single character's arc across the novel."""

    id: str
    name: str
    role: str = "配角"  # 主角/核心角色/配角/异客
    first_appearance: int = 0
    last_appearance: int = 0
    status: str = "coming"  # active/arriving/完成/coming
    state: str = ""
    key_items: list[str] = field(default_factory=list)


@dataclass
class ChapterRecord:
    """What happened in one chapter."""

    number: int
    title: str = ""
    word_count: int = 0
    scene: str = ""
    characters_present: list[str] = field(default_factory=list)
    key_events: list[str] = field(default_factory=list)
    strand_weights: dict[str, float] = field(default_factory=dict)


@dataclass
class HookState:
    """A planted hook that expects future payoff."""

    id: str
    description: str
    type: str = "悬念"  # 悬念/设定/物品/关系
    chapter_created: int = 0
    chapter_resolved: int | None = None
    status: str = "活跃"  # 活跃/兑现
    expected_payoff: str = ""


@dataclass
class StrandState:
    """Narrative strand balance tracking."""

    quest_ratio: float = 0.40
    fire_ratio: float = 0.30
    constellation_ratio: float = 0.30
    quest_streak: int = 0
    fire_streak: int = 0
    constellation_streak: int = 0


# ---------------------------------------------------------------------------
# StoryState  —  main aggregate
# ---------------------------------------------------------------------------


@dataclass
class StoryState:
    """Unified narrative state, persisted as story-state.json.

    ``story-state.json`` is the single source of truth.
    Backward-compatible JSON files (chapter_appearances.json,
    character_roster.json, hooks.json) are emitted on every save.
    """

    novel_title: str = ""
    volume: str = ""
    characters: dict[str, CharacterState] = field(default_factory=dict)
    chapters: dict[int, ChapterRecord] = field(default_factory=dict)
    hooks: dict[str, HookState] = field(default_factory=dict)
    strands: StrandState = field(default_factory=StrandState)
    last_commit_timestamp: str | None = None

    # -----------------------------------------------------------------------
    # Serialisation helpers
    # -----------------------------------------------------------------------

    @staticmethod
    def _path(project_dir: str | Path) -> Path:
        return Path(project_dir) / "story-state.json"

    # -----------------------------------------------------------------------
    # File I/O
    # -----------------------------------------------------------------------

    @classmethod
    def load(cls, project_dir: str | Path) -> StoryState:
        """Read ``story-state.json`` and return a StoryState instance."""
        path = cls._path(project_dir)
        if not path.exists():
            return cls()
        raw = json.loads(path.read_text(encoding="utf-8"))
        return cls._from_dict(raw)

    def save(self, project_dir: str | Path) -> None:
        """Serialise and write ``story-state.json``, plus compat files."""
        path = self._path(project_dir)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self._to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._write_compat(project_dir)

    # -----------------------------------------------------------------------
    # Apply commit
    # -----------------------------------------------------------------------

    def apply_commit(self, commit: ChapterCommit) -> None:
        """Update all state from a ChapterCommit."""
        self.novel_title = self.novel_title or ""
        self.last_commit_timestamp = commit.timestamp

        # --- chapter record ---
        scene = ""
        if commit.state_delta.location:
            scene = commit.state_delta.location
        characters_present = list(
            set(commit.state_delta.character_states.keys())
            | {e.entity for e in getattr(commit, "events", [])
               if hasattr(e, "entity") and getattr(e, "entity", None)}
        )
        characters_present.sort()

        self.chapters[commit.chapter_number] = ChapterRecord(
            number=commit.chapter_number,
            title=commit.chapter_title,
            word_count=commit.word_count,
            scene=scene,
            characters_present=characters_present,
            key_events=[e.description for e in commit.events],
            strand_weights=dict(commit.strand_ratios),
        )

        # --- characters ---
        self._update_characters(commit)

        # --- hooks ---
        self._update_hooks(commit)

        # --- strands ---
        self.update_strands(commit)



    def _update_characters(self, commit: ChapterCommit) -> None:
        seen: set[str] = set()

        for char_dict in commit.entity_delta.new_characters:
            cid = char_dict.get("id", char_dict.get("name", ""))
            if not cid:
                continue
            name = char_dict.get("name", cid)
            seen.add(cid)
            if cid not in self.characters:
                role = char_dict.get("role", "配角")
                self.characters[cid] = CharacterState(
                    id=cid,
                    name=name,
                    role=role,
                    first_appearance=commit.chapter_number,
                    last_appearance=commit.chapter_number,
                    status=role_map_to_status(role),
                    state=char_dict.get("description", ""),
                    key_items=char_dict.get("key_items", []),
                )
            else:
                ch = self.characters[cid]
                ch.last_appearance = max(ch.last_appearance, commit.chapter_number)
                ch.state = char_dict.get("description", ch.state)
                if char_dict.get("key_items"):
                    ch.key_items = list(
                        dict.fromkeys(ch.key_items + char_dict["key_items"])
                    )

        # Touch characters mentioned in state_delta.character_states
        for cid, cstate in commit.state_delta.character_states.items():
            if cid in seen:
                # Already processed via entity_delta.new_characters — skip
                continue
            seen.add(cid)
            if cid in self.characters:
                ch = self.characters[cid]
                ch.last_appearance = max(ch.last_appearance, commit.chapter_number)
                ch.state = cstate or ch.state
            else:
                self.characters[cid] = CharacterState(
                    id=cid,
                    name=cid,
                    role="配角",
                    first_appearance=commit.chapter_number,
                    last_appearance=commit.chapter_number,
                    status="active",
                    state=cstate,
                )

        # Update last_appearance for all existing characters in characters_present
        record = self.chapters.get(commit.chapter_number)
        if record:
            for cname in record.characters_present:
                for cid, ch in self.characters.items():
                    if ch.name == cname or cid == cname:
                        ch.last_appearance = max(ch.last_appearance, commit.chapter_number)

    def _update_hooks(self, commit: ChapterCommit) -> None:
        for h_desc in commit.hooks_created:
            hid = _hook_id(h_desc, commit.chapter_number)
            if hid not in self.hooks:
                self.hooks[hid] = HookState(
                    id=hid,
                    description=h_desc,
                    chapter_created=commit.chapter_number,
                )

        for h_desc in commit.hooks_resolved:
            for hid, hook in list(self.hooks.items()):
                if hook.status != "活跃":
                    continue
                # Fuzzy match: substring or containment
                if (hook.description == h_desc
                        or (len(h_desc) > 10 and hook.description in h_desc)
                        or (len(hook.description) > 10 and h_desc in hook.description)):
                    hook.status = "兑现"
                    hook.chapter_resolved = commit.chapter_number
                    break

    def update_strands(self, commit: ChapterCommit) -> None:
        """Update strand ratios and streaks from a commit."""
        ratios = commit.strand_ratios
        if ratios:
            self.strands.quest_ratio = ratios.get("quest", self.strands.quest_ratio)
            self.strands.fire_ratio = ratios.get("fire", self.strands.fire_ratio)
            self.strands.constellation_ratio = ratios.get(
                "constellation", self.strands.constellation_ratio
            )

        # Determine dominant strand for this chapter
        dominant = max(
            {"quest": self.strands.quest_ratio,
             "fire": self.strands.fire_ratio,
             "constellation": self.strands.constellation_ratio},
            key=lambda k: getattr(self.strands, f"{k}_ratio"),
        )

        # Reset streak for dominant, increment others
        streaks = {"quest": "quest_streak", "fire": "fire_streak",
                   "constellation": "constellation_streak"}
        for strand, attr in streaks.items():
            if strand == dominant:
                setattr(self.strands, attr, 0)
            else:
                setattr(self.strands, attr, getattr(self.strands, attr) + 1)

    # -----------------------------------------------------------------------
    # Query helpers
    # -----------------------------------------------------------------------

    def get_active_hooks(self) -> list[HookState]:
        """Return all unresolved hooks."""
        return [h for h in self.hooks.values() if h.status == "活跃"]

    def get_overdue_hooks(self, chapters_threshold: int = 15) -> list[HookState]:
        """Return hooks that haven't been resolved within *chapters_threshold*
        chapters of creation."""
        overdue: list[HookState] = []
        for hook in self.hooks.values():
            if hook.status != "活跃":
                continue
            age = max(self.chapters.keys(), default=hook.chapter_created) - hook.chapter_created
            if age >= chapters_threshold:
                overdue.append(hook)
        return overdue

    # -----------------------------------------------------------------------
    # Backward-compatible JSON output
    # -----------------------------------------------------------------------

    def to_json_compat(self) -> dict:
        """Build the old ``chapter_appearances.json`` format as a dict.

        Returns a list of per-chapter appearance records.
        """
        chapters_list: list[dict[str, Any]] = []
        for num in sorted(self.chapters):
            rec = self.chapters[num]
            characters_present = rec.characters_present[:]
            # Add any new characters whose first_appearance == this chapter
            new_chars = [
                c.name for c in self.characters.values()
                if c.first_appearance == num
            ]
            chapters_list.append({
                "chapter": num,
                "chapter_display": f"V{self.volume}Ch{num:03d}" if self.volume else str(num),
                "characters": characters_present,
                "new_characters": new_chars,
                "total_crowd": len(characters_present),
                "scene": rec.scene,
                "key_events": rec.key_events,
            })
        return {"chapters": chapters_list}

    def _write_compat(self, project_dir: str | Path) -> None:
        """Write backward-compatible JSON files to project root."""
        root = Path(project_dir)
        root.mkdir(parents=True, exist_ok=True)

        # chapter_appearances.json  (list format)
        compat_appearances = self.to_json_compat()
        (root / "chapter_appearances.json").write_text(
            json.dumps(compat_appearances.get("chapters", compat_appearances),
                       ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # character_roster.json  (dict of id → roster-entry)
        roster: dict[str, Any] = {}
        for cid, ch in self.characters.items():
            roster[cid] = {
                "id": ch.id,
                "name": ch.name,
                "role": ch.role,
                "first_appearance": ch.first_appearance,
                "last_appearance": ch.last_appearance,
                "status": ch.status,
                "state": ch.state,
                "key_items": ch.key_items,
            }
        (root / "character_roster.json").write_text(
            json.dumps(roster, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # hooks.json  (list format)
        hooks_list: list[dict[str, Any]] = []
        for hid, hook in self.hooks.items():
            hooks_list.append({
                "id": hook.id,
                "description": hook.description,
                "type": hook.type,
                "chapter_created": hook.chapter_created,
                "chapter_resolved": hook.chapter_resolved,
                "status": hook.status,
                "expected_payoff": hook.expected_payoff,
            })
        (root / "hooks.json").write_text(
            json.dumps(hooks_list, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # -----------------------------------------------------------------------
    # Internal serialisation
    # -----------------------------------------------------------------------

    def _to_dict(self) -> dict[str, Any]:
        return {
            "novel_title": self.novel_title,
            "volume": self.volume,
            "last_commit_timestamp": self.last_commit_timestamp,
            "strands": {
                "quest_ratio": self.strands.quest_ratio,
                "fire_ratio": self.strands.fire_ratio,
                "constellation_ratio": self.strands.constellation_ratio,
                "quest_streak": self.strands.quest_streak,
                "fire_streak": self.strands.fire_streak,
                "constellation_streak": self.strands.constellation_streak,
            },
            "characters": {
                cid: {
                    "id": ch.id,
                    "name": ch.name,
                    "role": ch.role,
                    "first_appearance": ch.first_appearance,
                    "last_appearance": ch.last_appearance,
                    "status": ch.status,
                    "state": ch.state,
                    "key_items": ch.key_items,
                }
                for cid, ch in self.characters.items()
            },
            "chapters": {
                str(num): {
                    "number": rec.number,
                    "title": rec.title,
                    "word_count": rec.word_count,
                    "scene": rec.scene,
                    "characters_present": rec.characters_present,
                    "key_events": rec.key_events,
                    "strand_weights": rec.strand_weights,
                }
                for num, rec in self.chapters.items()
            },
            "hooks": {
                hid: {
                    "id": hook.id,
                    "description": hook.description,
                    "type": hook.type,
                    "chapter_created": hook.chapter_created,
                    "chapter_resolved": hook.chapter_resolved,
                    "status": hook.status,
                    "expected_payoff": hook.expected_payoff,
                }
                for hid, hook in self.hooks.items()
            },
        }

    @classmethod
    def _from_dict(cls, raw: dict[str, Any]) -> StoryState:
        strands_raw = raw.get("strands", {})
        strands = StrandState(
            quest_ratio=strands_raw.get("quest_ratio", 0.40),
            fire_ratio=strands_raw.get("fire_ratio", 0.30),
            constellation_ratio=strands_raw.get("constellation_ratio", 0.30),
            quest_streak=strands_raw.get("quest_streak", 0),
            fire_streak=strands_raw.get("fire_streak", 0),
            constellation_streak=strands_raw.get("constellation_streak", 0),
        )

        characters: dict[str, CharacterState] = {}
        for cid, cd in raw.get("characters", {}).items():
            characters[cid] = CharacterState(
                id=cd.get("id", cid),
                name=cd.get("name", cid),
                role=cd.get("role", "配角"),
                first_appearance=cd.get("first_appearance", 0),
                last_appearance=cd.get("last_appearance", 0),
                status=cd.get("status", "coming"),
                state=cd.get("state", ""),
                key_items=cd.get("key_items", []),
            )

        chapters: dict[int, ChapterRecord] = {}
        for sk, cd in raw.get("chapters", {}).items():
            num = int(sk)
            chapters[num] = ChapterRecord(
                number=num,
                title=cd.get("title", ""),
                word_count=cd.get("word_count", 0),
                scene=cd.get("scene", ""),
                characters_present=cd.get("characters_present", []),
                key_events=cd.get("key_events", []),
                strand_weights=cd.get("strand_weights", {}),
            )

        hooks: dict[str, HookState] = {}
        for hid, hd in raw.get("hooks", {}).items():
            hooks[hid] = HookState(
                id=hd.get("id", hid),
                description=hd.get("description", ""),
                type=hd.get("type", "悬念"),
                chapter_created=hd.get("chapter_created", 0),
                chapter_resolved=hd.get("chapter_resolved"),
                status=hd.get("status", "活跃"),
                expected_payoff=hd.get("expected_payoff", ""),
            )

        return cls(
            novel_title=raw.get("novel_title", ""),
            volume=raw.get("volume", ""),
            characters=characters,
            chapters=chapters,
            hooks=hooks,
            strands=strands,
            last_commit_timestamp=raw.get("last_commit_timestamp"),
        )


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


def role_map_to_status(role: str) -> str:
    """Map a Chinese role string to an initial status."""
    mapping = {
        "主角": "active",
        "核心角色": "active",
        "配角": "arriving",
        "异客": "coming",
    }
    return mapping.get(role, "coming")


_hook_counter: int = 0


def _hook_id(description: str, chapter_number: int) -> str:
    """Generate a deterministic-ish hook ID."""
    global _hook_counter
    _hook_counter += 1
    # Use first 4 chars of description as a short key
    prefix = "".join(c for c in description[:4] if c.isalpha() or c.isdigit())
    return f"h{chapter_number}-{prefix or str(_hook_counter)}"
