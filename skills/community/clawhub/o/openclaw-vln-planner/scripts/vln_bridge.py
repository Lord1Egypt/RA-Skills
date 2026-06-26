#!/usr/bin/env python3
"""Example VLN planner bridge.

This script:
1. loads a YAML config file
2. accepts one current image + historical images
3. sends them to an OpenAI-compatible multimodal gateway
4. parses and validates pure JSON output
5. forwards the action to replaceable Python execution functions

The execution functions are placeholders and should be replaced by real OpenClaw integration.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import yaml

ALLOWED_TYPES = {"MOVE_FORWARD", "TURN_LEFT", "TURN_RIGHT", "STOP"}
FALLBACK_STOP = {
    "next_action": {"type": "STOP"},
    "task_status": "failed",
    "confidence": 0.0,
    "notes": "fallback_stop",
}

PROMPT_TEMPLATE = """You are a robot navigation planner.
You will receive:
1. historical observations
2. current observation
3. a user instruction
4. optional robot state and safety flags

Your job is to decide the robot's next single mid-level navigation action.
You may output only one of these actions:
- MOVE_FORWARD with distance in cm
- TURN_LEFT with angle in deg
- TURN_RIGHT with angle in deg
- STOP

Rules:
- Plan only the next step, not the whole route.
- If the goal has been reached, output STOP.
- If you are uncertain, the scene is unclear, or there is any safety risk, output STOP.
- MOVE_FORWARD must be 10-150 cm.
- TURN_LEFT and TURN_RIGHT must be 5-90 deg.
- Output pure JSON only, with no extra explanation.

Historical observations:
{history_desc}

Current observation:
One image is attached as the current observation.

User instruction:
{user_instruction}

Optional robot state:
{robot_state}

