"""对话式引导主入口"""

from music_studio import config
from music_studio.conversation import session, flows
from music_studio.session_manager import manager as sm


CANCEL_WORDS = ["取消", "算了", "退出", "不做了", "退出音乐工作室"]

# 在任意 step 都优先拦截的 meta 命令（在 flow 之前处理）
META_COMMANDS = ["上一步", "返回", "back", "会话历史", "历史记录", "6"]


def handle(message: str):
    msg = message.strip()

    # 退出
    if any(w in msg for w in CANCEL_WORDS):
        sm.clear_active()
        return "好的，已退出音乐工作室。有需要再说～"

    # ── 激活状态 ──────────────────────────────────────────
    if session.is_active():
        state_val, data = session.get_state()
        params = data.get("params", {})

        # setup 流程优先
        if state_val == session.State.SETUP.value:
            sm.append_message(data["id"], "user", msg)
            reply = flows.setup_flow(msg, data)
            if reply:
                sm.append_message(data["id"], "assistant", reply)
            return reply

        # Meta 命令：在任意 step 都优先拦截
        if msg in ("上一步", "返回", "back"):
            reply = flows._go_back(data)
            sm.append_message(data["id"], "user", msg)
            sm.append_message(data["id"], "assistant", reply)
            return reply

        if msg in ("会话历史", "历史记录", "6"):
            reply = flows.show_session_history(data)
            sm.append_message(data["id"], "user", msg)
            sm.append_message(data["id"], "assistant", reply)
            return reply

        # 数字序号恢复会话：仅在明确等待选择时生效
        if msg.isdigit() and params.get("awaiting_session_pick"):
            reply = flows.resume_session_pick(msg, data)
            sm.append_message(data["id"], "user", msg)
            sm.append_message(data["id"], "assistant", reply)
            return reply

        # DONE 状态
        if state_val == session.State.DONE.value:
            reply = flows.done_flow(msg, data)
            if reply:
                sm.append_message(data["id"], "user", msg)
                sm.append_message(data["id"], "assistant", reply)
            return reply

        # 记录用户消息
        sm.append_message(data["id"], "user", msg)

        # 路由到各 flow
        if state_val == session.State.MUSIC.value:
            reply = flows.music_flow(msg, data)
        elif state_val == session.State.LYRICS.value:
            reply = flows.lyrics_flow(msg, data)
        elif state_val == session.State.COVER.value:
            reply = flows.cover_flow(msg, data)
        else:
            sm.clear_active()
            return "会话异常，已重置。请再说「打开音乐工作室」。"

        if reply:
            sm.append_message(data["id"], "assistant", reply)
        return reply

    # ── 未激活：只有明确唤醒才进入 ────────────────────────
    triggers = ["打开音乐工作室", "音乐工作室", "进入音乐工作室",
                "music studio", "music-studio", "我要做音乐",
                "我要写歌词", "我要翻唱"]
    if not any(t in msg for t in triggers):
        return None  # 不走 music-studio 流程

    # ── 新会话，每次都是新的 ─────────────────────────────
    new_session = sm.create_session(s_type="music")

    if not config.is_ready():
        session.begin(session.State.SETUP.value, {"source": "open_music_studio"})
        reply = flows.setup_welcome()
        sm.append_message(new_session["id"], "assistant", reply)
        return reply

    session.begin(session.State.MUSIC.value, {})
    sm.append_message(new_session["id"], "assistant", flows.MENU.strip())
    return flows.MENU.strip()


def list_sessions() -> list[dict]:
    """返回最近会话列表（供外部调用）"""
    return sm.list_sessions(limit=20)


def get_session_history(sid: str) -> dict:
    """读取指定会话的完整消息历史"""
    return sm.get_session(sid)


def resume(sid: str) -> str:
    """恢复指定会话到活跃状态"""
    s = sm.resume_session(sid)
    state_val = s.get("state", session.State.MUSIC.value)
    step = s.get("step", 0)
    params = s.get("params", {})
    session.restore_state(state_val, step, params)
    return flows.render_restored_session(s)
