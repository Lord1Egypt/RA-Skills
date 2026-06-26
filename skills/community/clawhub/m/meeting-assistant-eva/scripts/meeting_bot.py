#!/usr/bin/env python3
"""
Meeting Bot — AI 会议机器人
通过 Vexa API (自托管) 让 AI Bot 直接加入 Zoom/Teams 会议。
Bot 能：加入会议、捕获音频/视频、实时转录、在聊天中发消息。

架构:
  Vexa (Docker) ← → meeting_bot.py ← → openclaw Agent
       ↓                    ↓
  Zoom/Teams          Whisper/Claude 分析
"""

import json
import time
import requests
import threading
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


class MeetingBot:
    """
    通过 Vexa API 控制会议机器人。
    支持 Zoom、Teams、Google Meet。

    Vexa API 使用 (platform, native_meeting_id) 作为资源标识符。
    API Token: X-API-Key header (来自 config.json bot.vexa_api_key)
    """

    def __init__(self, config=None):
        if config is None:
            config = load_config()
        self.config = config
        bot_cfg = config.get("bot", {})
        self.base_url = bot_cfg.get("vexa_url", "http://localhost:8056").rstrip("/")
        self.api_key = bot_cfg.get("vexa_api_key", "openclaw-meeting-bot")
        self.bot_name = bot_cfg.get("bot_name", "OpenClaw 助手")
        self.bot_id = None       # kept for backward compat
        self.platform = None
        self.meeting_id = None   # native_meeting_id
        self._polling_thread = None
        self._polling = False

    @property
    def headers(self):
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["X-API-Key"] = self.api_key
        return h

    def _meeting_path(self):
        """Return URL fragment: platform/native_meeting_id"""
        return f"{self.platform}/{self.meeting_id}"

    # ─── 会议生命周期 ──────────────────────────────────

    def join(self, meeting_url, bot_name=None, language=None):
        """
        加入会议。自动识别平台 (Zoom/Teams/Meet)。

        Args:
            meeting_url: 会议链接
            bot_name:    Bot 显示名称
            language:    转录语言代码 (e.g. "zh", "en")

        Returns:
            meeting_id
        """
        platform, meeting_id, passcode = self._parse_meeting_url(meeting_url)
        self.platform = platform
        self.meeting_id = meeting_id
        self.bot_id = meeting_id  # backward compat

        payload = {
            "platform": platform,
            "native_meeting_id": meeting_id,
            "bot_name": bot_name or self.bot_name,
        }
        if language:
            payload["language"] = language
        elif self.config.get("whisper_language"):
            payload["language"] = self.config["whisper_language"]

        print(f"[Bot] Joining {platform} meeting: {meeting_id}")
        resp = requests.post(
            f"{self.base_url}/bots",
            headers=self.headers,
            json=payload,
            timeout=30,
        )
        if resp.status_code not in (200, 201):
            print(f"[Bot] Join response: {resp.status_code} - {resp.text[:300]}")
        resp.raise_for_status()
        data = resp.json()
        print(f"[Bot] Joined! platform={platform} meeting_id={meeting_id}")
        print(f"[Bot] Response: {json.dumps(data, ensure_ascii=False)[:200]}")
        return meeting_id

    def leave(self):
        """离开会议。"""
        if not self.platform or not self.meeting_id:
            print("[Bot] No active session")
            return

        self._polling = False
        print(f"[Bot] Leaving meeting {self._meeting_path()}...")
        try:
            resp = requests.delete(
                f"{self.base_url}/bots/{self._meeting_path()}",
                headers=self.headers,
                timeout=15,
            )
            print(f"[Bot] Left: {resp.status_code}")
        except requests.RequestException as e:
            print(f"[Bot] Leave error: {e}")

    def status(self):
        """获取所有 Bot 状态。"""
        resp = requests.get(
            f"{self.base_url}/bots/status",
            headers=self.headers,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    # ─── 转录 ─────────────────────────────────────────

    def get_transcript(self, since=None):
        """
        获取会议转录文本。

        Returns:
            list of {speaker, text, timestamp, ...}
        """
        if not self.platform or not self.meeting_id:
            return []

        url = f"{self.base_url}/transcripts/{self._meeting_path()}"
        params = {}
        if since:
            params["created_after"] = since

        resp = requests.get(url, headers=self.headers, params=params, timeout=15)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        data = resp.json()

        # Normalize: Vexa returns list or {"utterances": [...]}
        if isinstance(data, list):
            return data
        return data.get("utterances", data.get("entries", data.get("transcript", [])))

    def get_full_transcript_text(self):
        """获取完整转录文本（格式化）。"""
        entries = self.get_transcript()
        lines = []
        for e in entries:
            speaker = e.get("speaker", e.get("speaker_name", "Unknown"))
            text    = e.get("text", e.get("words", e.get("content", "")))
            ts      = e.get("created_at", e.get("timestamp", ""))
            lines.append(f"[{ts}] {speaker}: {text}")
        return "\n".join(lines)

    def start_transcript_polling(self, callback=None, interval=10):
        """后台轮询转录，新内容触发 callback。"""
        self._polling = True
        last_ts = None

        def _poll():
            nonlocal last_ts
            while self._polling:
                try:
                    entries = self.get_transcript(since=last_ts)
                    if entries:
                        if last_ts and callback:
                            callback(entries)
                        last_entry = entries[-1]
                        last_ts = last_entry.get("created_at", last_entry.get("timestamp", last_ts))
                except Exception as e:
                    print(f"[Bot] Transcript poll error: {e}")
                time.sleep(interval)

        self._polling_thread = threading.Thread(target=_poll, daemon=True)
        self._polling_thread.start()
        print(f"[Bot] Transcript polling started (every {interval}s)")

    # ─── 聊天 ─────────────────────────────────────────

    def send_chat(self, message):
        """在会议聊天中发送消息。"""
        if not self.platform or not self.meeting_id:
            print("[Bot] No active session")
            return

        print(f"[Bot] Sending chat: {message[:80]}...")
        resp = requests.post(
            f"{self.base_url}/bots/{self._meeting_path()}/chat",
            headers=self.headers,
            json={"text": message},
            timeout=15,
        )
        if resp.status_code not in (200, 201):
            print(f"[Bot] Chat send: {resp.status_code} - {resp.text[:200]}")
        else:
            print("[Bot] Chat sent")
        return resp

    def read_chat(self):
        """读取会议聊天记录。"""
        if not self.platform or not self.meeting_id:
            return []

        resp = requests.get(
            f"{self.base_url}/bots/{self._meeting_path()}/chat",
            headers=self.headers,
            timeout=15,
        )
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("messages", data.get("items", []))

    # ─── 截图 ────────────────────────────────────────

    def get_screenshot(self, save_path=None):
        """
        启动/获取 Bot 屏幕画面。
        Vexa: POST /bots/{platform}/{id}/screen 开始屏幕共享
        实际截图需从录制流或屏幕共享中获取。
        """
        if not self.platform or not self.meeting_id:
            return None

        # Try to get a screenshot via screen endpoint
        try:
            resp = requests.post(
                f"{self.base_url}/bots/{self._meeting_path()}/screen",
                headers=self.headers,
                json={},
                timeout=10,
            )
            if resp.status_code in (200, 201):
                content_type = resp.headers.get("content-type", "")
                if "image" in content_type:
                    if save_path is None:
                        ts = datetime.now().strftime("%H%M%S")
                        save_dir = SKILL_DIR / "recordings" / "bot_screenshots"
                        save_dir.mkdir(parents=True, exist_ok=True)
                        save_path = save_dir / f"meeting_{ts}.png"
                    Path(save_path).write_bytes(resp.content)
                    print(f"[Bot] Screenshot saved: {save_path}")
                    return str(save_path)
        except Exception as e:
            print(f"[Bot] Screenshot via screen endpoint failed: {e}")

        print("[Bot] Screenshot not available (Vexa requires browser bot to be active)")
        return None

    def set_avatar(self, image_url):
        """设置 Bot 头像。"""
        if not self.platform or not self.meeting_id:
            return
        resp = requests.put(
            f"{self.base_url}/bots/{self._meeting_path()}/avatar",
            headers=self.headers,
            json={"image_url": image_url},
            timeout=10,
        )
        return resp.json()

    # ─── 工具方法 ─────────────────────────────────────

    def _parse_meeting_url(self, url):
        """
        解析会议 URL，返回 (platform, native_meeting_id, passcode)。
        """
        url = url.strip()
        passcode = None

        # Zoom
        if "zoom.us" in url or "zoom.com" in url:
            platform = "zoom"
            if "/j/" in url:
                mid = url.split("/j/")[1].split("?")[0].split("#")[0]
            elif "/wc/" in url:
                mid = url.split("/wc/")[1].split("/")[0]
            else:
                mid = url
            if "pwd=" in url:
                passcode = url.split("pwd=")[1].split("&")[0].split("#")[0]
            meeting_id = mid.replace("-", "").strip()

        # Teams
        elif "teams.microsoft.com" in url or "teams.live.com" in url:
            platform = "teams"
            meeting_id = url

        # Google Meet
        elif "meet.google.com" in url:
            platform = "google_meet"
            meeting_id = url.split("meet.google.com/")[1].split("?")[0].strip("/")

        # Raw meeting ID
        elif url.replace("-", "").isdigit():
            platform = "zoom"
            meeting_id = url.replace("-", "")

        else:
            platform = "zoom"
            meeting_id = url

        return platform, meeting_id, passcode

    def list_bots(self):
        """列出所有活跃的 Bot。"""
        resp = requests.get(
            f"{self.base_url}/bots/status",
            headers=self.headers,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


# ─── 高级：AI 会议助手循环 ────────────────────────────

class MeetingAssistantLoop:
    """
    AI 会议助手主循环。

    两个并发线程：
      1. 分析线程 (主线程)   — 每 interval 秒：截图 + 转录 → Claude 分析 → 聊天
      2. 聊天轮询线程 (后台)  — 每 chat_poll_interval 秒：读聊天 → 检测用户提问 → Claude 回答

    用户可以在会议聊天中直接向 Bot 提问，Bot 会实时回答。
    """

    def __init__(self, bot, config=None):
        self.bot = bot
        self.config = config or load_config()
        self.session_dir = None
        self._running = False
        self._mode = "general"

        # Data logs
        self.transcript_log = []        # all transcript entries
        self.suggestions_log = []       # all chat messages sent by bot

        # State tracking
        self._last_chat_count = 0       # index of last processed chat message
        self._latest_screenshot = None  # for providing visual context to chat replies
        self._cycle_count = 0

        # Claude API client (optional — bot still works without it)
        self.claude = None
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent))
            from claude_client import MeetingClaudeClient
            self.claude = MeetingClaudeClient(self.config)
            print("[Assistant] Claude API client initialized")
        except ImportError as e:
            print(f"[Assistant] anthropic not installed: {e}")
            print("[Assistant] Running in data-collection-only mode")
        except ValueError as e:
            print(f"[Assistant] Claude API key not set: {e}")
            print("[Assistant] Running in data-collection-only mode")
        except Exception as e:
            print(f"[Assistant] Claude client error: {e}")

        # Chat poll thread
        self._chat_poll_stop = threading.Event()
        self._chat_thread = None

    # ─── Public API ────────────────────────────────────────────────────────

    def start(self, meeting_url, mode="general", interval=30):
        """
        启动 AI 助手：加入会议 → 双线程运行（聊天轮询 + 分析循环）。

        Args:
            meeting_url: 会议链接 (Zoom/Teams/Meet URL)
            mode:        "general" 或 "medical"
            interval:    分析间隔（秒），默认 30
        """
        self._mode = mode

        # 1. Create session directory
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = SKILL_DIR / "recordings" / f"bot_{ts}"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        (self.session_dir / "screenshots").mkdir(exist_ok=True)
        (self.session_dir / "analysis").mkdir(exist_ok=True)

        # 2. Join meeting
        self.bot.join(meeting_url)

        # 3. Wait for bot to be in the meeting (poll meetings endpoint)
        print("[Assistant] Waiting for bot to join...")
        for _ in range(30):
            try:
                resp = requests.get(
                    f"{self.bot.base_url}/meetings",
                    headers=self.bot.headers,
                    timeout=10,
                )
                if resp.ok:
                    meetings = resp.json().get("meetings", [])
                    for m in meetings:
                        if (m.get("platform") == self.bot.platform and
                                m.get("native_meeting_id") == self.bot.meeting_id):
                            if m.get("status") == "active":
                                print("[Assistant] Bot is in the meeting!")
                                break
                            elif m.get("status") == "failed":
                                raise RuntimeError(f"Bot failed to join: {m.get('data', {}).get('error_details', '')[:200]}")
                    else:
                        time.sleep(2)
                        continue
                    break
            except RuntimeError:
                raise
            except Exception:
                pass
            time.sleep(2)

        # 4. Send greeting
        greeting = self._get_greeting(mode)
        try:
            self.bot.send_chat(greeting)
            self._log_suggestion(greeting, category="greeting")
        except Exception as e:
            print(f"[Assistant] Could not send greeting: {e}")

        # 5. Save session metadata
        meta = {
            "start_time": datetime.now().isoformat(),
            "meeting_url": meeting_url,
            "mode": mode,
            "bot_id": self.bot.bot_id,
            "platform": self.bot.platform,
            "claude_enabled": self.claude is not None,
        }
        with open(self.session_dir / "session.json", "w") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        # 6. Start chat poll thread (fast — every 5s)
        chat_interval = self.config.get("chat_poll_interval", 5)
        self._chat_poll_stop.clear()
        self._chat_thread = threading.Thread(
            target=self._chat_poll_loop,
            args=(chat_interval,),
            daemon=True,
            name="MeetingChatPoll",
        )
        self._chat_thread.start()
        print(f"[Assistant] Chat polling started (every {chat_interval}s)")

        # 7. Main analysis loop
        self._running = True
        print(f"[Assistant] Analysis loop started (every {interval}s, mode={mode})")
        claude_status = "with Claude AI" if self.claude else "data-collection only"
        print(f"[Assistant] Running {claude_status}")

        try:
            while self._running:
                self._analysis_cycle(mode)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[Assistant] Keyboard interrupt received")
        finally:
            self.stop()

    def stop(self):
        """停止助手、生成摘要、离开会议。"""
        if not self._running:
            return
        self._running = False

        # Stop chat thread
        self._chat_poll_stop.set()
        if self._chat_thread and self._chat_thread.is_alive():
            self._chat_thread.join(timeout=8)

        # Send farewell
        farewell = "📋 会议助手已停止记录。正在生成会议摘要，请稍候..."
        try:
            self.bot.send_chat(farewell)
        except Exception:
            pass

        # Save transcript + suggestions logs
        if self.session_dir:
            with open(self.session_dir / "transcript_log.json", "w", encoding="utf-8") as f:
                json.dump(self.transcript_log, f, ensure_ascii=False, indent=2)
            with open(self.session_dir / "suggestions_log.json", "w", encoding="utf-8") as f:
                json.dump(self.suggestions_log, f, ensure_ascii=False, indent=2)

            # Generate final summary with Claude
            if self.claude:
                print("[Assistant] Generating final meeting summary...")
                try:
                    summary = self.claude.generate_final_summary(self.session_dir, self._mode)
                    lines = summary.split("\n")[:3]
                    preview = " | ".join(l for l in lines if l.strip())[:120]
                    try:
                        self.bot.send_chat(f"✅ 会议摘要已生成！\n{preview}...\n（完整摘要已保存到文件）")
                    except Exception:
                        pass
                except Exception as e:
                    print(f"[Assistant] Summary generation failed: {e}")

        # Leave meeting
        self.bot.leave()
        print(f"[Assistant] Session saved: {self.session_dir}")

        # Update session status
        meta_path = self.session_dir / "session.json" if self.session_dir else None
        if meta_path and meta_path.exists():
            try:
                with open(meta_path, encoding="utf-8") as f:
                    meta = json.load(f)
                meta["status"] = "completed"
                meta["end_time"] = datetime.now().isoformat()
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

    # ─── Analysis Cycle ────────────────────────────────────────────────────

    def _analysis_cycle(self, mode):
        """
        单次分析循环（每 interval 秒）：
          截图 → 转录增量 → Claude 分析 → 若有建议则发聊天 → 记录
        """
        self._cycle_count += 1
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"\n[Analysis] Cycle #{self._cycle_count} at {ts}")

        # 1. Screenshot
        screenshot_path = None
        try:
            ss_filename = f"screen_{ts.replace(':', '')}.png"
            screenshot_path = self.bot.get_screenshot(
                self.session_dir / "screenshots" / ss_filename
            )
            if screenshot_path:
                self._latest_screenshot = screenshot_path
                print(f"[Analysis] Screenshot: {ss_filename}")
        except Exception as e:
            print(f"[Analysis] Screenshot failed: {e}")

        # 2. Transcript delta
        new_entries = []
        try:
            all_entries = self.bot.get_transcript()
            new_entries = all_entries[len(self.transcript_log):]
            if new_entries:
                self.transcript_log.extend(new_entries)
                for e in new_entries:
                    speaker = e.get("speaker", "?")
                    text    = e.get("text", "")[:120]
                    print(f"  [{ts}] {speaker}: {text}")
        except Exception as e:
            print(f"[Analysis] Transcript failed: {e}")

        # 3. Claude analysis (if available and there's something to analyze)
        analysis_result = None
        chat_msg_to_send = None

        if self.claude and (new_entries or screenshot_path):
            try:
                analysis_result = self.claude.analyze_meeting_state(
                    screenshot_path=screenshot_path,
                    transcript_entries=new_entries,
                    mode=mode,
                )
                print(f"[Analysis] Claude: {analysis_result['analysis'][:120]}...")

                # Send chat message if Claude suggests one
                if analysis_result.get("chat_message"):
                    chat_msg_to_send = analysis_result["chat_message"]
            except Exception as e:
                print(f"[Analysis] Claude analysis failed: {e}")

        if chat_msg_to_send:
            try:
                self.bot.send_chat(chat_msg_to_send)
                self._log_suggestion(chat_msg_to_send, category="analysis")
                print(f"[Analysis] Sent to chat: {chat_msg_to_send[:80]}")
            except Exception as e:
                print(f"[Analysis] Chat send failed: {e}")

        # 4. Log cycle entry
        entry = {
            "cycle": self._cycle_count,
            "timestamp": ts,
            "screenshot": str(screenshot_path) if screenshot_path else None,
            "new_transcript_entries": len(new_entries),
            "analysis": analysis_result.get("analysis", "") if analysis_result else None,
            "chat_sent": chat_msg_to_send,
        }
        log_path = self.session_dir / "analysis" / "cycle_log.jsonl"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ─── Chat Poll Loop ────────────────────────────────────────────────────

    def _chat_poll_loop(self, interval: int):
        """
        后台线程：每 interval 秒读取聊天，检测用户提问，用 Claude 回答。
        用户可以通过会议聊天直接和助手交流。
        """
        print(f"[Chat] Poll loop started")
        while not self._chat_poll_stop.is_set():
            try:
                self._process_incoming_chat()
            except Exception as e:
                print(f"[Chat] Poll error: {e}")
            self._chat_poll_stop.wait(interval)
        print("[Chat] Poll loop stopped")

    def _process_incoming_chat(self):
        """Read chat, find new messages directed at bot, generate Claude replies."""
        try:
            messages = self.bot.read_chat()
        except Exception as e:
            print(f"[Chat] read_chat error: {e}")
            return

        new_messages = messages[self._last_chat_count:]
        self._last_chat_count = len(messages)

        bot_name = self.config.get("bot", {}).get("bot_name", "OpenClaw").lower()

        for msg in new_messages:
            sender = msg.get("sender") or msg.get("from") or msg.get("author") or "?"
            text   = msg.get("text")  or msg.get("message") or msg.get("content") or ""

            # Skip empty messages and messages from the bot itself
            if not text.strip():
                continue
            if sender.lower() in (bot_name, "openclaw", "bot"):
                continue

            # Detect if this message is directed at / relevant to the bot
            if not self._should_respond_to_chat(text, sender):
                continue

            print(f"[Chat] Responding to {sender}: {text[:80]}")

            if self.claude:
                try:
                    reply = self.claude.respond_to_chat(
                        user_message=text,
                        sender=sender,
                        context_screenshot=self._latest_screenshot,
                        mode=self._mode,
                    )
                except Exception as e:
                    reply = f"抱歉，处理您的问题时出错了：{e}"
            else:
                reply = (
                    f"@{sender} 我收到了您的消息，但当前运行在数据收集模式"
                    f"（Claude API 未配置）。请配置 ANTHROPIC_API_KEY 以启用 AI 回答。"
                )

            try:
                self.bot.send_chat(f"@{sender} {reply}")
                self._log_suggestion(reply, category="chat_reply", meta={"to": sender, "question": text})
                print(f"[Chat] Replied to {sender}: {reply[:80]}")
            except Exception as e:
                print(f"[Chat] Send reply failed: {e}")

    def _should_respond_to_chat(self, text: str, sender: str) -> bool:
        """
        判断一条聊天消息是否需要助手回应。

        回应条件（满足任一）：
          1. 包含 Bot 名称 / @助手
          2. 包含问号（用户在提问）
          3. 医疗模式下包含医疗关键词
          4. 以特定指令前缀开头
        """
        t_lower = text.lower().strip()

        # Explicit bot mention
        triggers = ["openclaw", "助手", "@bot", "会议助手", "ai"]
        if any(tr in t_lower for tr in triggers):
            return True

        # Question mark (Chinese or English)
        if "?" in text or "？" in text:
            return True

        # Medical keywords in medical mode
        if self._mode == "medical":
            medical_kw = ["药", "诊断", "处方", "症状", "用法", "剂量", "医嘱",
                          "medication", "diagnosis", "prescription", "dosage"]
            if any(kw in t_lower for kw in medical_kw):
                return True

        # Command prefixes
        if t_lower.startswith(("/", "!", "！", "帮", "请问", "请")):
            return True

        return False

    # ─── Helpers ───────────────────────────────────────────────────────────

    def _log_suggestion(self, message: str, category: str = "general", meta: dict | None = None):
        """Record a bot-sent chat message."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "message": message,
        }
        if meta:
            entry.update(meta)
        self.suggestions_log.append(entry)

    def _get_greeting(self, mode):
        if mode == "medical":
            return (
                "🏥 OpenClaw 医疗会议助手已加入。\n"
                "我将实时记录并分析会议内容：\n"
                "• 自动转录对话\n"
                "• 识别医学术语并通俗解释\n"
                "• 在聊天中主动分享重要信息\n"
                "• 会后生成完整会议摘要\n"
                "您可以直接在聊天中向我提问，我会立即回答！"
            )
        return (
            "📝 OpenClaw 会议助手已加入。\n"
            "我将实时分析会议内容并提供辅助。\n"
            "可以在聊天中直接向我提问！"
        )


# ─── CLI ────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Meeting Bot — AI 会议机器人")
    sub = parser.add_subparsers(dest="command")

    # join
    p_join = sub.add_parser("join", help="加入会议")
    p_join.add_argument("meeting_url", help="会议链接 (Zoom/Teams/Meet)")
    p_join.add_argument("--name", default=None, help="Bot 显示名称")

    # leave
    sub.add_parser("leave", help="离开会议")

    # status
    sub.add_parser("status", help="查看 Bot 状态")

    # chat
    p_chat = sub.add_parser("chat", help="发送聊天消息")
    p_chat.add_argument("message", help="消息内容")

    # read-chat
    sub.add_parser("read-chat", help="读取聊天记录")

    # transcript
    sub.add_parser("transcript", help="获取转录文本")

    # screenshot
    p_ss = sub.add_parser("screenshot", help="获取会议截图")
    p_ss.add_argument("--output", "-o", help="保存路径")

    # assist — 完整 AI 助手模式
    p_assist = sub.add_parser("assist", help="启动 AI 会议助手")
    p_assist.add_argument("meeting_url", help="会议链接")
    p_assist.add_argument("--mode", choices=["general", "medical"], default="general")
    p_assist.add_argument("--interval", type=int, default=30, help="分析间隔（秒）")

    # list
    sub.add_parser("list", help="列出活跃 Bot")

    # setup
    sub.add_parser("setup", help="检查 Vexa 服务状态")

    args = parser.parse_args()
    config = load_config()
    bot = MeetingBot(config)

    if args.command == "join":
        bot.join(args.meeting_url, bot_name=args.name)
        print(f"Bot ID: {bot.bot_id}")

    elif args.command == "leave":
        # Load bot_id from session
        bot.bot_id = _load_active_bot_id()
        bot.leave()

    elif args.command == "status":
        bot.bot_id = _load_active_bot_id()
        st = bot.status()
        print(json.dumps(st, indent=2, ensure_ascii=False))

    elif args.command == "chat":
        bot.bot_id = _load_active_bot_id()
        bot.send_chat(args.message)

    elif args.command == "read-chat":
        bot.bot_id = _load_active_bot_id()
        messages = bot.read_chat()
        for m in messages:
            sender = m.get("sender", m.get("from", "?"))
            text = m.get("text", m.get("message", ""))
            print(f"  {sender}: {text}")

    elif args.command == "transcript":
        bot.bot_id = _load_active_bot_id()
        print(bot.get_full_transcript_text())

    elif args.command == "screenshot":
        bot.bot_id = _load_active_bot_id()
        path = bot.get_screenshot(args.output)
        if path:
            print(f"Saved: {path}")

    elif args.command == "assist":
        assistant = MeetingAssistantLoop(bot, config)
        assistant.start(args.meeting_url, mode=args.mode, interval=args.interval)

    elif args.command == "list":
        bots = bot.list_bots()
        print(json.dumps(bots, indent=2, ensure_ascii=False))

    elif args.command == "setup":
        _check_vexa_setup(config)

    else:
        parser.print_help()


def _load_active_bot_id():
    """从最近的 session 文件加载 bot_id。"""
    recordings = SKILL_DIR / "recordings"
    if not recordings.exists():
        return None
    sessions = sorted(recordings.glob("bot_*/session.json"), reverse=True)
    for s in sessions:
        with open(s) as f:
            data = json.load(f)
        if data.get("bot_id"):
            return data["bot_id"]
    return None


def _check_vexa_setup(config):
    """检查 Vexa 服务是否运行。"""
    import sys
    # Windows GBK terminal safe output
    def safe_print(s):
        try:
            print(s)
        except UnicodeEncodeError:
            print(s.encode('ascii', 'replace').decode('ascii'))

    bot_cfg = config.get("bot", {})
    url = bot_cfg.get("vexa_url", "http://localhost:8056")

    safe_print(f"Checking Vexa at: {url}")
    try:
        resp = requests.get(f"{url}/health", timeout=5)
        if resp.ok:
            safe_print(f"  [OK] Vexa is running")
            safe_print(f"  Response: {resp.json()}")
        else:
            safe_print(f"  [FAIL] Vexa responded with {resp.status_code}")
    except requests.ConnectionError:
        safe_print(f"  [FAIL] Cannot connect to Vexa at {url}")
        safe_print(f"\n  To start Vexa (docker-compose):")
        safe_print(f"    cd skills/meeting-assistant && docker compose up -d")
        safe_print(f"\n  Or manually:")
        safe_print(f"    docker run -d --name vexa -p 8056:8056 vexaai/vexa-lite:latest")
    except Exception as e:
        safe_print(f"  [ERROR] {e}")


if __name__ == "__main__":
    main()
