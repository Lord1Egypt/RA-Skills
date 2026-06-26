"""Local JSON-backed workspace state for development and tests."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.memory import (
    MemoryContext,
    MemoryRecord,
    build_profile_key,
    memory_context_from_record,
    resolve_workspace_id,
)
from intelligence_desk_brief.profiles import SavedProfile
from intelligence_desk_brief.providers.base import MemoryAdapter


class LocalWorkspaceStore:
    """File-backed workspace state used outside OpenClaw-managed memory."""

    def __init__(self, base_dir: str | Path):
        self._base_dir = Path(base_dir)

    def load_memory_record(self, workspace_id: str, profile_key: str) -> MemoryRecord | None:
        path = self._memory_record_path(workspace_id, profile_key)
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        return MemoryRecord(**payload)

    def save_memory_record(self, record: MemoryRecord) -> None:
        path = self._memory_record_path(record.workspace_id, record.profile_key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(record), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def save_profile(self, profile: SavedProfile) -> None:
        path = self._profile_path(profile.workspace_id, profile.profile_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(profile.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def load_profile(self, workspace_id: str, profile_ref: str) -> SavedProfile | None:
        direct_path = self._profile_path(workspace_id, profile_ref)
        if direct_path.exists():
            return SavedProfile.from_dict(json.loads(direct_path.read_text(encoding="utf-8")))
        for profile in self.list_profiles(workspace_id):
            if profile.profile_name == profile_ref:
                return profile
        return None

    def list_profiles(self, workspace_id: str) -> list[SavedProfile]:
        profiles_dir = self._base_dir / workspace_id / "profiles"
        if not profiles_dir.exists():
            return []
        profiles: list[SavedProfile] = []
        for path in sorted(profiles_dir.glob("*.json")):
            profiles.append(SavedProfile.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        return profiles

    def _memory_record_path(self, workspace_id: str, profile_key: str) -> Path:
        return self._base_dir / workspace_id / "brief-state" / f"{profile_key}.json"

    def _profile_path(self, workspace_id: str, profile_id: str) -> Path:
        return self._base_dir / workspace_id / "profiles" / f"{profile_id}.json"


class LocalFileMemoryAdapter(MemoryAdapter):
    """Workspace-scoped memory adapter for local development."""

    def __init__(self, base_dir: str | Path):
        self._store = LocalWorkspaceStore(base_dir)

    def recall_context(self, request: CreateBriefRequest) -> MemoryContext:
        record = self._store.load_memory_record(resolve_workspace_id(request), build_profile_key(request))
        if record is None:
            return MemoryContext(available=True, first_run=True)
        return memory_context_from_record(record)

    def store_brief(self, request: CreateBriefRequest, record: MemoryRecord) -> None:
        del request
        self._store.save_memory_record(record)
