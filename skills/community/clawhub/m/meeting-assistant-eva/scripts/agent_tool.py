#!/usr/bin/env python3
"""
Meeting Assistant — Tool Interface for Claude Code & OpenClaw

This module exposes the meeting assistant as callable tools that can be used:
  1. By Claude Code directly (via Bash tool calling this script)
  2. By OpenClaw agents (imported as Python module)
  3. Via the Anthropic tool_use API format (tool_definitions())

Usage as CLI (returns JSON):
  python agent_tool.py start "https://zoom.us/j/123?pwd=xxx" --mode medical
  python agent_tool.py status
  python agent_tool.py chat "What was just prescribed?"
  python agent_tool.py transcript
  python agent_tool.py screenshot
  python agent_tool.py stop

Usage as Python:
  from agent_tool import MeetingAssistantTool
  tool = MeetingAssistantTool()
  result = tool.start_assistant("https://zoom.us/j/123", mode="medical")

Usage with Anthropic tool_use:
  from agent_tool import tool_definitions
  tools = tool_definitions()  # pass to client.messages.create(tools=tools)
"""

import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
STATE_FILE = SKILL_DIR / ".assistant_state.json"
DAEMON_LOG = SKILL_DIR / ".assistant_daemon.log"


def _load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def _ok(data: dict) -> dict:
    return {"status": "ok", **data}


def _err(message: str) -> dict:
    return {"status": "error", "error": message}


def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def _clear_state():
    STATE_FILE.unlink(missing_ok=True)


# ─── MeetingAssistantTool ─────────────────────────────────────────────────────

