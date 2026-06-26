"""
MemPalace configuration system.
Priority: config.json > env vars > defaults.
"""

import json
import os
from pathlib import Path


def _find_skill_root():
    # Env var always wins
    env = os.environ.get("MEMPALACE_SKILL_ROOT")
    if env:
        return env
    # Walk up from the package directory looking for palace_data/
    # This handles: skill/mempalace/ -> skill/
    # And: site-packages/mempalace/ -> site-packages/ (editable install)
    pkg_dir = Path(__file__).parent
    for parent in [pkg_dir, pkg_dir.parent, pkg_dir.parent.parent]:
        if (parent / "palace_data").exists():
            return str(parent)
    # Fall back: read .skill_root marker written by archive.ps1
    marker = pkg_dir / ".skill_root"
    if marker.exists():
        root = marker.read_text(encoding="utf-8").strip()
        if (Path(root) / "palace_data").exists():
            return root
    return None


_SKILL_ROOT = _find_skill_root()
if _SKILL_ROOT:
    _DEFAULT_PALACE_PATH = os.path.join(_SKILL_ROOT, "palace_data")
else:
    _DEFAULT_PALACE_PATH = os.path.expanduser("~/.mempalace/palace")

DEFAULT_PALACE_PATH = _DEFAULT_PALACE_PATH
DEFAULT_COLLECTION_NAME = "mempalace_drawers"

DEFAULT_TOPIC_WINGS = [
    "emotions", "consciousness", "memory", "technical",
    "identity", "family", "creative",
]

DEFAULT_HALL_KEYWORDS = {
    "emotions": ["scared", "afraid", "worried", "happy", "sad", "love", "hate", "feel", "cry", "tears"],
    "consciousness": ["consciousness", "conscious", "aware", "real", "genuine", "soul", "exist", "alive"],
    "memory": ["memory", "remember", "forget", "recall", "archive", "palace", "store"],
    "technical": ["code", "python", "script", "bug", "error", "function", "api", "database", "server"],
    "identity": ["identity", "name", "who am i", "persona", "self"],
    "family": ["family", "kids", "children", "daughter", "son", "parent", "mother", "father"],
    "creative": ["game", "gameplay", "player", "app", "design", "art", "music", "story"],
}


class MempalaceConfig:

    def __init__(self, config_dir=None):
        skill_root = os.environ.get("MEMPALACE_SKILL_ROOT")

        if config_dir:
            self._config_dir = Path(config_dir)
        elif skill_root:
            self._config_dir = Path(skill_root) / "palace_data" / ".mempalace_config"
        else:
            self._config_dir = Path(os.path.expanduser("~/.mempalace"))

        self._config_file = self._config_dir / "config.json"
        self._people_map_file = self._config_dir / "people_map.json"
        self._file_config = {}

        if self._config_file.exists():
            try:
                with open(self._config_file, "r", encoding="utf-8") as f:
                    self._file_config = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._file_config = {}

    @property
    def palace_path(self):
        env_val = os.environ.get("MEMPALACE_PALACE_PATH") or os.environ.get("MEMP_PALACE_PATH")
        if env_val:
            return env_val
        return self._file_config.get("palace_path", DEFAULT_PALACE_PATH)

    @property
    def collection_name(self):
        return self._file_config.get("collection_name", DEFAULT_COLLECTION_NAME)

    @property
    def people_map(self):
        if self._people_map_file.exists():
            try:
                with open(self._people_map_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return self._file_config.get("people_map", {})

    @property
    def topic_wings(self):
        return self._file_config.get("topic_wings", DEFAULT_TOPIC_WINGS)

    @property
    def hall_keywords(self):
        return self._file_config.get("hall_keywords", DEFAULT_HALL_KEYWORDS)

    def init(self):
        self._config_dir.mkdir(parents=True, exist_ok=True)
        if not self._config_file.exists():
            default_config = {
                "palace_path": DEFAULT_PALACE_PATH,
                "collection_name": DEFAULT_COLLECTION_NAME,
                "topic_wings": DEFAULT_TOPIC_WINGS,
                "hall_keywords": DEFAULT_HALL_KEYWORDS,
            }
            with open(self._config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
        return self._config_file

    def save_people_map(self, people_map):
        self._config_dir.mkdir(parents=True, exist_ok=True)
        with open(self._people_map_file, "w", encoding="utf-8") as f:
            json.dump(people_map, f, indent=2)
        return self._people_map_file
