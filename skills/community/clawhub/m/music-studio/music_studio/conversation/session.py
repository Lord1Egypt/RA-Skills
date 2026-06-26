"""会话状态管理（对话流程级，委托 session_manager 存储）"""

from enum import Enum
from typing import Any, Optional

from music_studio import config
from music_studio.session_manager import manager as sm


SESSION_FILE = lambda: config.get_output_dir() / ".session.json"


class State(Enum):
    IDLE = "idle"
    SETUP = "setup"
    MUSIC = "music"
    LYRICS = "lyrics"
    COVER = "cover"
    DONE = "done"


def get_state() -> tuple[str, dict[str, Any]]:
    session = sm.get_active()
    if not session:
        return State.IDLE.value, {}
    return session.get("state", State.IDLE.value), session


def begin(state: str, context: dict[str, Any] | None = None) -> None:
    session = sm.get_active()
    if not session:
        session = sm.create_session(s_type=state)
    else:
        # 已有活跃会话，更新状态
        sm.update_session_state(session["id"], state, 0, context or {})
        sm._set_active(session["id"])


def restore_state(state: str, step: int, context: dict[str, Any] | None = None) -> None:
    session = sm.get_active()
    if not session:
        return
    sm.update_session_state(session["id"], state, step, context or session.get("params", {}))
    sm._set_active(session["id"])


def update(params: dict[str, Any], step: int | None = None,
           prev_params: dict[str, Any] | None = None) -> None:
    session = sm.get_active()
    if not session:
        return
    sid = session["id"]

    if prev_params is not None:
        sm.update_session_state(sid, session.get("state", State.IDLE.value),
                               step or session.get("step", 0),
                               {**session.get("params", {}), **params,
                                "prev_params": prev_params})
        return

    if step is not None and step != session.get("step"):
        prev = {
            "state": session.get("state"),
            "step": session.get("step"),
            "params": dict(session.get("params", {})),
        }
        current_params = {**session.get("params", {}), **params, "prev_params": prev}
    else:
        current_params = {**session.get("params", {}), **params}

    sm.update_session_state(sid, session.get("state", State.IDLE.value),
                            step if step is not None else session.get("step", 0),
                            current_params)


def set_state(state: str, step: int | None = None) -> None:
    session = sm.get_active()
    if not session:
        return
    sid = session["id"]
    current = session.get("params", {})

    if step is not None and step != session.get("step"):
        prev = {
            "state": session.get("state"),
            "step": session.get("step"),
            "params": dict(current),
        }
        current = {**current, "prev_params": prev}

    sm.update_session_state(sid, state,
                            step if step is not None else session.get("step", 0),
                            current)


def end() -> None:
    """结束当前会话（不清除数据，只清除活跃标记）"""
    sm.clear_active()


def is_active() -> bool:
    return sm.get_active_id() is not None


def get_prev(data: dict[str, Any]) -> Optional[dict[str, Any]]:
    return data.get("params", {}).get("prev_params")
