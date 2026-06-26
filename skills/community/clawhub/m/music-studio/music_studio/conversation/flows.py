"""各业务方向的引导流程（全部直调 API，不走 CLI subprocess）"""

import re
import time
import uuid
import urllib.request
from pathlib import Path

from music_studio import config, providers, library as lib_mod
from music_studio.conversation import session
from music_studio.session_manager import manager as sm

MENU = """
🎵 **音乐工作室** 已就绪！

请问想做什么？

    1️⃣  生成音乐
    2️⃣  写歌词
    3️⃣  翻唱（基于参考音频）
    4️⃣  查看音乐库
    5️⃣  导出 / 清理
    6️⃣  会话历史

直接说选项数字或名称即可，例如「1」或「生成音乐」。
"""

SETUP_WELCOME = """
🎵 检测到这是第一次使用，或当前配置还没完成。

先做个快速初始化吧：
1) 设置 MiniMax API Key
2) 确认默认模型
3) 然后直接进入音乐工作室

请回复：
A) 手动输入 API Key
B) 取消
""".strip()


# ── setup flow ────────────────────────────────────────────

def setup_welcome() -> str:
    return SETUP_WELCOME


def setup_flow(msg, data):
    step = data.get("step", 0)
    params = data.get("params", {})
    raw = msg.strip()
    upper = raw.upper()

    if raw in ("取消", "退出", "C"):
        session.end()
        return "好的，已退出初始化。有需要再说「打开音乐工作室」。"

    if step == 0:
        if upper == "A":
            session.update({}, step=1)
            return "请输入 MiniMax API Key："

        if upper == "B":
            session.end()
            return "好的，已退出初始化。有需要再说「打开音乐工作室」。"

        return SETUP_WELCOME

    if step == 1:
        api_key = raw
        if not api_key:
            return "API Key 不能为空，请重新输入。"
        ok, detail = _validate_api_key(api_key)
        if not ok:
            return f"❌ API Key 校验失败：{detail}\n请重新输入，或回复 B 取消。"
        config.save_config({
            "provider": "minimax",
            "music_model": "music-2.6",
            "cover_model": "music-cover",
            "api_key": api_key,
        })
        session.set_state(session.State.MUSIC.value, step=0)
        return "✅ 初始化完成，已保存配置。\n\n" + MENU.strip()

    return SETUP_WELCOME


# ── 歌词元信息解析 ─────────────────────────────────────────

def _parse_lyrics_meta(text: str):
    style = None
    title = None

    m = re.search(r"style\s*[：:]\s*([^\n]+)", text, re.IGNORECASE)
    if m:
        style = m.group(1).strip().rstrip(",;，；")
        text = text[:m.start()] + text[m.end():]

    m = re.search(r"title\s*[：:]\s*([^\n]+)", text, re.IGNORECASE)
    if m:
        title = m.group(1).strip().rstrip(",;，；")
        text = text[:m.start()] + text[m.end():]

    clean = re.sub(r"\n{3,}", "\n\n", text.strip())
    return clean, style, title


# ── 工具函数 ───────────────────────────────────────────────

def _with_retry(fn, max_attempts=3, initial_delay=5):
    def wrapper(*args, **kwargs):
        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                is_timeout = "timeout" in err_str or "timed out" in err_str
                if is_timeout and attempt < max_attempts:
                    time.sleep(initial_delay * attempt)
                    continue
                break
        raise last_error
    return wrapper


def _validate_api_key(api_key: str) -> tuple[bool, str]:
    try:
        client = providers.get_api_client(api_key, "minimax")
        resp = client.lyrics_generation(prompt="test")
        client.raise_on_error(resp)
        return True, "ok"
    except Exception as e:
        return False, str(e)


def _get_client():
    return providers.get_api_client(
        config.get_api_key(),
        config.get_provider(),
    )


def _call_with_retry(fn, label="生成"):
    last_err = None
    for attempt in range(1, 4):
        try:
            return fn()
        except Exception as e:
            last_err = e
            err = str(e).lower()
            is_temp = "timeout" in err or "timed out" in err or "connection" in err
            if is_temp and attempt < 3:
                time.sleep(5 * attempt)
                continue
            break
    raise last_err


