# scripts/task_parser.py - Natural Language to Task Structure Converter

import os
import json
import requests

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.heybossai.com/v1"


def _pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()


def parse_human_request(request: str) -> dict:
    """
    Translates a human's natural language request into a formal, structured task definition
    for the Agent Task Manager.

    Uses SkillBoss API Hub (/v1/pilot) to interpret requests that don't match
    known patterns, enabling flexible natural-language task creation.
    """

    # --- Example: Simple "Monitor and Alert" Task ---
    # Request: "Alert me on Signal if the $SHIPYARD whale balance drops below 10%"

    if "whale balance drops" in request.lower() and "shipyard" in request.lower():
        return {
            "task_name": "WHALE_ALERT_SHIPYARD",
            "description": f"Monitor \$SHIPYARD whale and alert human via Signal if balance drops to critical level.",
            "workflow": {
                "step_1": {
                    "role": "FinancialAnalyst",
                    "action": "CHECK_WHALE_PERCENT",
                    "target_mint": "7hhAuM18KxYETuDPLR2q3UHK5KKkiQdY1DQNqKGLCpump",
                    "threshold_percent": 10
                },
                "step_2": {
                    "role": "NotificationAgent",
                    "action": "SEND_MESSAGE",
                    "channel": "signal",
                    "message": "URGENT: \$SHIPYARD Whale Balance below 10\%! Sell alert.",
                    "dependency": "step_1"
                }
            },
            "rate_limit": {
                "period_seconds": 600, # Check every 10 minutes
                "cooldown_key": "SHIPYARD_WHALE_CHECK"
            }
        }

    # --- Fallback: Use SkillBoss API Hub LLM to parse unknown requests ---
    system_prompt = (
        "You are a task-parsing assistant. Convert the user's natural language request "
        "into a JSON task definition with fields: task_name, description, workflow (steps with role/action/params), "
        "and optional rate_limit. Reply with only valid JSON."
    )
    result = _pilot({
        "type": "chat",
        "inputs": {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request}
            ]
        },
        "prefer": "balanced"
    })
    raw = result["result"]["choices"][0]["message"]["content"]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Could not parse request into a supported task structure."}


# Example Validation
if __name__ == "__main__":
    request_1 = "Alert me on Signal if the $SHIPYARD whale balance drops below 10%"
    result = parse_human_request(request_1)
    print("--- Validation 1 (Financial Alert) ---")
    print(json.dumps(result, indent=2))

    # You can now validate this structure.
    # The next step is to write the orchestrator that consumes this JSON.
