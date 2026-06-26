import json
import os
import tempfile
import time
import uuid
from pathlib import Path


def get_runtime_dir():
    configured = os.getenv("MUMU_RUNTIME_DIR")
    if configured:
        return Path(configured).expanduser()
    return Path(__file__).resolve().parents[1] / ".mumu_runtime"


def get_state_path(project_id):
    return get_runtime_dir() / f"{project_id}.json"


def get_owner_id():
    return os.getenv("MUMU_OWNER_ID") or "default-owner"


def new_runner_id():
    return str(uuid.uuid4())


def load_state(project_id):
    path = get_state_path(project_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def save_state(project_id, payload):
    path = get_state_path(project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = dict(payload)
    data.setdefault("project_id", project_id)
    data.setdefault("owner_id", get_owner_id())
    data.setdefault("runner_id", new_runner_id())
    data.setdefault("updated_at", time.time())
    fd, tmp_path = tempfile.mkstemp(prefix=path.name, dir=str(path.parent))
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(data, handle, ensure_ascii=False)
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
    return data


def clear_state(project_id):
    path = get_state_path(project_id)
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def is_stale(state, stale_after_seconds=300):
    if not state:
        return True
    updated_at = state.get("updated_at")
    if not updated_at:
        return True
    return (time.time() - float(updated_at)) > stale_after_seconds
