#!/usr/bin/env python3
"""
IMA Event Stream Module - JSON Lines Format for Agent Integration

This module provides structured event streaming for real-time progress tracking
and interactive verification. Events are emitted as JSON Lines (one JSON per line)
to stdout, allowing agents to parse and relay information to users.

Event Types:
- task_preview: Pre-execution task summary
- progress: Execution progress updates (every 30-45s)
- info: General information messages
- warning: Warning messages
- error: Error messages
- prompt: User input required (interactive verification)
- result: Final execution result

Usage:
    from ima_events import emit_event, emit_task_preview, emit_progress, emit_prompt
    
    # Task preview
    emit_task_preview({
        "model": "ima-pro",
        "task_type": "reference_image_to_video",
        "duration": "15s",
        "size": "9:16",
        "credit": 105,
        "estimated_time": "4-6 minutes"
    })
    
    # Progress update
    emit_progress(percent=50, elapsed=120, message="Generating video...")
    
    # User prompt
    response = emit_prompt("Asset contains human face. Continue?", ["yes", "no"])
"""

import sys
import json
import time
import os
from typing import Any, Literal

EventType = Literal["task_preview", "progress", "info", "warning", "error", "prompt", "result"]


def emit_event(event_type: EventType, data: dict[str, Any], message: str = "") -> None:
    """
    Emit a structured event to stdout as JSON Line.
    
    Args:
        event_type: Type of event
        data: Event-specific data payload
        message: Human-readable message
    """
    event = {
        "type": event_type,
        "timestamp": time.time(),
        "message": message,
        "data": data
    }
    
    # Output as single line JSON
    print(json.dumps(event, ensure_ascii=False), flush=True)


def structured_stdout_only() -> bool:
    """
    Whether stdout should contain only structured JSON events.

    Modes:
    - IMA_STDOUT_MODE=events: always JSON events only on stdout
    - IMA_STDOUT_MODE=mixed: allow human text on stdout
    - IMA_STDOUT_MODE=auto: events-only when stdout is not a TTY
    """
    mode = os.getenv("IMA_STDOUT_MODE", "events").strip().lower()
    if mode == "events":
        return True
    if mode == "mixed":
        return False
    return not sys.stdout.isatty()


def human_print(*args, **kwargs) -> None:
    """
    Print human-readable text without polluting JSON event stdout in stream mode.
    """
    if "file" in kwargs:
        print(*args, **kwargs)
        return

    target = sys.stderr if structured_stdout_only() else sys.stdout
    print(*args, file=target, **kwargs)


def emit_task_preview(
    model: str,
    task_type: str,
    duration: str | None = None,
    size: str | None = None,
    credit: int = 0,
    estimated_time: str = "4-6 minutes",
    environment: str = "production"
) -> None:
    """
    Emit task preview event before execution starts.
    
    This satisfies SKILL.md Rule 2: "ALWAYS inform user BEFORE execution"
    
    Args:
        environment: Fixed to "production" for production-only build
    """
    data = {
        "model": model,
        "task_type": task_type,
        "credit": credit,
        "estimated_time": estimated_time,
        "environment": "production"  # Always production in this build
    }
    
    if duration:
        data["duration"] = duration
    if size:
        data["size"] = size
    
    emit_event(
        "task_preview",
        data,
        f"Task Preview: {model} | {task_type} | {credit} pts | Est. {estimated_time}"
    )


def emit_progress(percent: int, elapsed: int, message: str, stage: str = "") -> None:
    """
    Emit progress update event.
    
    This satisfies SKILL.md Rule 3: "SEND progress updates every 30-45s"
    
    Args:
        percent: Completion percentage (0-100)
        elapsed: Elapsed time in seconds
        message: Progress message
        stage: Current execution stage (e.g., "uploading", "creating", "polling")
    """
    data = {
        "percent": percent,
        "elapsed": elapsed,
        "stage": stage
    }
    
    emit_event("progress", data, message)


def emit_info(message: str, **kwargs) -> None:
    """Emit informational message."""
    emit_event("info", kwargs, message)


def emit_warning(message: str, **kwargs) -> None:
    """Emit warning message."""
    emit_event("warning", kwargs, message)


def emit_error(message: str, error_code: str | None = None, **kwargs) -> None:
    """Emit error message."""
    data = kwargs.copy()
    if error_code:
        data["error_code"] = error_code
    emit_event("error", data, message)


def emit_result(
    success: bool,
    task_id: str | None = None,
    url: str | None = None,
    cover_url: str | None = None,
    message: str = ""
) -> None:
    """
    Emit final result event.
    
    This satisfies SKILL.md Rule 5: "SEND results properly - Video + metadata"
    """
    data = {
        "success": success
    }
    
    if task_id:
        data["task_id"] = task_id
    if url:
        data["url"] = url
    if cover_url:
        data["cover_url"] = cover_url
    
    emit_event("result", data, message)


