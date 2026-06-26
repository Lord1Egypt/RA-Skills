#!/usr/bin/env python3
"""Run OpenCode and mirror progress into a Discord thread."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import textwrap
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DISCORD_API_BASE = "https://discord.com/api/v10"
DISCORD_LIMIT = 1900
STATUS_PREVIEW_LINES = 12
DEFAULT_ARCHIVE_MINUTES = 1440


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run OpenCode and mirror progress into a Discord thread."
    )
    parser.add_argument("--repo", required=True, help="Repository working directory.")
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt passed to OpenCode.")
    prompt_group.add_argument("--prompt-file", help="File containing the prompt.")

    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("--thread-id", help="Existing Discord thread id.")
    target_group.add_argument(
        "--parent-channel-id",
        help="Parent text channel id used to create a new public thread.",
    )
    parser.add_argument(
        "--thread-name",
        default="OpenCode session",
        help="Thread title when creating a new thread.",
    )
    parser.add_argument(
        "--starter-message",
        default="Starting an OpenCode run. Live updates will follow in this thread.",
        help="Starter message used when creating a new thread.",
    )
    parser.add_argument(
        "--auto-archive-duration",
        type=int,
        default=DEFAULT_ARCHIVE_MINUTES,
        choices=(60, 1440, 4320, 10080),
        help="Discord thread auto archive duration in minutes.",
    )
    parser.add_argument("--attach", help="Attach to a warm opencode serve URL.")
    parser.add_argument("--model", help="OpenCode model id in provider/model form.")
    parser.add_argument("--agent", help="Optional OpenCode agent id.")
    parser.add_argument("--session", help="Continue the specified OpenCode session id.")
    parser.add_argument(
        "--continue-last",
        action="store_true",
        help="Continue the last OpenCode session.",
    )
    parser.add_argument(
        "--opencode-bin",
        default="opencode",
        help="OpenCode executable path.",
    )
    parser.add_argument(
        "--opencode-arg",
        action="append",
        default=[],
        help="Additional argument appended to `opencode run`.",
    )
    parser.add_argument(
        "--update-interval",
        type=float,
        default=3.0,
        help="Seconds between Discord status edits.",
    )
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="Print the final OpenCode command before execution.",
    )
    return parser.parse_args()


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt.strip()
    return Path(args.prompt_file).read_text(encoding="utf-8").strip()


def chunk_text(text: str, limit: int = DISCORD_LIMIT) -> list[str]:
    text = text.strip()
    if not text:
        return []
    chunks: list[str] = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break
        split_at = text.rfind("\n", 0, limit)
        if split_at <= 0:
            split_at = text.rfind(" ", 0, limit)
        if split_at <= 0:
            split_at = limit
        chunks.append(text[:split_at].rstrip())
        text = text[split_at:].lstrip()
    return chunks


def shorten(value: str, limit: int = 400) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def extract_text(value: Any) -> list[str]:
    results: list[str] = []
    if value is None:
        return results
    if isinstance(value, str):
        stripped = value.strip()
        if stripped:
            results.append(stripped)
        return results
    if isinstance(value, list):
        for item in value:
            results.extend(extract_text(item))
        return results
    if isinstance(value, dict):
        preferred_keys = (
            "text",
            "delta",
            "content",
            "message",
            "summary",
            "error",
            "input",
            "output",
            "name",
            "tool",
            "title",
        )
        for key in preferred_keys:
            if key in value:
                results.extend(extract_text(value[key]))
        for item in value.values():
            if isinstance(item, (dict, list)):
                results.extend(extract_text(item))
        return results
    return results


def summarize_event(event: dict[str, Any]) -> str:
    event_type = (
        event.get("type")
        or event.get("event")
        or event.get("kind")
        or event.get("name")
        or "event"
    )
    fragments = extract_text(event)
    if fragments:
        summary = shorten(" | ".join(dict.fromkeys(fragments)))
        return f"[{event_type}] {summary}"
    return f"[{event_type}]"


class DiscordClient:
    def __init__(self, token: str):
        self.token = token

    def _request(
        self, method: str, path: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"{DISCORD_API_BASE}{path}"
        data = None
        headers = {
            "Authorization": f"Bot {self.token}",
            "User-Agent": "openclaw-opencode-discord-bridge/1.0",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Discord API {method} {path} failed: {message}") from exc
        return json.loads(body) if body else {}

    def create_message(self, channel_id: str, content: str) -> dict[str, Any]:
        return self._request(
            "POST", f"/channels/{channel_id}/messages", {"content": content}
        )

    def edit_message(self, channel_id: str, message_id: str, content: str) -> dict[str, Any]:
        return self._request(
            "PATCH",
            f"/channels/{channel_id}/messages/{message_id}",
            {"content": content},
        )

    def create_public_thread_from_message(
        self,
        channel_id: str,
        message_id: str,
        name: str,
        auto_archive_duration: int,
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/channels/{channel_id}/messages/{message_id}/threads",
            {
                "name": name,
                "auto_archive_duration": auto_archive_duration,
            },
        )


def ensure_repo(path: str) -> str:
    repo = Path(path).expanduser().resolve()
    if not repo.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo}")
    if not repo.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {repo}")
    return str(repo)


def ensure_opencode(binary: str) -> str:
    resolved = shutil.which(binary) if os.path.sep not in binary else binary
    if not resolved or not Path(resolved).exists():
        raise FileNotFoundError(
            f"OpenCode executable not found: {binary}. Install OpenCode first."
        )
    return resolved


def build_opencode_command(
    args: argparse.Namespace, opencode_bin: str, prompt: str
) -> list[str]:
    cmd = [opencode_bin, "run", "--format", "json"]
    if args.attach:
        cmd.extend(["--attach", args.attach])
    if args.model:
        cmd.extend(["--model", args.model])
    if args.agent:
        cmd.extend(["--agent", args.agent])
    if args.session:
        cmd.extend(["--session", args.session])
    if args.continue_last:
        cmd.append("--continue")
    for item in args.opencode_arg:
        cmd.append(item)
    cmd.append(prompt)
    return cmd


def create_thread_if_needed(
    discord: DiscordClient, args: argparse.Namespace, header_text: str
) -> str:
    if args.thread_id:
        discord.create_message(args.thread_id, header_text)
        return args.thread_id

    starter = discord.create_message(args.parent_channel_id, args.starter_message)
    thread = discord.create_public_thread_from_message(
        args.parent_channel_id,
        starter["id"],
        args.thread_name,
        args.auto_archive_duration,
    )
    discord.create_message(thread["id"], header_text)
    return thread["id"]


def render_status(
    state: dict[str, Any],
    prompt: str,
    command: list[str],
    done: bool = False,
) -> str:
    heading = "OpenCode run finished" if done else "OpenCode run in progress"
    preview = "\n".join(state["lines"][-STATUS_PREVIEW_LINES:]) or "(waiting for events)"
    stderr_preview = "\n".join(state["stderr"][-6:])
    result = textwrap.dedent(
        f"""
        {heading}

        Repo: `{state["repo"]}`
        Model: `{state["model"]}`
        Command: `{shlex.join(command)}`
        Prompt: `{shorten(prompt, 180)}`
        Events: `{state["event_count"]}`

        Recent events:
        {preview}
        """
    ).strip()
    if stderr_preview:
        result += "\n\nstderr:\n" + stderr_preview
    return result[:DISCORD_LIMIT]


def reader_thread(pipe: Any, sink: list[str], prefix: str) -> None:
    try:
        for raw_line in iter(pipe.readline, ""):
            line = raw_line.strip()
            if line:
                sink.append(f"{prefix}{shorten(line, 300)}")
    finally:
        pipe.close()


def main() -> int:
    args = parse_args()
    prompt = read_prompt(args)
    if not prompt:
        raise SystemExit("Prompt is empty.")

    repo = ensure_repo(args.repo)
    opencode_bin = ensure_opencode(args.opencode_bin)

    discord_token = os.environ.get("DISCORD_BOT_TOKEN")
    if not discord_token:
        raise SystemExit("DISCORD_BOT_TOKEN is required.")

    discord = DiscordClient(discord_token)
    command = build_opencode_command(args, opencode_bin, prompt)

    if args.print_command:
        print(shlex.join(command))

    model_label = args.model or "default-configured"
    header_text = textwrap.dedent(
        f"""
        OpenCode bridge started.
        Repo: `{repo}`
        Model: `{model_label}`
        Prompt: `{shorten(prompt, 240)}`
        """
    ).strip()

    thread_id = create_thread_if_needed(discord, args, header_text)
    status_message = discord.create_message(thread_id, "OpenCode run queued.")

    state: dict[str, Any] = {
        "repo": repo,
        "model": model_label,
        "event_count": 0,
        "lines": [],
        "stderr": [],
    }

    process = subprocess.Popen(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )

    stderr_thread = threading.Thread(
        target=reader_thread, args=(process.stderr, state["stderr"], "[stderr] "), daemon=True
    )
    stderr_thread.start()

    last_update = 0.0
    transcript: list[str] = []

    try:
        assert process.stdout is not None
        for raw_line in iter(process.stdout.readline, ""):
            line = raw_line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                summary = f"[raw] {shorten(line, 400)}"
            else:
                summary = summarize_event(event)
                transcript.extend(extract_text(event))
            state["event_count"] += 1
            state["lines"].append(summary)
            now = time.time()
            if now - last_update >= args.update_interval:
                discord.edit_message(
                    thread_id,
                    status_message["id"],
                    render_status(state, prompt, command, done=False),
                )
                last_update = now
    finally:
        if process.stdout is not None:
            process.stdout.close()

    return_code = process.wait()
    stderr_thread.join(timeout=1.0)

    done_status = render_status(state, prompt, command, done=True)
    if return_code != 0:
        done_status += f"\n\nExit code: `{return_code}`"
    discord.edit_message(thread_id, status_message["id"], done_status[:DISCORD_LIMIT])

    transcript_text = "\n".join(dict.fromkeys(item for item in transcript if item.strip()))
    final_summary = (
        f"OpenCode exited with code `{return_code}` after `{state['event_count']}` events."
    )
    discord.create_message(thread_id, final_summary)

    for chunk in chunk_text(transcript_text):
        discord.create_message(thread_id, chunk)

    return return_code


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"error: {exc}", file=sys.stderr)
        raise
