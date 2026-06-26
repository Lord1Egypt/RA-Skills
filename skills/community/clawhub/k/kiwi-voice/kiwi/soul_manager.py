"""Soul manager — dynamic personality switching for Kiwi Voice.

Souls are markdown files in kiwi/souls/ that define personality traits.
The SoulManager composes the full system prompt by combining the base
Kiwi context (capabilities, voice rules) with the active soul's personality.
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from kiwi import PROJECT_ROOT
from kiwi.utils import kiwi_log


@dataclass
class SoulConfig:
    """Configuration for a single soul."""
    id: str                          # Filename without .md, e.g. "storyteller"
    name: str                        # Display name from H1 header
    description: str                 # First paragraph after header
    prompt: str                      # Full soul prompt text (markdown body)
    model: Optional[str] = None      # LLM model hint (informational, displayed in UI)
    session: Optional[str] = None    # OpenClaw session ID override (None = default)
    nsfw: bool = False               # Whether this is NSFW mode


class SoulManager:
    """Manages soul loading, switching, and system prompt composition."""

    def __init__(self, souls_dir: Optional[str] = None, default_soul: str = "mindful-companion"):
        self._souls_dir = souls_dir or os.path.join(PROJECT_ROOT, "kiwi", "souls")
        self._souls: Dict[str, SoulConfig] = {}
        self._active_soul_id: str = default_soul
        self._default_soul_id: str = default_soul

        # Model overrides per soul (configured externally)
        self._model_overrides: Dict[str, str] = {}

        # NSFW soul IDs (configured externally)
        self._nsfw_souls: set = set()

        self._load_souls()

    def _load_souls(self):
        """Load all .md files from the souls directory."""
        if not os.path.isdir(self._souls_dir):
            kiwi_log("SOUL", f"Souls directory not found: {self._souls_dir}", level="WARNING")
            return

        for fname in sorted(os.listdir(self._souls_dir)):
            if not fname.endswith(".md"):
                continue
            soul_id = fname[:-3]  # strip .md
            filepath = os.path.join(self._souls_dir, fname)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                soul = self._parse_soul(soul_id, content)

                # Apply external overrides
                if soul_id in self._model_overrides:
                    soul.model = self._model_overrides[soul_id]
                if soul_id in self._nsfw_souls:
                    soul.nsfw = True

                self._souls[soul_id] = soul
                kiwi_log("SOUL", f"Loaded soul: {soul.name} ({soul_id})", level="INFO")
            except Exception as e:
                kiwi_log("SOUL", f"Error loading soul {fname}: {e}", level="ERROR")

        if not self._souls:
            kiwi_log("SOUL", "No souls loaded, using empty personality", level="WARNING")

        # Validate default soul exists
        if self._active_soul_id not in self._souls and self._souls:
            first = next(iter(self._souls))
            kiwi_log("SOUL", f"Default soul '{self._active_soul_id}' not found, using '{first}'", level="WARNING")
            self._active_soul_id = first

    def _parse_soul(self, soul_id: str, content: str) -> SoulConfig:
        """Parse a soul markdown file into SoulConfig."""
        lines = content.strip().split("\n")

        # Extract name from first H1 header
        name = soul_id.replace("-", " ").title()
        description = ""
        body_start = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("# "):
                name = stripped[2:].strip()
                body_start = i + 1
                break

        # Extract description: first non-empty line after header (often italic)
        for i in range(body_start, min(body_start + 5, len(lines))):
            stripped = lines[i].strip()
            if stripped and stripped != "---":
                # Remove markdown italic markers
                description = stripped.strip("_*").strip()
                break

        # Full prompt is the entire content
        prompt = content.strip()

        # Auto-detect NSFW from filename or content
        nsfw = soul_id in ("nsfw", "18+", "adult", "siren")

        return SoulConfig(
            id=soul_id,
            name=name,
            description=description,
            prompt=prompt,
            model=None,
            nsfw=nsfw,
        )

    def configure(self, default_soul: str = "",
                  model_overrides: Optional[Dict[str, str]] = None,
                  session_overrides: Optional[Dict[str, str]] = None,
                  nsfw_souls: Optional[List[str]] = None):
        """Apply external configuration (from config.yaml).

        Args:
            default_soul: Default soul ID
            model_overrides: {soul_id: model_name} — informational, shown in UI
            session_overrides: {soul_id: openclaw_session_id} — actual LLM switching
            nsfw_souls: List of soul IDs marked as NSFW
        """
        if default_soul and default_soul in self._souls:
            self._default_soul_id = default_soul
            if self._active_soul_id == self._default_soul_id or self._active_soul_id not in self._souls:
                self._active_soul_id = default_soul

        if model_overrides:
            self._model_overrides = model_overrides
            for soul_id, model in model_overrides.items():
                if soul_id in self._souls:
                    self._souls[soul_id].model = model

        if session_overrides:
            for soul_id, session in session_overrides.items():
                if soul_id in self._souls:
                    self._souls[soul_id].session = session

        if nsfw_souls:
            self._nsfw_souls = set(nsfw_souls)
            for soul_id in nsfw_souls:
                if soul_id in self._souls:
                    self._souls[soul_id].nsfw = True

    @property
    def active_soul_id(self) -> str:
        return self._active_soul_id

    def list_souls(self) -> List[SoulConfig]:
        """Return all loaded souls."""
        return list(self._souls.values())

    def get_soul(self, soul_id: str) -> Optional[SoulConfig]:
        """Get a specific soul by ID."""
        return self._souls.get(soul_id)

    def get_active_soul(self) -> Optional[SoulConfig]:
        """Get the currently active soul."""
        return self._souls.get(self._active_soul_id)

    def switch_soul(self, soul_id: str) -> bool:
        """Switch to a different soul. Returns True if successful."""
        if soul_id not in self._souls:
            kiwi_log("SOUL", f"Soul not found: {soul_id}", level="WARNING")
            return False

        old = self._active_soul_id
        self._active_soul_id = soul_id
        soul = self._souls[soul_id]
        kiwi_log("SOUL", f"Switched soul: {old} -> {soul_id} ({soul.name})", level="INFO")
        return True

    def switch_to_default(self) -> bool:
        """Switch back to the default soul."""
        return self.switch_soul(self._default_soul_id)

    def get_system_prompt(self, base_context: str = "") -> str:
        """Compose full system prompt: base Kiwi context + active soul personality.

        Args:
            base_context: The base Kiwi voice context (capabilities, voice rules).
                          If empty, only the soul personality is returned.

        Returns:
            Composed system prompt string.
        """
        soul = self.get_active_soul()
        if not soul:
            return base_context

        if base_context:
            return f"{base_context}\n\n---\n\n{soul.prompt}"
        return soul.prompt

    def get_model_override(self) -> Optional[str]:
        """Return model hint for the active soul, or None for default (informational)."""
        soul = self.get_active_soul()
        if soul and soul.model:
            return soul.model
        return None

    def get_session_override(self) -> Optional[str]:
        """Return OpenClaw session ID override for the active soul, or None for default."""
        soul = self.get_active_soul()
        if soul and soul.session:
            return soul.session
        return None

    def is_nsfw_active(self) -> bool:
        """Check if the active soul is NSFW."""
        soul = self.get_active_soul()
        return soul.nsfw if soul else False

    def find_soul_by_name(self, query: str) -> Optional[str]:
        """Find soul ID by partial name match (for voice commands)."""
        query_lower = query.lower().strip()
        # Exact match first
        if query_lower in self._souls:
            return query_lower
        # Name match
        for soul_id, soul in self._souls.items():
            if query_lower == soul.name.lower():
                return soul_id
        # Partial match
        for soul_id, soul in self._souls.items():
            if query_lower in soul_id or query_lower in soul.name.lower():
                return soul_id
        return None

    def get_soul_info(self) -> Dict:
        """Return serializable info about all souls and current state."""
        return {
            "active": self._active_soul_id,
            "default": self._default_soul_id,
            "nsfw_active": self.is_nsfw_active(),
            "souls": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "model": s.model,
                    "session": s.session,
                    "nsfw": s.nsfw,
                    "active": s.id == self._active_soul_id,
                }
                for s in self._souls.values()
            ],
        }
