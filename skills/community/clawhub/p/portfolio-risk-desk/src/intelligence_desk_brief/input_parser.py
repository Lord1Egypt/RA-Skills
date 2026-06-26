"""Input parsing helpers for the local runtime."""

from __future__ import annotations

import json
from pathlib import Path

from intelligence_desk_brief.contracts import CreateBriefRequest, DeliveryTarget
from intelligence_desk_brief.fixtures import load_demo_request_payload
from intelligence_desk_brief.providers.local_state import LocalWorkspaceStore


def load_request_from_file(path: str) -> CreateBriefRequest:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return CreateBriefRequest.from_dict(payload)


def load_fixture_request() -> CreateBriefRequest:
    return CreateBriefRequest.from_dict(load_demo_request_payload())


def load_request_from_saved_profile(
    state_dir: str,
    *,
    workspace_id: str,
    profile_ref: str,
    delivery_target: DeliveryTarget,
) -> CreateBriefRequest:
    store = LocalWorkspaceStore(state_dir)
    profile = store.load_profile(workspace_id, profile_ref)
    if profile is None:
        raise FileNotFoundError(
            f"No saved profile '{profile_ref}' was found in workspace '{workspace_id}'."
        )
    return profile.to_request(delivery_target=delivery_target)