class MeetingAssistantTool:
    """
    High-level tool interface to the meeting assistant.

    All methods return a dict with at least {"status": "ok"|"error"}.
    This class can be instantiated by any agent to control the meeting assistant.
    """

    def __init__(self):
        self.config = _load_config()

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def start_assistant(
        self,
        meeting_url: str,
        mode: str = "general",
        interval: int = 30,
        bot_name: str | None = None,
    ) -> dict:
        """
        Join a meeting and start the AI assistant loop as a background daemon.

        Args:
            meeting_url: Zoom/Teams/Meet URL
            mode:        "general" or "medical"
            interval:    Analysis cycle interval in seconds (default 30)
            bot_name:    Display name for the bot in the meeting

        Returns:
            {"status": "ok", "pid": int, "session_dir": str, "message": str}
        """
        state = _load_state()
        if state.get("pid"):
            try:
                os.kill(state["pid"], 0)  # Check if process exists
                return _err(f"Assistant already running (PID {state['pid']}). Call stop() first.")
            except ProcessLookupError:
                _clear_state()

        python = self.config.get("conda_env", {}).get("python", sys.executable)
        bot_script = Path(__file__).parent / "meeting_bot.py"

        cmd = [
            python, str(bot_script),
            "assist", meeting_url,
            "--mode", mode,
            "--interval", str(interval),
        ]
        if bot_name:
            cmd += ["--name", bot_name]

        log_file = open(DAEMON_LOG, "w", encoding="utf-8")
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                cwd=str(SKILL_DIR),
                env={**os.environ},
            )
        except Exception as e:
            return _err(f"Failed to start assistant: {e}")

        state = {
            "pid": proc.pid,
            "meeting_url": meeting_url,
            "mode": mode,
            "interval": interval,
            "started_at": datetime.now().isoformat(),
            "log_file": str(DAEMON_LOG),
        }
        _save_state(state)

        # Give it a moment to start
        time.sleep(2)

        return _ok({
            "pid": proc.pid,
            "message": f"Assistant starting (PID {proc.pid}). Bot joining {meeting_url}...",
            "mode": mode,
            "log": str(DAEMON_LOG),
        })

    def stop_assistant(self) -> dict:
        """
        Stop the running assistant daemon gracefully.

        Returns:
            {"status": "ok", "message": str}
        """
        state = _load_state()
        pid = state.get("pid")

        if not pid:
            return _err("No active assistant session found.")

        try:
            os.kill(pid, signal.SIGINT)
            # Wait for graceful shutdown
            for _ in range(15):
                time.sleep(1)
                try:
                    os.kill(pid, 0)
                except ProcessLookupError:
                    break
            else:
                # Force kill if still alive
                try:
                    os.kill(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
        except ProcessLookupError:
            pass

        _clear_state()
        return _ok({"message": f"Assistant stopped (was PID {pid})"})

    def get_status(self) -> dict:
        """
        Get the current assistant and bot status.

        Returns:
            {"status": "ok", "running": bool, "pid": int|None, "bot_status": dict|None, ...}
        """
        state = _load_state()
        pid = state.get("pid")
        running = False

        if pid:
            try:
                os.kill(pid, 0)
                running = True
            except ProcessLookupError:
                _clear_state()
                state = {}

        # Try to get Vexa bot status
        bot_status = None
        session_info = self._get_latest_session()
        if session_info:
            bot_id = session_info.get("bot_id")
            if bot_id:
                try:
                    import requests
                    cfg = self.config.get("bot", {})
                    url = cfg.get("vexa_url", "http://localhost:8056")
                    headers = {}
                    if cfg.get("vexa_api_key"):
                        headers["X-API-Key"] = cfg["vexa_api_key"]
                    resp = requests.get(f"{url}/bots/{bot_id}", headers=headers, timeout=5)
                    if resp.ok:
                        bot_status = resp.json()
                except Exception:
                    pass

        return _ok({
            "running": running,
            "pid": pid if running else None,
            "meeting_url": state.get("meeting_url"),
            "mode": state.get("mode"),
            "started_at": state.get("started_at"),
            "bot_status": bot_status,
            "session": session_info,
        })

    # ── Meeting Interaction ────────────────────────────────────────────────

    def send_chat(self, message: str) -> dict:
        """
        Send a message to the meeting chat via the active bot.

        Args:
            message: Text to send to the meeting chat

        Returns:
            {"status": "ok", "message": str}
        """
        python = self.config.get("conda_env", {}).get("python", sys.executable)
        bot_script = Path(__file__).parent / "meeting_bot.py"

        result = subprocess.run(
            [python, str(bot_script), "chat", message],
            capture_output=True, text=True, timeout=15, cwd=str(SKILL_DIR),
        )
        if result.returncode != 0:
            return _err(result.stderr or result.stdout)
        return _ok({"message": f"Sent: {message[:80]}"})

    def get_transcript(self, max_entries: int = 50) -> dict:
        """
        Get the current meeting transcript.

        Returns:
            {"status": "ok", "entries": list, "text": str}
        """
        python = self.config.get("conda_env", {}).get("python", sys.executable)
        bot_script = Path(__file__).parent / "meeting_bot.py"

        result = subprocess.run(
            [python, str(bot_script), "transcript"],
            capture_output=True, text=True, timeout=15, cwd=str(SKILL_DIR),
        )
        text = result.stdout.strip()

        # Also try to read from transcript_log.json
        session = self._get_latest_session_dir()
        entries = []
        if session:
            log = session / "transcript_log.json"
            if log.exists():
                try:
                    all_entries = json.loads(log.read_text(encoding="utf-8"))
                    entries = all_entries[-max_entries:]
                except Exception:
                    pass

        return _ok({"text": text, "entries": entries, "count": len(entries)})

    def get_screenshot(self, save_path: str | None = None) -> dict:
        """
        Capture the current meeting view.

        Returns:
            {"status": "ok", "path": str}
        """
        python = self.config.get("conda_env", {}).get("python", sys.executable)
        bot_script = Path(__file__).parent / "meeting_bot.py"

        cmd = [python, str(bot_script), "screenshot"]
        if save_path:
            cmd += ["--output", save_path]

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=20, cwd=str(SKILL_DIR),
        )
        if result.returncode != 0:
            return _err(result.stderr or result.stdout)

        # Extract path from output
        path = None
        for line in result.stdout.split("\n"):
            if "Saved:" in line or ".png" in line:
                path = line.split("Saved:")[-1].strip()
                break

        return _ok({"path": path, "output": result.stdout.strip()})

    def read_chat(self) -> dict:
        """
        Read meeting chat messages.

        Returns:
            {"status": "ok", "messages": list}
        """
        python = self.config.get("conda_env", {}).get("python", sys.executable)
        bot_script = Path(__file__).parent / "meeting_bot.py"

        result = subprocess.run(
            [python, str(bot_script), "read-chat"],
            capture_output=True, text=True, timeout=15, cwd=str(SKILL_DIR),
        )
        messages = [line for line in result.stdout.strip().split("\n") if line.strip()]
        return _ok({"messages": messages, "count": len(messages)})

    def get_session_summary(self) -> dict:
        """
        Get or generate the meeting summary for the latest session.

        Returns:
            {"status": "ok", "summary": str, "path": str}
        """
        session_dir = self._get_latest_session_dir()
        if not session_dir:
            return _err("No session found")

        summary_path = session_dir / "meeting_summary.md"
        if summary_path.exists():
            return _ok({
                "summary": summary_path.read_text(encoding="utf-8"),
                "path": str(summary_path),
            })

        return _err(f"No summary yet. Session dir: {session_dir}")

    def get_logs(self, lines: int = 50) -> dict:
        """Get recent daemon log lines."""
        if not DAEMON_LOG.exists():
            return _ok({"lines": [], "message": "No daemon log found"})
        try:
            all_lines = DAEMON_LOG.read_text(encoding="utf-8", errors="replace").split("\n")
            recent = all_lines[-lines:]
            return _ok({"lines": recent, "total_lines": len(all_lines)})
        except Exception as e:
            return _err(str(e))

    # ── Helpers ────────────────────────────────────────────────────────────

    def _get_latest_session(self) -> dict | None:
        recordings = SKILL_DIR / "recordings"
        if not recordings.exists():
            return None
        sessions = sorted(recordings.glob("bot_*/session.json"), reverse=True)
        for s in sessions:
            try:
                return json.loads(s.read_text(encoding="utf-8"))
            except Exception:
                continue
        return None

    def _get_latest_session_dir(self) -> Path | None:
        recordings = SKILL_DIR / "recordings"
        if not recordings.exists():
            return None
        sessions = sorted(recordings.glob("bot_*"), reverse=True)
        return sessions[0] if sessions else None


