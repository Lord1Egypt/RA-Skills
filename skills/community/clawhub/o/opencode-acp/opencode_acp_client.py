#!/usr/bin/env python3
"""
OpenCode ACP Client - Seamless OpenCode collaboration.

Usage:
    python opencode_acp_client.py --project /path/to/project --task "Your task description"
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Optional, Dict, List

from venv_utils import ensure_local_skill_venv

SESSION_STORE_DIR = Path(__file__).resolve().parent / ".acp_sessions"


class OpenCodeACPClient:
    def __init__(self, project_dir: str, verbose: bool = False, quiet: bool = False):
        self.project_dir = project_dir
        self.verbose = verbose
        self.quiet = quiet
        self.process: Optional[subprocess.Popen] = None
        self.stderr_thread: Optional[threading.Thread] = None
        self.session_id: Optional[str] = None
        self.request_id = 0
        self.tool_calls: Dict[str, str] = {}  # tool_call_id -> title
        self.current_response_chunks: List[str] = []

    def drain_stderr(self):
        """Continuously drain stderr to avoid pipe blocking."""
        if not self.process or not self.process.stderr:
            return

        while True:
            line = self.process.stderr.readline()
            if not line:
                break
            text = line.decode(errors="replace").rstrip()
            if text:
                self.log(f"[opencode stderr] {text}")

    def log(self, message: str, force: bool = False):
        """Log message if verbose mode is enabled or force is True."""
        if force or (self.verbose and not self.quiet):
            print(f"[opencode] {message}", file=sys.stderr)

    def output(self, message: str):
        """Output message to stdout (always visible unless quiet)."""
        if not self.quiet:
            print(message)

    def send_request(self, method: str, params: dict) -> dict:
        """Send JSON-RPC request to OpenCode."""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params,
        }
        request_json = json.dumps(request) + "\n"
        self.log(f"→ {method}")
        self.process.stdin.write(request_json.encode())
        self.process.stdin.flush()
        return request

    def read_response(self, timeout: int = 30) -> Optional[dict]:
        """Read JSON-RPC response from OpenCode."""
        start_time = time.time()
        buffer = ""
        
        while time.time() - start_time < timeout:
            try:
                line = self.process.stdout.readline().decode()
                if not line:
                    time.sleep(0.1)
                    continue
                
                buffer += line
                
                try:
                    response = json.loads(buffer)
                    self.log(f"← {response.get('method', 'response')}")
                    return response
                except json.JSONDecodeError:
                    continue
            except Exception as e:
                self.log(f"Error reading: {e}")
                time.sleep(0.1)
        
        return None

    def start(self):
        """Start OpenCode ACP server."""
        self.log("Starting OpenCode...", force=True)
        
        opencode_paths = []
        configured_bin = os.environ.get("OPENCODE_BIN")
        if configured_bin:
            opencode_paths.append(configured_bin)
        opencode_paths.extend([
            "/root/.opencode/bin/opencode",
            "opencode",
        ])

        opencode_bin = None
        for path in opencode_paths:
            if os.path.isabs(path):
                if os.path.exists(path):
                    opencode_bin = path
                    break
                continue

            resolved = shutil.which(path)
            if resolved:
                opencode_bin = resolved
                break
        
        if not opencode_bin:
            raise Exception("OpenCode binary not found")
        
        self.process = subprocess.Popen(
            [opencode_bin, "acp"],
            cwd=self.project_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.stderr_thread = threading.Thread(target=self.drain_stderr, daemon=True)
        self.stderr_thread.start()
        time.sleep(2)

    def initialize(self):
        """Initialize ACP connection."""
        self.log("Initializing connection...")
        self.send_request("initialize", {
            "protocolVersion": 1,
            "clientCapabilities": {
                "fs": {"readTextFile": True, "writeTextFile": True},
                "terminal": True,
            },
            "clientInfo": {
                "name": "Claw",
                "title": "Claw AI Assistant",
                "version": "1.0.0",
            },
        })
        
        response = self.read_response()
        if not response or "result" not in response:
            raise Exception("Failed to initialize")
        
        self.log("Connected ✓", force=True)
        return response

    def create_session(self):
        """Create new OpenCode session."""
        self.log("Creating session...")
        self.send_request("session/new", {
            "cwd": self.project_dir,
            "mcpServers": [],
        })
        
        response = self.read_response()
        if not response or "result" not in response:
            raise Exception("Failed to create session")
        
        self.session_id = response["result"]["sessionId"]
        model = response["result"]["models"]["currentModelId"]
        mode = response["result"]["modes"]["currentModeId"]
        self.log(f"Session ready ({model}, {mode}) ✓", force=True)
        return response

    def send_task(self, task: str):
        """Send task to OpenCode."""
        self.log("Sending task...")
        self.current_response_chunks = []
        self.send_request("session/prompt", {
            "sessionId": self.session_id,
            "prompt": [{"type": "text", "text": task}],
        })

    def handle_session_update(self, update: dict):
        """Handle session update notification."""
        session_update = update.get("sessionUpdate")
        
        if session_update == "agent_message_chunk":
            # Agent output - show it
            content = update.get("content", {})
            if content.get("type") == "text":
                text = content.get("text", "")
                if text and not self.quiet:
                    print(text, end="", flush=True)
                if text:
                    self.current_response_chunks.append(text)
        
        elif session_update == "tool_call":
            # Tool started
            tool_call_id = update.get("toolCallId", "")
            title = update.get("title", "")
            self.tool_calls[tool_call_id] = title
            self.output(f"\n🔧 {title}")
        
        elif session_update == "tool_call_update":
            # Tool status update
            tool_call_id = update.get("toolCallId", "")
            status = update.get("status", "")
            title = self.tool_calls.get(tool_call_id, "tool")
            
            if status == "completed":
                self.output(f"   ✓ {title}")
            elif status == "failed":
                self.output(f"   ✗ {title}")

    def monitor_progress(self, timeout: int = 600):
        """Monitor OpenCode progress until completion."""
        self.log("Working...", force=True)
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = self.read_response(timeout=5)
            if not response:
                continue
            
            # Handle notifications
            if "method" in response:
                method = response["method"]
                params = response.get("params", {})
                
                if method == "session/update":
                    update = params.get("update", {})
                    self.handle_session_update(update)
            
            # Handle response (task completion)
            elif "result" in response:
                result = response["result"]
                stop_reason = result.get("stopReason")
                
                if stop_reason:
                    self.log(f"Completed: {stop_reason}", force=True)
                    
                    # Show usage
                    usage = result.get("usage", {})
                    total = usage.get("totalTokens", 0)
                    cached = usage.get("cachedReadTokens", 0)
                    actual = total - cached
                    self.output(f"\n📊 Tokens: {actual:,} used ({cached:,} cached)")

                    assistant_text = "".join(self.current_response_chunks).strip()
                    if assistant_text:
                        result["assistantText"] = assistant_text
                    
                    return result
        
        self.log("Timeout!", force=True)
        return None

    def stop(self):
        """Stop OpenCode ACP server."""
        if self.process:
            self.log("Stopping...")
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.log("Force killing...")
                self.process.kill()
                self.process.wait()

            if self.stderr_thread and self.stderr_thread.is_alive():
                self.stderr_thread.join(timeout=1)

    def run(self, task: str, timeout: int = 600):
        """Run complete OpenCode collaboration workflow."""
        try:
            self.start_session()
            result = self.run_prompt(task=task, timeout=timeout)
            return result
        finally:
            self.stop()

    def start_session(self):
        """Start ACP process and create a fresh OpenCode session."""
        self.start()
        self.initialize()
        self.create_session()

    def run_prompt(self, task: str, timeout: int = 600):
        """Send a prompt inside current session and wait for completion."""
        self.send_task(task)
        return self.monitor_progress(timeout=timeout)


def sanitize_session_name(name: str) -> str:
    """Restrict session names to a safe filename subset."""
    safe = "".join(ch for ch in name if ch.isalnum() or ch in ("-", "_"))
    if not safe:
        raise ValueError("Session name must contain letters, numbers, '-' or '_'")
    return safe


def session_file_path(session_name: str) -> Path:
    """Return JSON path for persisted conversation session."""
    safe_name = sanitize_session_name(session_name)
    return SESSION_STORE_DIR / f"{safe_name}.json"


def ensure_session_store_dir() -> None:
    """Create local session storage directory if missing."""
    SESSION_STORE_DIR.mkdir(parents=True, exist_ok=True)


def load_persisted_session(session_name: str) -> Optional[dict]:
    """Load persisted session metadata from disk."""
    path = session_file_path(session_name)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def save_persisted_session(session_name: str, data: dict) -> None:
    """Persist session metadata to disk."""
    ensure_session_store_dir()
    path = session_file_path(session_name)
    with path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def build_session_prompt(history: List[dict], user_prompt: str, history_limit: int = 12) -> str:
    """Build a replay prompt so one-shot runs can continue prior context."""
    trimmed = history[-history_limit:] if history_limit > 0 else history
    if not trimmed:
        return user_prompt

    lines = [
        "Continue the conversation using the following prior context.",
        "Conversation history:",
    ]

    for item in trimmed:
        role = item.get("role", "user")
        content = item.get("content", "")
        lines.append(f"{role}: {content}")

    lines.append("user: " + user_prompt)
    return "\n".join(lines)


def run_interactive_mode(client: OpenCodeACPClient, timeout: int, initial_task: Optional[str]) -> int:
    """Run terminal interactive loop in a single ACP session."""
    try:
        client.start_session()
        client.output("Interactive mode ready. Type :exit to quit.")

        if initial_task:
            client.run_prompt(task=initial_task, timeout=timeout)

        while True:
            try:
                prompt = input("\nYou> ").strip()
            except EOFError:
                break

            if not prompt:
                continue
            if prompt in {":exit", ":quit"}:
                break

            result = client.run_prompt(task=prompt, timeout=timeout)
            if not result:
                return 1

        return 0
    finally:
        client.stop()


def run_persisted_session_mode(args: argparse.Namespace) -> int:
    """Run persisted pseudo-interactive session workflow for OpenClaw usage."""
    action = args.session_action
    session_name = args.session_name

    if action == "start":
        if not args.project:
            raise ValueError("--project is required for --session-action start")
        existing = load_persisted_session(session_name)
        if existing:
            raise ValueError(f"Session '{session_name}' already exists")

        now = int(time.time())
        data = {
            "sessionName": session_name,
            "projectDir": args.project,
            "history": [],
            "createdAt": now,
            "updatedAt": now,
        }
        save_persisted_session(session_name, data)
        if not args.quiet:
            print(f"Session '{session_name}' created")
        return 0

    if action == "status":
        data = load_persisted_session(session_name)
        if not data:
            print(f"Session '{session_name}' not found")
            return 1
        if not args.quiet:
            print(f"Session: {data.get('sessionName', session_name)}")
            print(f"Project: {data.get('projectDir', '')}")
            print(f"Turns: {len(data.get('history', []))}")
        return 0

    if action == "stop":
        path = session_file_path(session_name)
        if path.exists():
            path.unlink()
            if not args.quiet:
                print(f"Session '{session_name}' removed")
            return 0
        print(f"Session '{session_name}' not found")
        return 1

    # ask
    if not args.task:
        raise ValueError("--task is required for --session-action ask")

    data = load_persisted_session(session_name)
    if not data:
        raise ValueError(f"Session '{session_name}' not found. Run with --session-action start first")

    project_dir = args.project or data.get("projectDir")
    if not project_dir:
        raise ValueError("No project directory available for this session")

    conversation_prompt = build_session_prompt(
        history=data.get("history", []),
        user_prompt=args.task,
        history_limit=args.history_limit,
    )

    client = OpenCodeACPClient(project_dir=project_dir, verbose=args.verbose, quiet=args.quiet)
    result = client.run(task=conversation_prompt, timeout=args.timeout)
    if not result:
        return 1

    history = data.get("history", [])
    history.append({"role": "user", "content": args.task, "ts": int(time.time())})
    assistant_text = result.get("assistantText", "")
    if assistant_text:
        history.append({"role": "assistant", "content": assistant_text, "ts": int(time.time())})

    data["history"] = history
    data["projectDir"] = project_dir
    data["updatedAt"] = int(time.time())
    save_persisted_session(session_name, data)
    return 0


def main():
    ensure_local_skill_venv()

    parser = argparse.ArgumentParser(
        description="OpenCode ACP Client - Seamless collaboration"
    )
    parser.add_argument(
        "--project",
        required=False,
        help="Project directory path",
    )
    parser.add_argument(
        "--task",
        required=False,
        help="Task description for OpenCode",
    )
    parser.add_argument(
        "--mode",
        choices=["oneshot", "interactive", "session"],
        default="oneshot",
        help="Execution mode: one prompt, terminal interactive loop, or persisted session",
    )
    parser.add_argument(
        "--session-name",
        default="default",
        help="Persisted session name for --mode session",
    )
    parser.add_argument(
        "--session-action",
        choices=["start", "ask", "status", "stop"],
        default="ask",
        help="Action for --mode session",
    )
    parser.add_argument(
        "--history-limit",
        type=int,
        default=12,
        help="How many previous messages to include when replaying persisted sessions",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Task timeout in seconds (default: 600)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode (minimal output)",
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == "oneshot":
            if not args.project or not args.task:
                raise ValueError("--project and --task are required for --mode oneshot")
            client = OpenCodeACPClient(
                project_dir=args.project,
                verbose=args.verbose,
                quiet=args.quiet,
            )
            result = client.run(task=args.task, timeout=args.timeout)
            sys.exit(0 if result else 1)

        if args.mode == "interactive":
            if not args.project:
                raise ValueError("--project is required for --mode interactive")
            client = OpenCodeACPClient(
                project_dir=args.project,
                verbose=args.verbose,
                quiet=args.quiet,
            )
            code = run_interactive_mode(client=client, timeout=args.timeout, initial_task=args.task)
            sys.exit(code)

        code = run_persisted_session_mode(args)
        sys.exit(code)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