def _download_url(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _sanitize_filename(name: str, fallback: str = "output") -> str:
    safe = (name or fallback).replace("/", "_").replace("\\", "_").strip()
    return safe or fallback


def _save_audio_from_url(title: str, audio_url: str) -> tuple[str | None, str | None]:
    try:
        data_bytes = _download_url(audio_url)
        mp3_path = lib_mod.OUTPUT_DIR() / f"{_sanitize_filename(title, 'music')}.mp3"
        mp3_path.write_bytes(data_bytes)
        return str(mp3_path), None
    except Exception as e:
        return None, str(e)


def _build_media_lines(paths) -> str:
    lines = []
    seen = set()
    for p in paths:
        if not p:
            continue
        s = str(p)
        if s in seen:
            continue
        seen.add(s)
        lines.append(f"MEDIA:{s}")
    return "\n".join(lines)


def _write_text_file(path: Path, content: str) -> str:
    path.write_text(content)
    return str(path)


def _write_meta_file(base_name: str, lines: list[str]) -> str:
    meta_path = lib_mod.OUTPUT_DIR() / f"{base_name}.meta.txt"
    meta_path.write_text("\n".join(lines).strip() + "\n")
    return str(meta_path)


def _prepare_music_assets(*, out_id: str, title: str, entry_type: str, prompt: str,
                          audio_url: str, provider: str, model: str,
                          reference_url: str = "", lyrics_text: str = "") -> dict:
    safe = _sanitize_filename(title, entry_type)
    url_path = _write_text_file(lib_mod.OUTPUT_DIR() / f"{safe}.url", audio_url + "\n")
    meta_lines = [
        f"id: {out_id}",
        f"title: {title}",
        f"type: {entry_type}",
        f"provider: {provider}",
        f"model: {model}",
        f"prompt: {prompt}",
        f"created: {lib_mod._now()}",
        f"audio_url: {audio_url}",
    ]
    if reference_url:
        meta_lines.append(f"reference_url: {reference_url}")
    if lyrics_text:
        lyrics_path = _write_text_file(lib_mod.OUTPUT_DIR() / f"{safe}.lyrics.txt", lyrics_text)
        meta_lines.append(f"lyrics_path: {lyrics_path}")
    else:
        lyrics_path = ""
    meta_path = _write_meta_file(safe, meta_lines)
    local_path, dl_err = _save_audio_from_url(title, audio_url)
    return {
        "url_path": url_path,
        "meta_path": meta_path,
        "lyrics_path": lyrics_path,
        "local_path": local_path,
        "download_error": dl_err,
    }


def _prepare_lyrics_assets(*, out_id: str, title: str, prompt: str, lyrics_text: str,
                           style_tags: str = "") -> dict:
    safe = _sanitize_filename(title, "lyrics")
    lyrics_path = _write_text_file(lib_mod.OUTPUT_DIR() / f"{safe}.lyrics.txt", lyrics_text)
    tags_path = ""
    if style_tags:
        tags_path = _write_text_file(lib_mod.OUTPUT_DIR() / f"{safe}.tags.txt", style_tags + "\n")
    meta_lines = [
        f"id: {out_id}",
        f"title: {title}",
        f"type: lyrics",
        f"provider: {config.get_provider()}",
        f"prompt: {prompt}",
        f"created: {lib_mod._now()}",
    ]
    if style_tags:
        meta_lines.append(f"style_tags: {style_tags}")
    meta_path = _write_meta_file(safe, meta_lines)
    return {
        "lyrics_path": lyrics_path,
        "tags_path": tags_path,
        "meta_path": meta_path,
    }


def _clear_session_pick_flag(data):
    if data.get("params", {}).get("awaiting_session_pick"):
        params = dict(data.get("params", {}))
        params.pop("awaiting_session_pick", None)
        session.update(params)


def _step_prompt(state_val: str, step: int, params: dict) -> str:
    if state_val == session.State.MUSIC.value:
        if step == 0:
            return MENU.strip()
        if step == 1:
            return "🎵 **音乐生成**\n\n请描述音乐风格/情绪/场景："
        if step == 2:
            return (
                f"✅ 风格确认：「{params.get('prompt', '')}」\n\n"
                "接下来，音乐要不要带歌词？\n\n"
                "    A) 自动生成歌词\n"
                "    B) 我有歌词，填在这里\n"
                "    C) 纯音乐（无人声）\n\n"
                "请选择 A / B / C 或直接发歌词"
            )
        if step == 3:
            return "回复「确认」执行生成，或直接修改内容重新发送"

    if state_val == session.State.LYRICS.value:
        if step == 0:
            return MENU.strip()
        if step == 1:
            return "📝 **写歌词**\n\n请描述想写什么主题/风格的歌："
        if step == 2:
            return "要不要指定标题？（直接回标题，或跳过）"
        if step == 3:
            return "回复「确认」开始生成歌词"

    if state_val == session.State.COVER.value:
        if step == 0:
            return MENU.strip()
        if step == 1:
            return "🎙️ **翻唱**\n\n请提供参考音频的 URL（6秒~6分钟，≤50MB）："
        if step == 2:
            return "✅ 音频已收到\n\n请描述想翻唱成什么风格（10~300字）："
        if step == 3:
            return "回复「确认」开始翻唱"

    if state_val == session.State.DONE.value:
        return "已恢复到生成完成状态，可继续下载/继续生成/查看音乐库。"

    return MENU.strip()


def render_restored_session(s: dict) -> str:
    state_val = s.get("state", session.State.MUSIC.value)
    step = s.get("step", 0)
    params = s.get("params", {})
    return (
        f"✅ 已恢复「{s.get('title', s.get('id', '未知会话'))}」，"
        f"{len(s.get('messages', []))} 条历史消息\n\n"
        f"{_step_prompt(state_val, step, params)}"
    )


def show_session_history(data) -> str:
    sessions = sm.list_sessions(limit=20)
    if not sessions:
        return "📭 暂无会话记录"
    session.update({"awaiting_session_pick": True})
    lines = ["=== 最近会话 ===\n"]
    for idx, s in enumerate(sessions, 1):
        updated = s.get("updated", "")[:10]
        title = s.get("title", s["id"])
        m_count = len(sm.get_session(s["id"]).get("messages", []))
        lines.append(f"[{idx}] {title}")
        lines.append(f"    {s.get('type','-')} | 更新: {updated} | {m_count} 条消息")
    lines.append("\n输入序号恢复会话，或「返回」回到主菜单")
    return "\n".join(lines)


def resume_session_pick(msg, data) -> str:
    sessions = sm.list_sessions(limit=20)
    idx = int(msg.strip()) - 1
    if 0 <= idx < len(sessions):
        sid = sessions[idx]["id"]
        s = sm.resume_session(sid)
        params = dict(s.get("params", {}))
        params.pop("awaiting_session_pick", None)
        session.restore_state(s.get("state", session.State.MUSIC.value), s.get("step", 0), params)
        return render_restored_session(sm.get_active())
    return "请输入正确的序号，或说「返回」"


# ── music 引导 ──────────────────────────────────────────────

def music_flow(msg, data):
    step = data.get("step", 0)
    params = data.get("params", {})
    _clear_session_pick_flag(data)

    if msg.strip() in ("上一步", "返回", "back"):
        return _go_back(data)

    if step == 0:
        if msg.strip() in ("1", "生成音乐", "生成", "做音乐"):
            session.update({"prev_params": {}}, step=1)
            return (
                "🎵 **音乐生成**\n\n"
                "请描述音乐风格/情绪/场景：\n"
                "比如「轻快的钢琴曲」「悲伤的电子乐」「夏日海边氛围」"
            )
        return _route_main(msg, data)

    elif step == 1:
        if not msg.strip():
            return "请输入音乐风格描述～"
        prompt_text = msg.strip()
        session.update({"prompt": prompt_text, "prev_params": {"step": 1, "params": {}}}, step=2)
        return (
            "✅ 风格确认：「{}」\n\n"
            "接下来，音乐要不要带歌词？\n\n"
            "    A) 自动生成歌词\n"
            "    B) 我有歌词，填在这里\n"
            "    C) 纯音乐（无人声）\n\n"
            "请选择 A / B / C 或直接发歌词\n"
            "（说「上一步」可返回修改风格）"
        ).format(prompt_text)

    elif step == 2:
        lyric_choice = msg.strip().upper()
        raw_input = msg.strip()

        if lyric_choice == "A":
            session.update({"lyrics": "__optimizer__", "prev_params": {"step": 2, "params": params}}, step=3)
            return _confirm_prompt(params["prompt"], None, True, False)

        if lyric_choice == "B":
            session.update({"prev_params": {"step": 2, "params": params}}, step=3)
            return (
                "请把歌词内容发给我（用 \\n 换行）\n\n"
                "💡 小技巧：在歌词开头加一行 `style: 风格标签` 可以自动指定音乐风格"
            )

        if lyric_choice == "C":
            session.update({"lyrics": "__instrumental__", "prev_params": {"step": 2, "params": params}}, step=3)
            return _confirm_prompt(params["prompt"], None, False, True)

        clean_lyrics, style_hint, title_hint = _parse_lyrics_meta(raw_input)
        updates = {"lyrics": clean_lyrics, "prev_params": {"step": 2, "params": params}}
        if style_hint:
            updates["style_hint"] = style_hint
        if title_hint:
            updates["title_hint"] = title_hint
        session.update(updates, step=3)
        return _confirm_prompt(params["prompt"], clean_lyrics, False, False,
                               style_hint=style_hint, title_hint=title_hint)

    elif step == 3:
        if msg.strip() in ("确认", "执行", "好", "生成", "是"):
            return _do_music(data["params"])
        clean_lyrics, style_hint, title_hint = _parse_lyrics_meta(msg.strip())
        updates = {"lyrics": clean_lyrics}
        if style_hint:
            updates["style_hint"] = style_hint
        if title_hint:
            updates["title_hint"] = title_hint
        session.update(updates)
        return _confirm_prompt(params["prompt"], clean_lyrics, False, False,
                               style_hint=style_hint, title_hint=title_hint)


# ── lyrics 引导 ─────────────────────────────────────────────

def lyrics_flow(msg, data):
    step = data.get("step", 0)
    params = data.get("params", {})
    _clear_session_pick_flag(data)

    if msg.strip() in ("上一步", "返回", "back"):
        return _go_back(data)

    if step == 0:
        if msg.strip() in ("2", "写歌词", "歌词", "作词"):
            session.update({"prev_params": {}}, step=1)
            return "📝 **写歌词**\n\n请描述想写什么主题/风格的歌："
        return _route_main(msg, data)

    elif step == 1:
        if not msg.strip():
            return "请输入主题～"
        clean_prompt, style_hint, title_hint = _parse_lyrics_meta(msg.strip())
        updates = {"prompt": clean_prompt, "prev_params": {"step": 1, "params": {}}}
        auto_title = None
        if title_hint:
            auto_title = title_hint
            updates["title"] = title_hint
        if style_hint:
            updates["style_hint"] = style_hint

        if auto_title:
            session.update(updates, step=3)
            return f"✅ 主题确认：「{clean_prompt}」\n📌 已从内容中检测到标题：「{auto_title}」\n\n回复「确认」开始生成歌词"

        session.update(updates, step=2)
        return f"✅ 主题确认：「{clean_prompt}」\n\n要不要指定标题？（直接回标题，或跳过）"

    elif step == 2:
        raw = msg.strip()
        if raw in ("跳过", "", "不用", "n"):
            session.update({"title": None, "prev_params": {"step": 2, "params": params}}, step=3)
            return "好的，不设标题\n\n回复「确认」开始生成歌词"

        _, style_hint, title_hint = _parse_lyrics_meta(raw)
        is_confirm_word = raw in ("确认", "执行", "好", "生成", "是")

        if title_hint and not is_confirm_word:
            title = title_hint
        elif is_confirm_word:
            title = params.get("title")
        else:
            title = raw

        updates = {"title": title, "prev_params": {"step": 2, "params": params}}
        if style_hint:
            updates["style_hint"] = style_hint
        session.update(updates, step=3)

        title_display = title if title else "（无）"
        return f"好的，标题：「{title_display}」\n\n回复「确认」开始生成歌词"

    elif step == 3:
        if msg.strip() in ("确认", "执行", "好", "生成", "是"):
            return _do_lyrics(data["params"])
        return "回复「确认」或「执行」开始生成"


# ── cover 引导 ──────────────────────────────────────────────

def cover_flow(msg, data):
    step = data.get("step", 0)
    params = data.get("params", {})
    _clear_session_pick_flag(data)

    if msg.strip() in ("上一步", "返回", "back"):
        return _go_back(data)

    if step == 0:
        if msg.strip() in ("3", "翻唱"):
            session.update({"prev_params": {}}, step=1)
            return "🎙️ **翻唱**\n\n请提供参考音频的 URL（6秒~6分钟，≤50MB）："
        return _route_main(msg, data)

    elif step == 1:
        url = msg.strip()
        if not url.startswith("http"):
            return "请输入有效的 URL（以 http:// 或 https:// 开头）"
        session.update({"audio": url, "prev_params": {"step": 1, "params": {}}}, step=2)
        return "✅ 音频已收到\n\n请描述想翻唱成什么风格（10~300字）："

    elif step == 2:
        if len(msg.strip()) < 10:
            return "风格描述请稍详细一点（10字以上）"
        session.update({"prompt": msg.strip(), "prev_params": {"step": 2, "params": params}}, step=3)
        return f"✅ 风格确认：「{msg.strip()}」\n\n回复「确认」开始翻唱"

    elif step == 3:
        if msg.strip() in ("确认", "执行", "好", "生成", "是"):
            return _do_cover(data["params"])
        return "回复「确认」或「执行」开始翻唱"


# ── 上一步 ─────────────────────────────────────────────────

def _go_back(data):
    prev = session.get_prev(data)
    if not prev:
        return "已经是第一步了，无法返回～"
    session.restore_state(prev["state"], prev["step"], prev["params"])
    return "✅ 已返回上一步，请重新输入"


# ── 主菜单路由 ─────────────────────────────────────────────

def _route_main(msg, data):
    m = msg.strip()
    if m in ("1", "生成音乐", "做音乐"):
        session.update({"prev_params": {}}, step=1)
        return "🎵 **音乐生成**\n\n请描述音乐风格/情绪/场景："
    if m in ("2", "写歌词", "歌词"):
        session.set_state(session.State.LYRICS.value, step=1)
        return "📝 **写歌词**\n\n请描述想写什么主题/风格的歌："
    if m in ("3", "翻唱"):
        session.set_state(session.State.COVER.value, step=1)
        return "🎙️ **翻唱**\n\n请提供参考音频的 URL（6秒~6分钟，≤50MB）："
    if m in ("4", "查看音乐库", "音乐库"):
        session.end()
        return _fmt_library()
    if m in ("5", "导出", "清理"):
        session.end()
        return _fmt_export()
    if m in ("6", "会话历史", "历史记录"):
        return show_session_history(data)
    return "不认识这个选项，请输入 1~6"


# ── 确认信息组装 ────────────────────────────────────────────

def _confirm_prompt(prompt, lyrics, use_optimizer, is_instrumental,
                    style_hint=None, title_hint=None):
    if is_instrumental:
        kind = "（纯音乐）"
    elif use_optimizer:
        kind = "（自动生成歌词）"
    else:
        kind = "（已有歌词）"

    parts = [f"✅ 确认信息：", f"  风格：「{prompt}」{kind}"]
    if style_hint:
        parts.insert(1, f"  🎨 已检测风格：「{style_hint}」（可覆盖）")
    if title_hint:
        parts.insert(1, f"  📌 已检测标题：「{title_hint}」（可覆盖）")
    parts.append("")
    parts.append("回复「确认」执行生成，或直接修改内容重新发送")
    return "\n".join(parts)


# ── API 直调执行（含附件交付）──────────────────────────────

def _do_music(params):
    prompt = params["prompt"]
    lyrics = params.get("lyrics", "")
    is_instrumental = lyrics == "__instrumental__"
    use_optimizer = lyrics == "__optimizer__"
    style_hint = params.get("style_hint")
    effective_prompt = f"{prompt}" + (f", {style_hint}" if style_hint else "")

    client = _get_client()
    model = config.get_music_model()

    def _call():
        return client.music_generation(
            model=model,
            prompt=effective_prompt,
            lyrics=(None if (is_instrumental or use_optimizer) else lyrics),
            is_instrumental=is_instrumental,
            lyrics_optimizer=use_optimizer,
        )

    try:
        resp = _call_with_retry(_call, "音乐")
        client.raise_on_error(resp)
    except Exception as e:
        session.end()
        return f"❌ 音乐生成失败（已重试）：{e}"

    audio_url = resp.get("data", {}).get("audio", "")
    if not audio_url:
        session.end()
        return "❌ 生成失败：未返回音频链接"

    out_id = str(uuid.uuid4())
    lib_mod.ensure_output_dir()
    title = params.get("title_hint") or prompt
    assets = _prepare_music_assets(
        out_id=out_id,
        title=title,
        entry_type="music",
        prompt=effective_prompt,
        audio_url=audio_url,
        provider=config.get_provider(),
        model=model,
        lyrics_text=(lyrics if lyrics not in ("__instrumental__", "__optimizer__") else ""),
    )

    entry = {
        "id": out_id,
        "title": title,
        "created": lib_mod._now(),
        "type": "music",
        "provider": config.get_provider(),
        "model": model,
        "music_url": audio_url,
        "local_path": assets.get("local_path", ""),
        "url_path": assets.get("url_path", ""),
        "meta_path": assets.get("meta_path", ""),
        "lyrics_path": assets.get("lyrics_path", ""),
        "expires": lib_mod._expires(),
    }
    lib_mod.add_entry(entry)

    session.update({
        "last_type": "music",
        "last_title": title,
        "last_url": audio_url,
        "last_local_path": assets.get("local_path", ""),
        "last_url_path": assets.get("url_path", ""),
        "last_meta_path": assets.get("meta_path", ""),
        "last_lyrics_path": assets.get("lyrics_path", ""),
    })
    session.set_state(session.State.DONE.value)

    media_lines = _build_media_lines([
        assets.get("local_path"),
        assets.get("url_path"),
        assets.get("meta_path"),
        assets.get("lyrics_path"),
    ])
    msg = "🎵 音乐已生成！"
    if assets.get("local_path"):
        msg += f"\n已附上音频与说明文件：{Path(assets['local_path']).name}"
    else:
        msg += f"\n⚠️ 音频自动下载失败：{assets.get('download_error')}\n已附上链接与说明文件。"
    msg += "\n\n接下来想做什么？\n  A) 下载音频\n  B) 基于这首继续生成（改风格/加歌词）\n  C) 查看音乐库\n  D) 退出\n请输入 A / B / C / D"
    if media_lines:
        msg += "\n" + media_lines
    return msg


def _do_lyrics(params):
    client = _get_client()
    style_hint = params.get("style_hint")
    effective_prompt = params["prompt"] + (f", {style_hint}" if style_hint else "")

    def _call():
        return client.lyrics_generation(
            prompt=effective_prompt,
            mode="write_full_song",
            title=params.get("title"),
        )

    try:
        resp = _call_with_retry(_call, "歌词")
        client.raise_on_error(resp)
    except Exception as e:
        session.end()
        return f"❌ 歌词生成失败（已重试）：{e}"

    song_title = resp.get("song_title", "未命名")
    style_tags = resp.get("style_tags", "")
    lyrics_text = resp.get("lyrics", "")

    if not lyrics_text:
        session.end()
        return "❌ 生成失败：未返回歌词"

    out_id = str(uuid.uuid4())
    lib_mod.ensure_output_dir()
    assets = _prepare_lyrics_assets(
        out_id=out_id,
        title=song_title,
        prompt=effective_prompt,
        lyrics_text=lyrics_text,
        style_tags=style_tags,
    )

    entry = {
        "id": out_id,
        "title": song_title,
        "created": lib_mod._now(),
        "type": "lyrics",
        "provider": config.get_provider(),
        "style_tags": style_tags,
        "lyrics_path": assets.get("lyrics_path", ""),
        "tags_path": assets.get("tags_path", ""),
        "meta_path": assets.get("meta_path", ""),
        "expires": lib_mod._expires(),
    }
    lib_mod.add_entry(entry)

    session.update({
        "last_type": "lyrics",
        "last_title": song_title,
        "last_lyrics": lyrics_text,
        "last_tags": style_tags,
        "last_lyrics_path": assets.get("lyrics_path", ""),
        "last_tags_path": assets.get("tags_path", ""),
        "last_meta_path": assets.get("meta_path", ""),
    })
    session.set_state(session.State.DONE.value)

    header = f"📝 **{song_title}**"
    if style_tags:
        header += f"\n风格: {style_tags}"
    media_lines = _build_media_lines([
        assets.get("lyrics_path"),
        assets.get("tags_path"),
        assets.get("meta_path"),
    ])
    msg = (
        f"{header}\n\n{lyrics_text}\n\n"
        "已附上歌词与说明文件。\n"
        "接下来想做什么？\n"
        "  A) 继续生成（基于这个主题再做一首）\n"
        "  B) 查看音乐库\n"
        "  C) 退出\n"
        "请输入 A / B / C"
    )
    if media_lines:
        msg += "\n" + media_lines
    return msg


def _do_cover(params):
    client = _get_client()
    preprocess_model = config.get_cover_model()
    generate_model = config.get_music_model()

    def _preprocess():
        return client.music_cover_preprocess(
            model=preprocess_model,
            audio_url=params["audio"],
        )

    try:
        prep = _call_with_retry(_preprocess, "翻唱前处理")
        client.raise_on_error(prep)
    except Exception as e:
        session.end()
        return f"❌ 翻唱前处理失败（已重试）：{e}"

    cover_feature_id = prep.get("cover_feature_id", "")
    auto_lyrics = prep.get("formatted_lyrics", "")
    if not cover_feature_id:
        session.end()
        return "❌ 翻唱前处理失败：未返回 cover_feature_id"

    def _call():
        return client.music_generation(
            model=generate_model,
            prompt=params["prompt"],
            lyrics=params.get("lyrics") or auto_lyrics or None,
            cover_feature_id=cover_feature_id,
        )

    try:
        resp = _call_with_retry(_call, "翻唱")
        client.raise_on_error(resp)
    except Exception as e:
        session.end()
        return f"❌ 翻唱生成失败（已重试）：{e}"

    audio_url = resp.get("data", {}).get("audio", "")
    if not audio_url:
        session.end()
        return "❌ 生成失败：未返回音频链接"

    out_id = str(uuid.uuid4())
    lib_mod.ensure_output_dir()
    title = params["prompt"]
    assets = _prepare_music_assets(
        out_id=out_id,
        title=title,
        entry_type="cover",
        prompt=params["prompt"],
        audio_url=audio_url,
        provider=config.get_provider(),
        model=generate_model,
        reference_url=params.get("audio", ""),
        lyrics_text=(params.get("lyrics") or auto_lyrics or ""),
    )

    entry = {
        "id": out_id,
        "title": title,
        "created": lib_mod._now(),
        "type": "cover",
        "provider": config.get_provider(),
        "model": generate_model,
        "preprocess_model": preprocess_model,
        "music_url": audio_url,
        "reference_url": params["audio"],
        "cover_feature_id": cover_feature_id,
        "formatted_lyrics": auto_lyrics,
        "local_path": assets.get("local_path", ""),
        "url_path": assets.get("url_path", ""),
        "meta_path": assets.get("meta_path", ""),
        "lyrics_path": assets.get("lyrics_path", ""),
        "expires": lib_mod._expires(),
    }
    lib_mod.add_entry(entry)

    session.update({
        "last_type": "cover",
        "last_title": title,
        "last_url": audio_url,
        "last_reference": params["audio"],
        "last_local_path": assets.get("local_path", ""),
        "last_url_path": assets.get("url_path", ""),
        "last_meta_path": assets.get("meta_path", ""),
        "last_lyrics_path": assets.get("lyrics_path", ""),
    })
    session.set_state(session.State.DONE.value)

    media_lines = _build_media_lines([
        assets.get("local_path"),
        assets.get("url_path"),
        assets.get("meta_path"),
        assets.get("lyrics_path"),
    ])
    msg = "🎵 翻唱已生成！"
    if assets.get("local_path"):
        msg += f"\n已附上音频与说明文件：{Path(assets['local_path']).name}"
    else:
        msg += f"\n⚠️ 音频自动下载失败：{assets.get('download_error')}\n已附上链接与说明文件。"
    msg += "\n\n接下来想做什么？\n  A) 下载音频\n  B) 基于这个参考音频继续生成\n  C) 查看音乐库\n  D) 退出\n请输入 A / B / C / D"
    if media_lines:
        msg += "\n" + media_lines
    return msg


# ── done flow：生成完成后询问后续操作 ────────────────────────

def done_flow(msg, data):
    params = data.get("params", {})
    last_type = params.get("last_type", "")
    last_title = params.get("last_title", "")
    choice = msg.strip().upper()

    if last_type == "lyrics":
        mapping = {"A": "continue", "B": "library", "C": "quit"}
        if choice not in mapping:
            return "请输入 A / B / C"
    else:
        mapping = {"A": "download", "B": "continue", "C": "library", "D": "quit"}
        if choice not in mapping:
            return "请输入 A / B / C / D"

    action = mapping[choice]

    if action == "download":
        return _do_download(params, last_type, last_title)
    if action == "continue":
        return _do_continue_from_last(params, last_type)
    if action == "library":
        session.end()
        return _fmt_library()
    session.end()
    return "好的，有需要再说～ 👋"


def _do_download(params, last_type, last_title):
    if last_type == "lyrics":
        lyrics_path = params.get("last_lyrics_path", "")
        tags_path = params.get("last_tags_path", "")
        meta_path = params.get("last_meta_path", "")
        if lyrics_path:
            media = _build_media_lines([lyrics_path, tags_path, meta_path])
            return f"📝 已附上歌词文件与说明。\n{media}".strip()
        lyrics = params.get("last_lyrics", "")
        if lyrics:
            out = lib_mod.OUTPUT_DIR() / f"{_sanitize_filename(last_title, 'lyrics')}.lyrics.txt"
            out.write_text(lyrics)
            media = _build_media_lines([out, meta_path])
            return f"📝 已附上歌词文件与说明。\n{media}".strip()
        return "❌ 未找到歌词内容"

    local_path = params.get("last_local_path", "")
    url_path = params.get("last_url_path", "")
    meta_path = params.get("last_meta_path", "")
    if local_path or url_path or meta_path:
        media = _build_media_lines([local_path, url_path, meta_path])
        return f"📥 已附上音频/链接与说明文件。\n{media}".strip()

    url = params.get("last_url", "")
    if not url:
        return "❌ 未找到音频 URL"

    local_path, err = _save_audio_from_url(last_title, url)
    if local_path:
        lib = lib_mod.read_library()
        for song in reversed(lib["songs"]):
            if song.get("title") == last_title and song.get("type") == last_type:
                song["local_path"] = str(local_path)
                break
        lib_mod.write_library(lib)
        media = _build_media_lines([local_path, url_path, meta_path])
        return f"📥 已附上音频/链接与说明文件。\n{media}".strip()
    return f"❌ 下载失败：{err}"


def _do_continue_from_last(params, last_type):
    if last_type == "music":
        prev = {"prompt": params.get("last_title", "")}
        session.set_state(session.State.MUSIC.value, step=1)
        session.update(prev)
        return "🎵 继续生成音乐\n\n请描述新的风格/变化（例如「更欢快的版本」）："

    if last_type == "lyrics":
        prev = {"prompt": params.get("last_title", "")}
        session.set_state(session.State.MUSIC.value, step=1)
        session.update(prev)
        return f"🎵 基于歌词「{params.get('last_title', '')}」继续生成音乐\n\n请描述新的风格/变化："

    if last_type == "cover":
        prev = {"audio": params.get("last_reference", "")}
        session.set_state(session.State.COVER.value, step=2)
        session.update(prev)
        return "🎙️ 继续翻唱\n\n请描述新的翻唱风格："

    session.end()
    return "无法继续，请重新开始"


# ── library 工具（含音频批量下载）────────────────────────────

def _fmt_library():
    lib_mod.remove_expired()
    try:
        entries = list(lib_mod.list_entries())
    except Exception:
        return "📭 暂无任何记录"
    if not entries:
        return "📭 暂无任何记录"
    lines = [f"=== 音乐库记录（共 {len(entries)} 条）===\n"]
    for idx, song in entries:
        has_local = " 📥" if song.get("local_path") else ""
        lines.append(f"[{idx}] {song.get('title', '未知')}")
        lines.append(f"    类型: {song.get('type', '-')} | 模型: {song.get('model') or '-'} | 创建: {song.get('created', '-')[:10]}{has_local}")
        lines.append("")
    return "```\n" + "\n".join(lines).strip() + "\n```"


def _fmt_export():
    lib_mod.remove_expired()
    lib = lib_mod.read_library()
    songs = lib.get("songs", [])
    if not songs:
        return "📭 暂无记录可导出"

    delivered = []
    downloaded = 0
    errors = []

    for song in songs:
        if song.get("local_path"):
            delivered.append(song.get("local_path"))
        if song.get("lyrics_path"):
            delivered.append(song.get("lyrics_path"))
        if song.get("tags_path"):
            delivered.append(song.get("tags_path"))
        if song.get("url_path"):
            delivered.append(song.get("url_path"))
        if song.get("meta_path"):
            delivered.append(song.get("meta_path"))

        title = song.get("title", "未知").replace("/", "_").replace("\\", "_")
        stype = song.get("type", "")

        if stype in ("music", "cover") and song.get("music_url") and not song.get("local_path"):
            try:
                data = _download_url(song["music_url"])
                mp3_path = lib_mod.OUTPUT_DIR() / f"{title}.mp3"
                mp3_path.write_bytes(data)
                song["local_path"] = str(mp3_path)
                delivered.append(str(mp3_path))
                downloaded += 1
            except Exception as e:
                errors.append(f"[{title}] 下载失败: {e}")

    lib_mod.write_library(lib)

    msg = f"📦 已整理并导出 {len(songs)} 条记录"
    if downloaded:
        msg += f"，补下了 {downloaded} 个音频文件"
    if errors:
        msg += "\n部分音频下载失败：\n" + "\n".join(errors)
    media = _build_media_lines(delivered[:20])
    if media:
        msg += "\n" + media
    return msg