# ─── Anthropic Tool Definitions ───────────────────────────────────────────────

def tool_definitions() -> list[dict]:
    """
    Returns Anthropic tool_use format definitions for the meeting assistant.
    Use with: client.messages.create(tools=tool_definitions(), ...)

    Example:
        import anthropic
        from agent_tool import tool_definitions
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            tools=tool_definitions(),
            messages=[{"role": "user", "content": "Join this meeting: https://zoom.us/j/123"}]
        )
    """
    return [
        {
            "name": "meeting_start",
            "description": (
                "Join a video meeting (Zoom/Teams/Google Meet) and start the AI assistant. "
                "The bot will participate in the meeting, transcribe audio, analyze content, "
                "and respond to participant questions via meeting chat."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "meeting_url": {
                        "type": "string",
                        "description": "Full meeting URL (Zoom, Teams, or Google Meet)",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["general", "medical"],
                        "description": "Assistant mode. 'medical' enables medical terminology support and patient summaries.",
                        "default": "general",
                    },
                    "interval": {
                        "type": "integer",
                        "description": "Analysis cycle interval in seconds (default 30)",
                        "default": 30,
                    },
                    "bot_name": {
                        "type": "string",
                        "description": "Display name for the bot in the meeting",
                    },
                },
                "required": ["meeting_url"],
            },
        },
        {
            "name": "meeting_stop",
            "description": (
                "Stop the AI meeting assistant, generate a final meeting summary, "
                "and leave the meeting. Should be called after the meeting ends."
            ),
            "input_schema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "meeting_status",
            "description": "Get the current status of the meeting assistant and bot.",
            "input_schema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "meeting_send_chat",
            "description": "Send a message to the meeting chat on behalf of the assistant bot.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to send to the meeting chat",
                    }
                },
                "required": ["message"],
            },
        },
        {
            "name": "meeting_get_transcript",
            "description": "Get the current meeting transcript (recent conversation).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "max_entries": {
                        "type": "integer",
                        "description": "Maximum number of transcript entries to return",
                        "default": 50,
                    }
                },
            },
        },
        {
            "name": "meeting_screenshot",
            "description": "Capture the current meeting view as a screenshot.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "save_path": {
                        "type": "string",
                        "description": "Optional file path to save the screenshot",
                    }
                },
            },
        },
        {
            "name": "meeting_read_chat",
            "description": "Read all chat messages from the current meeting.",
            "input_schema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "meeting_get_summary",
            "description": "Get the meeting summary (available after meeting ends or after analysis).",
            "input_schema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "meeting_get_logs",
            "description": "Get recent assistant daemon logs for debugging.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "lines": {
                        "type": "integer",
                        "description": "Number of recent log lines to return",
                        "default": 50,
                    }
                },
            },
        },
    ]


