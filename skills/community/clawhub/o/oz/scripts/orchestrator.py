#!/usr/bin/env python3
"""
Oz Agent Pipeline Orchestrator

Chains Oz cloud agent runs in sequence with conditional logic.
No LLM tokens — just REST API calls, polling, and string matching.

Usage:
    python3 orchestrator.py --config pipeline.yaml
    python3 orchestrator.py --env ENV_ID --task "Build X" --stages architect,trading-engineer,security-engineer,red-teamer
"""

import asyncio
import json
import os
import subprocess
import sys
import time
import argparse
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --- Config ---

API_BASE = "https://app.warp.dev/api/v1"
POLL_INTERVAL = 15  # seconds
POLL_TIMEOUT = 5400  # 90 minutes per stage
MAX_RETRIES = 2  # max times to loop back on critical findings

# Override via env: OP_WARP_REFERENCE="op://your-vault/item/field"
OP_REFERENCE = os.environ.get("OP_WARP_REFERENCE", "op://your-vault/warp-api-key/credential")


class Severity(Enum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0


@dataclass
class StageResult:
    stage: str
    run_id: str
    state: str
    status_message: str
    session_link: str
    conversation_id: str
    severity: Severity = Severity.NONE
    raw: dict = field(default_factory=dict)


# --- API helpers ---

def get_api_key() -> str:
    key = os.environ.get("WARP_API_KEY")
    if key:
        return key
    try:
        result = subprocess.run(
            ["op", "read", OP_REFERENCE],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    print("ERROR: No WARP_API_KEY and 1Password read failed", file=sys.stderr)
    sys.exit(1)


API_KEY: Optional[str] = None


def headers():
    global API_KEY
    if not API_KEY:
        API_KEY = get_api_key()
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }


async def api_call(method: str, endpoint: str, body: dict = None) -> dict:
    """Make an API call using asyncio subprocess (no httpx dependency).
    
    Auth header is passed via stdin using curl --config to avoid
    exposing the Bearer token in the process list.
    """
    url = f"{API_BASE}{endpoint}"
    cmd = ["curl", "-sf", "--max-time", "30", "-X", method, url,
           "-H", "Content-Type: application/json",
           "--config", "-"]
    if body:
        cmd.extend(["-d", json.dumps(body)])

    # Pass auth header via stdin to keep it out of ps/proc
    hdrs = headers()
    config_data = f'-H "Authorization: {hdrs["Authorization"]}"\n'

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate(input=config_data.encode())
    if proc.returncode != 0:
        # Retry without -f for error body
        cmd_verbose = [c.replace("-sf", "-s") if c == "-sf" else c for c in cmd]
        proc2 = await asyncio.create_subprocess_exec(
            *cmd_verbose,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout2, _ = await proc2.communicate(input=config_data.encode())
        raise RuntimeError(f"API call failed: {stderr.decode()} {stdout2.decode()}")

    if not stdout.strip():
        return {}
    try:
        return json.loads(stdout.decode())
    except json.JSONDecodeError:
        raise RuntimeError(f"Non-JSON API response: {stdout.decode()[:200]}")


# --- Core operations ---

async def create_run(
    prompt: str,
    env_id: str,
    skill: str = None,
    name: str = None,
    conversation_id: str = None,
    title: str = None,
) -> dict:
    body = {"prompt": prompt, "team": False}
    if title:
        body["title"] = title
    if skill:
        body["skill"] = skill
    if conversation_id:
        body["conversation_id"] = conversation_id
    config = {}
    if name:
        config["name"] = name
    if env_id:
        config["environment_id"] = env_id
    if config:
        body["config"] = config
    result = await api_call("POST", "/agent/run", body)
    if not result.get("run_id"):
        raise RuntimeError(f"create_run returned no run_id: {json.dumps(result)[:200]}")
    return result


async def get_run(run_id: str) -> dict:
    return await api_call("GET", f"/agent/runs/{run_id}")


async def poll_run(run_id: str, interval: int = POLL_INTERVAL, timeout: int = POLL_TIMEOUT) -> dict:
    elapsed = 0
    while elapsed < timeout:
        result = await get_run(run_id)
        state = result.get("state", "UNKNOWN")
        msg = result.get("status_message", {}).get("message", "no status")
        print(f"  [{state}] {msg} ({elapsed}s)", file=sys.stderr)
        if state in ("SUCCEEDED", "FAILED"):
            return result
        await asyncio.sleep(interval)
        elapsed += interval
    print(f"  TIMEOUT after {timeout}s", file=sys.stderr)
    return await get_run(run_id)


def detect_severity(status_message: str) -> Severity:
    """Simple heuristic to detect finding severity from status message."""
    text = status_message.upper()
    if "CRITICAL" in text:
        return Severity.CRITICAL
    if "HIGH" in text:
        return Severity.HIGH
    if "MEDIUM" in text:
        return Severity.MEDIUM
    if "LOW" in text:
        return Severity.LOW
    return Severity.NONE


async def run_stage(
    stage_name: str,
    prompt: str,
    env_id: str,
    skill: str = None,
    conversation_id: str = None,
) -> StageResult:
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"STAGE: {stage_name}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    result = await create_run(
        prompt=prompt,
        env_id=env_id,
        skill=skill,
        name=stage_name,
        conversation_id=conversation_id,
        title=f"Pipeline: {stage_name}",
    )
    run_id = result.get("run_id", "")
    print(f"  Run ID: {run_id}", file=sys.stderr)

    final = await poll_run(run_id)
    status_msg = final.get("status_message", {}).get("message", "")
    session_link = final.get("session_link", "")
    conv_id = final.get("conversation_id", "")

    sr = StageResult(
        stage=stage_name,
        run_id=run_id,
        state=final.get("state", "UNKNOWN"),
        status_message=status_msg,
        session_link=session_link,
        conversation_id=conv_id,
        severity=detect_severity(status_msg),
        raw=final,
    )

    print(f"  State: {sr.state}", file=sys.stderr)
    print(f"  Session: {sr.session_link}", file=sys.stderr)
    if sr.severity != Severity.NONE:
        print(f"  Severity detected: {sr.severity.name}", file=sys.stderr)

    return sr


# --- Pipeline ---

async def run_pipeline(
    task: str,
    env_id: str,
    stages: list[str],
    skill_prefix: str = "",
    share_conversation: bool = True,
):
    results: list[StageResult] = []
    conversation_id = None
    retry_count = 0

    i = 0
    while i < len(stages):
        stage = stages[i]
        skill = f"{skill_prefix}:{stage}"

        # Build prompt based on stage position
        if i == 0:
            prompt = task
        else:
            prev = results[-1]
            prompt = (
                f"Previous stage ({prev.stage}) completed.\n"
                f"Summary: {prev.status_message}\n"
                f"Session: {prev.session_link}\n\n"
                f"Continue the work. The original task was:\n{task}"
            )

        result = await run_stage(
            stage_name=stage,
            prompt=prompt,
            env_id=env_id,
            skill=skill,
            conversation_id=conversation_id,
        )
        results.append(result)

        # Use conversation_id to continue in same sandbox when appropriate
        if share_conversation and not conversation_id and result.conversation_id:
            conversation_id = result.conversation_id

        if result.state == "FAILED":
            print(f"\n⚠️  Stage {stage} FAILED. Stopping pipeline.", file=sys.stderr)
            break

        # Check if review stages found critical/high issues → loop back
        review_stages = {"security-engineer", "red-teamer", "risk-manager"}
        if stage in review_stages and result.severity.value >= Severity.HIGH.value:
            if retry_count < MAX_RETRIES:
                retry_count += 1
                # Find the last implementation stage to loop back to
                impl_stages = {"trading-engineer", "developer"}
                loop_target = None
                for j in range(len(stages)):
                    if stages[j] in impl_stages:
                        loop_target = j
                if loop_target is not None:
                    print(
                        f"\n🔄 {stage} found {result.severity.name} issues. "
                        f"Looping back to {stages[loop_target]} (retry {retry_count}/{MAX_RETRIES})",
                        file=sys.stderr
                    )
                    i = loop_target
                    continue
            else:
                print(f"\n⚠️  Max retries ({MAX_RETRIES}) reached. Continuing.", file=sys.stderr)

        i += 1

    # --- Summary ---
    print(f"\n{'='*60}", file=sys.stderr)
    print("PIPELINE COMPLETE", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    summary = {
        "task": task,
        "stages": [],
        "total_stages_run": len(results),
    }
    for r in results:
        stage_summary = {
            "stage": r.stage,
            "state": r.state,
            "status_message": r.status_message,
            "session_link": r.session_link,
            "run_id": r.run_id,
        }
        if r.severity != Severity.NONE:
            stage_summary["severity"] = r.severity.name
        summary["stages"].append(stage_summary)
        print(f"  {r.stage}: {r.state} — {r.status_message[:100]}", file=sys.stderr)
        print(f"    Session: {r.session_link}", file=sys.stderr)

    # Output JSON summary to stdout
    print(json.dumps(summary, indent=2))
    return results


# --- CLI ---

def _update_globals(poll_interval, poll_timeout, max_retries):
    global POLL_INTERVAL, POLL_TIMEOUT, MAX_RETRIES
    POLL_INTERVAL = poll_interval
    POLL_TIMEOUT = poll_timeout
    MAX_RETRIES = max_retries


def main():
    parser = argparse.ArgumentParser(description="Oz Agent Pipeline Orchestrator")
    parser.add_argument("--env", required=True, help="Environment ID")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument(
        "--stages", required=True,
        help="Comma-separated stage names (e.g., architect,trading-engineer,security-engineer,red-teamer)"
    )
    parser.add_argument("--skill-prefix", required=True, help="Skill repo prefix (e.g., owner/repo-name)")
    parser.add_argument("--poll-interval", type=int, default=POLL_INTERVAL)
    parser.add_argument("--poll-timeout", type=int, default=POLL_TIMEOUT)
    parser.add_argument("--max-retries", type=int, default=MAX_RETRIES)
    parser.add_argument("--no-conversation", action="store_true", help="Don't share conversation_id between stages")

    args = parser.parse_args()

    # Update module-level defaults
    _update_globals(args.poll_interval, args.poll_timeout, args.max_retries)

    stages = [s.strip() for s in args.stages.split(",")]

    asyncio.run(run_pipeline(
        task=args.task,
        env_id=args.env,
        stages=stages,
        skill_prefix=args.skill_prefix,
        share_conversation=not args.no_conversation,
    ))


if __name__ == "__main__":
    main()