Optional safety flags:
{safety_flags}
"""


@dataclass
class PlannerConfig:
    confidence_threshold: float
    base_url: str
    api_key: str
    model_id: str
    timeout_seconds: int
    max_history_frames: int
    dry_run: bool


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_config(raw: Dict[str, Any]) -> PlannerConfig:
    planner = raw.get("planner", {})
    model = raw.get("model", {})
    executor = raw.get("executor", {})
    return PlannerConfig(
        confidence_threshold=float(planner.get("confidence_threshold", 0.55)),
        base_url=str(model.get("base_url", "")).rstrip("/"),
        api_key=str(model.get("api_key", "")),
        model_id=str(model.get("model_id", "")),
        timeout_seconds=int(model.get("timeout_seconds", 60)),
        max_history_frames=int(planner.get("max_history_frames", 5)),
        dry_run=bool(executor.get("dry_run", True)),
    )


def image_to_data_url(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    mime = mime or "image/jpeg"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_messages(user_instruction: str, current_frame: str, history_frames: List[str], robot_state: Any, safety_flags: Any) -> List[Dict[str, Any]]:
    history_desc = json.dumps(
        [{"index": i, "image": os.path.basename(p)} for i, p in enumerate(history_frames, start=1)],
        ensure_ascii=False,
    )
    text = PROMPT_TEMPLATE.format(
        history_desc=history_desc,
        user_instruction=user_instruction,
        robot_state=json.dumps(robot_state or {}, ensure_ascii=False),
        safety_flags=json.dumps(safety_flags or {}, ensure_ascii=False),
    )

    content: List[Dict[str, Any]] = [{"type": "text", "text": text}]
    for hf in history_frames:
        content.append({"type": "image_url", "image_url": {"url": image_to_data_url(hf)}})
    content.append({"type": "image_url", "image_url": {"url": image_to_data_url(current_frame)}})
    return [{"role": "user", "content": content}]


def extract_text_from_response(data: Dict[str, Any]) -> str:
    if isinstance(data.get("output_text"), str) and data["output_text"].strip():
        return data["output_text"].strip()

    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        msg = choices[0].get("message", {})
        content = msg.get("content")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict):
                    t = item.get("text") or item.get("content")
                    if isinstance(t, str):
                        texts.append(t)
            if texts:
                return "\n".join(texts).strip()

    output = data.get("output")
    if isinstance(output, list):
        texts = []
        for block in output:
            content = block.get("content", []) if isinstance(block, dict) else []
            for item in content:
                if isinstance(item, dict) and item.get("type") in {"output_text", "text"}:
                    text = item.get("text")
                    if isinstance(text, str):
                        texts.append(text)
        if texts:
            return "\n".join(texts).strip()

    raise ValueError("Could not extract text from model response")


def safe_parse_json(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
        raise


def validate_action(data: Dict[str, Any], confidence_threshold: float) -> Dict[str, Any]:
    action = data.get("next_action")
    if not isinstance(action, dict):
        raise ValueError("next_action missing")

    action_type = action.get("type")
    if action_type not in ALLOWED_TYPES:
        raise ValueError("invalid action type")

    task_status = data.get("task_status", "in_progress")
    if task_status not in {"in_progress", "completed", "failed"}:
        raise ValueError("invalid task_status")

    confidence = data.get("confidence", 0.0)
    if not isinstance(confidence, (int, float)):
        raise ValueError("invalid confidence")

    if confidence < confidence_threshold:
        raise ValueError("confidence below threshold")

    if action_type == "MOVE_FORWARD":
        value = action.get("value")
        unit = action.get("unit")
        if unit != "cm" or not isinstance(value, (int, float)) or not (10 <= value <= 150):
            raise ValueError("invalid MOVE_FORWARD bounds")
    elif action_type in {"TURN_LEFT", "TURN_RIGHT"}:
        value = action.get("value")
        unit = action.get("unit")
        if unit != "deg" or not isinstance(value, (int, float)) or not (5 <= value <= 90):
            raise ValueError("invalid TURN bounds")
    elif action_type == "STOP":
        pass

    return data


def execute_move_forward(distance_cm: float) -> None:
    print(f"EXECUTE MOVE_FORWARD {distance_cm} cm", file=sys.stderr)


def execute_turn_left(angle_deg: float) -> None:
    print(f"EXECUTE TURN_LEFT {angle_deg} deg", file=sys.stderr)


def execute_turn_right(angle_deg: float) -> None:
    print(f"EXECUTE TURN_RIGHT {angle_deg} deg", file=sys.stderr)


def execute_stop() -> None:
    print("EXECUTE STOP", file=sys.stderr)


def get_robot_state() -> Dict[str, Any]:
    return {}


def get_safety_flags() -> Dict[str, Any]:
    return {}


def bridge_execute(action_json: Dict[str, Any], dry_run: bool = True) -> None:
    action = action_json["next_action"]
    action_type = action["type"]
    if dry_run:
        print(f"DRY_RUN {json.dumps(action_json, ensure_ascii=False)}", file=sys.stderr)
        return
    if action_type == "MOVE_FORWARD":
        execute_move_forward(float(action["value"]))
    elif action_type == "TURN_LEFT":
        execute_turn_left(float(action["value"]))
    elif action_type == "TURN_RIGHT":
        execute_turn_right(float(action["value"]))
    else:
        execute_stop()


def call_openai_compatible(cfg: PlannerConfig, messages: List[Dict[str, Any]]) -> str:
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": cfg.model_id,
        "messages": messages,
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    chat_url = f"{cfg.base_url}/chat/completions"
    resp = requests.post(chat_url, headers=headers, json=payload, timeout=cfg.timeout_seconds)
    resp.raise_for_status()
    return extract_text_from_response(resp.json())


def should_force_stop(safety_flags: Dict[str, Any]) -> bool:
    return any(bool(safety_flags.get(k, False)) for k in ["blocked", "collision_risk", "lost"])


def goal_reached(safety_flags: Dict[str, Any]) -> bool:
    return bool(safety_flags.get("target_reached", False))


def plan_once(config_path: str, user_instruction: str, current_frame: str, history_frames: List[str], robot_state: Optional[Dict[str, Any]] = None, safety_flags: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    raw_cfg = load_config(config_path)
    cfg = build_config(raw_cfg)

    if not cfg.base_url or not cfg.api_key or not cfg.model_id:
        return FALLBACK_STOP

    robot_state = robot_state if robot_state is not None else get_robot_state()
    safety_flags = safety_flags if safety_flags is not None else get_safety_flags()

    if goal_reached(safety_flags):
        return {
            "next_action": {"type": "STOP"},
            "task_status": "completed",
            "confidence": 1.0,
            "notes": "goal reached",
        }

    if should_force_stop(safety_flags):
        return {
            "next_action": {"type": "STOP"},
            "task_status": "failed",
            "confidence": 1.0,
            "notes": "safety_stop",
        }

    history_frames = history_frames[: cfg.max_history_frames]
    messages = build_messages(user_instruction, current_frame, history_frames, robot_state, safety_flags)

    try:
        raw_text = call_openai_compatible(cfg, messages)
        parsed = safe_parse_json(raw_text)
        validated = validate_action(parsed, cfg.confidence_threshold)
    except Exception:
        validated = FALLBACK_STOP

    bridge_execute(validated, dry_run=cfg.dry_run)
    return validated


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="Path to YAML config")
    p.add_argument("--instruction", required=True, help="Navigation instruction")
    p.add_argument("--current-frame", required=True, help="Current frame image path")
    p.add_argument("--history-frame", action="append", default=[], help="Historical frame image path; repeat as needed")
    p.add_argument("--robot-state-json", default="{}", help="Robot state JSON string")
    p.add_argument("--safety-flags-json", default="{}", help="Safety flags JSON string")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = plan_once(
        config_path=args.config,
        user_instruction=args.instruction,
        current_frame=args.current_frame,
        history_frames=args.history_frame,
        robot_state=json.loads(args.robot_state_json),
        safety_flags=json.loads(args.safety_flags_json),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