def handle_tool_call(tool_name: str, tool_input: dict) -> dict:
    """
    Execute a tool call from the Anthropic tool_use API.

    Args:
        tool_name:  Name from tool_definitions()
        tool_input: Input dict matching the tool's input_schema

    Returns:
        dict result to return as tool_result content
    """
    tool = MeetingAssistantTool()
    dispatch = {
        "meeting_start":         lambda: tool.start_assistant(**tool_input),
        "meeting_stop":          lambda: tool.stop_assistant(),
        "meeting_status":        lambda: tool.get_status(),
        "meeting_send_chat":     lambda: tool.send_chat(tool_input["message"]),
        "meeting_get_transcript":lambda: tool.get_transcript(**tool_input),
        "meeting_screenshot":    lambda: tool.get_screenshot(**tool_input),
        "meeting_read_chat":     lambda: tool.read_chat(),
        "meeting_get_summary":   lambda: tool.get_session_summary(),
        "meeting_get_logs":      lambda: tool.get_logs(**tool_input),
    }

    handler = dispatch.get(tool_name)
    if not handler:
        return _err(f"Unknown tool: {tool_name}")

    try:
        return handler()
    except Exception as e:
        return _err(f"Tool execution error: {e}")


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Meeting Assistant Tool — CLI Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  start <url>          Join meeting and start AI assistant
  stop                 Stop assistant and generate summary
  status               Check assistant status
  chat <message>       Send message to meeting chat
  transcript           Get meeting transcript
  screenshot           Capture meeting screenshot
  read-chat            Read all meeting chat messages
  summary              Get meeting summary
  logs                 Get assistant logs
  tool-defs            Print Anthropic tool definitions (JSON)

All commands return JSON output.
        """,
    )

    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start", help="Start AI meeting assistant")
    p_start.add_argument("meeting_url", help="Meeting URL")
    p_start.add_argument("--mode", choices=["general", "medical"], default="general")
    p_start.add_argument("--interval", type=int, default=30)
    p_start.add_argument("--bot-name", dest="bot_name", default=None)

    sub.add_parser("stop", help="Stop assistant")
    sub.add_parser("status", help="Get status")

    p_chat = sub.add_parser("chat", help="Send chat message")
    p_chat.add_argument("message")

    p_transcript = sub.add_parser("transcript", help="Get transcript")
    p_transcript.add_argument("--max", type=int, default=50, dest="max_entries")

    p_screenshot = sub.add_parser("screenshot", help="Take screenshot")
    p_screenshot.add_argument("--output", default=None, dest="save_path")

    sub.add_parser("read-chat", help="Read chat messages")
    sub.add_parser("summary", help="Get meeting summary")

    p_logs = sub.add_parser("logs", help="Get daemon logs")
    p_logs.add_argument("--lines", type=int, default=50)

    sub.add_parser("tool-defs", help="Print Anthropic tool definitions")

    args = parser.parse_args()
    tool = MeetingAssistantTool()

    def output(result):
        print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.command == "start":
        output(tool.start_assistant(
            args.meeting_url,
            mode=args.mode,
            interval=args.interval,
            bot_name=args.bot_name,
        ))
    elif args.command == "stop":
        output(tool.stop_assistant())
    elif args.command == "status":
        output(tool.get_status())
    elif args.command == "chat":
        output(tool.send_chat(args.message))
    elif args.command == "transcript":
        output(tool.get_transcript(args.max_entries))
    elif args.command == "screenshot":
        output(tool.get_screenshot(args.save_path))
    elif args.command == "read-chat":
        output(tool.read_chat())
    elif args.command == "summary":
        output(tool.get_session_summary())
    elif args.command == "logs":
        output(tool.get_logs(args.lines))
    elif args.command == "tool-defs":
        print(json.dumps(tool_definitions(), ensure_ascii=False, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