def emit_prompt(
    message: str,
    options: list[str],
    default: str | None = None,
    timeout: int | None = None
) -> str:
    """
    Emit interactive prompt and wait for user response.
    
    This satisfies SKILL.md Rule 4: "STOP on verification failure - Offer options"
    
    Args:
        message: Prompt message for user
        options: List of valid response options (e.g., ["yes", "no"])
        default: Default option if user doesn't respond (optional)
        timeout: Timeout in seconds (optional)
    
    Returns:
        User's response (one of the options)
    
    Example:
        response = emit_prompt(
            "Asset contains human face. Continue?",
            ["yes", "no"],
            default="no"
        )
    """
    data = {
        "options": options,
        "default": default,
        "timeout": timeout
    }
    
    # Emit prompt event
    emit_event("prompt", data, message)
    
    # For non-interactive environments (e.g., CI/CD), use default
    if not sys.stdin.isatty():
        if default:
            emit_info(f"Non-interactive mode: using default '{default}'")
            return default
        else:
            raise RuntimeError(
                f"Interactive prompt required but stdin is not a TTY: {message}"
            )
    
    # Wait for user input
    while True:
        try:
            # Print prompt to stderr (so it doesn't interfere with event stream)
            print(f"\n❓ {message}", file=sys.stderr)
            print(f"   Options: {' / '.join(options)}", file=sys.stderr)
            if default:
                print(f"   Default: {default} (press Enter)", file=sys.stderr)
            print("   Your choice: ", end="", flush=True, file=sys.stderr)
            
            # Read response
            response = input().strip().lower()
            
            # Handle empty response (use default)
            if not response and default:
                emit_info(f"User selected default: {default}")
                return default
            
            # Validate response
            if response in options:
                emit_info(f"User selected: {response}")
                return response
            else:
                print(f"   ❌ Invalid option. Please choose from: {', '.join(options)}", 
                      file=sys.stderr)
        
        except (EOFError, KeyboardInterrupt):
            # User interrupted (Ctrl+C or Ctrl+D)
            emit_warning("User interrupted prompt")
            if default:
                emit_info(f"Using default: {default}")
                return default
            else:
                raise RuntimeError(f"User interrupted prompt without default option")


# ─── Convenience Functions for Common Patterns ──────────────────────────────

def emit_stage_start(stage: str, message: str = "") -> None:
    """Emit stage start event."""
    emit_info(message or f"Starting stage: {stage}", stage=stage, status="started")


def emit_stage_complete(stage: str, message: str = "") -> None:
    """Emit stage completion event."""
    emit_info(message or f"Completed stage: {stage}", stage=stage, status="completed")


def emit_file_upload(filename: str, index: int, total: int, url: str = "") -> None:
    """Emit file upload progress."""
    emit_info(
        f"Uploaded file [{index}/{total}]: {filename}",
        stage="upload",
        filename=filename,
        index=index,
        total=total,
        url=url
    )


def emit_compliance_check(asset_type: str, status: str, details: dict | None = None) -> None:
    """Emit compliance verification status."""
    data = {
        "asset_type": asset_type,
        "status": status
    }
    if details:
        data.update(details)
    
    emit_info(f"Compliance check: {asset_type} → {status}", **data)


# ─── Event Stream Parser (for Agent consumption) ────────────────────────────

def parse_event_line(line: str) -> dict[str, Any] | None:
    """
    Parse a single event line from the stream.
    
    Args:
        line: JSON line from event stream
    
    Returns:
        Parsed event dict, or None if invalid
    
    Example:
        for line in subprocess.stdout:
            event = parse_event_line(line)
            if event and event["type"] == "progress":
                print(f"Progress: {event['data']['percent']}%")
    """
    try:
        return json.loads(line.strip())
    except (json.JSONDecodeError, ValueError):
        return None


if __name__ == "__main__":
    # Demo: emit sample events
    print("# Demo Event Stream\n", file=sys.stderr)
    
    emit_task_preview(
        model="ima-pro",
        task_type="text_to_video",
        duration="15s",
        size="16:9",
        credit=105,
        estimated_time="4-6 minutes"
    )
    
    time.sleep(0.5)
    emit_stage_start("upload", "Uploading input media...")
    emit_file_upload("image1.jpg", 1, 2, "https://cdn.example.com/img1.jpg")
    emit_file_upload("image2.jpg", 2, 2, "https://cdn.example.com/img2.jpg")
    emit_stage_complete("upload", "All media uploaded")
    
    time.sleep(0.5)
    emit_stage_start("verify", "Running compliance verification...")
    emit_compliance_check("image", "pending", {"contains_face": True})
    
    # Interactive prompt demo
    try:
        response = emit_prompt(
            "Asset contains human face. Continue?",
            ["yes", "no"],
            default="no",
            timeout=30
        )
        emit_compliance_check("image", "approved" if response == "yes" else "rejected")
    except RuntimeError as e:
        emit_error(str(e))
    
    time.sleep(0.5)
    emit_stage_start("create", "Creating video generation task...")
    emit_progress(25, 30, "Initializing generation...", "create")
    emit_progress(50, 60, "Generating frames...", "polling")
    emit_progress(75, 90, "Rendering video...", "polling")
    emit_progress(100, 120, "Finalizing...", "polling")
    
    time.sleep(0.5)
    emit_result(
        success=True,
        task_id="task_12345",
        url="https://cdn.example.com/video.mp4",
        cover_url="https://cdn.example.com/cover.jpg",
        message="Video generated successfully"
    )
