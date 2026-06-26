---
name: logic-bridge-protocol
description: >-
  Validates vague product requirements and user stories against five closure rules (actor, scenario, goal, actionable path). Returns structured follow-up questions when incomplete, or FileEditor-ready JSON tasks when the story is ready. Use when refining PRDs, user stories, feature specs, or before delegating implementation to an agent.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    emoji: "\U0001f9e0"
---

# Logic Bridge Protocol

## Purpose

Turn fuzzy natural-language requests into **reviewable, structured output**. The companion script `protocol.py` performs a **lightweight closure check** inspired by first-principles and pyramid-style thinking: if the text is too thin, the skill returns **specific follow-up questions**; if it passes, it returns **JSON tasks** suitable for a file editor or coding agent.

## When to use

- The user pastes a one-line idea, half-baked user story, or “make a button” request.
- You need a **gate** before writing code or large docs.
- You want a **repeatable JSON contract** for downstream tools (e.g. FileEditor, task runners).

## Dependencies

- Python **3.10+**
- **Pydantic v2** (`pip install pydantic` or `uv pip install pydantic`)

## How to run

From the skill folder:

```bash
python3 protocol.py
```

To call the API in code or from a REPL:

```python
from protocol import logic_bridge_protocol

result = logic_bridge_protocol({
    "raw_text": "As a store manager, on the inventory page I need to export CSV when stock is low so I can reorder."
})
print(result)
```

## Input

| Field       | Type   | Required | Description                          |
| ----------- | ------ | -------- | ------------------------------------ |
| `raw_text`  | string | yes      | Raw requirement or user story text   |

## Output (JSON)

### Failure — `status: "error"`

- `message`: short summary for the agent.
- `follow_up_questions`: list of concrete gaps (actor, scenario, goal, path, or length).

### Success — `status: "ok"`

- `message`: confirmation string.
- `file_editor_tasks`: list of tasks with:
  - `intent`: `write` | `patch` | `review`
  - `target_path`: suggested file path (default brief: `docs/logic_bridge_task.md`)
  - `instructions`: what to write in natural language, including a **sha256** digest of the normalized input for traceability.

## Rules the checker enforces

1. **Minimum substance** — not just a couple of words.
2. **Actor** — who benefits or performs the action (supports EN/ZH cues).
3. **Scenario** — where/when in the product this applies.
4. **Problem / goal** — pain or intended outcome.
5. **Actionable path** — steps or navigation, not only intent.

## Limitations

- Heuristic only; it can **false-negative** on poetic or highly implicit writing.
- Tune regexes in `protocol.py` for your domain (e.g. B2B, internal tools).

## Examples

**Too vague**

Input: `{"raw_text": "add a feature"}`  
→ Error with follow-ups asking for actor, scenario, goal, and steps.

**Stronger story**

Input: `{"raw_text": "As a support agent, when I open a ticket I want to paste logs and save them so the engineer sees them. I click Attach, choose file, then Save."}`  
→ Success with a `docs/logic_bridge_task.md` write task and sha256 note.

## Testing

A self-contained test suite ships with the skill:

```bash
python3 test_protocol.py
# 12/12 tests passed
```

Coverage: empty input, missing keys, wrong types, vague one-liners, partially-complete stories (EN + ZH), fully-closed stories, hash determinism.

## Publishing to ClawHub

Zip the **folder** that contains `SKILL.md`, `protocol.py`, `requirements.txt`, and `test_protocol.py` (same directory level), or use the ClawHub CLI per current docs. Ensure only **text-based** files are included; total bundle must respect registry limits.
