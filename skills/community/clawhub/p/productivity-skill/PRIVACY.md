# Privacy Policy — Productivity Skill v2.9

## Overview

This skill is a **local-only, instruction-based** AI productivity coach. It does **not** contain any executable code, install scripts, or network communication logic. All data is stored through the system's native memory mechanism and is never uploaded, transmitted, or shared with any external service.

## System-Native Memory

Every OpenClaw environment is different — different operating systems, different workspace paths, different configurations. This skill does **not** create its own custom file folders or assume any fixed directory structure. Instead, it uses the **system's built-in memory function** that every OpenClaw environment provides:

*   **MEMORY.md** — long-term memory, loaded automatically at the start of every session
*   **Daily notes** (memory/YYYY-MM-DD.md) — short-term context for today and yesterday

This approach ensures compatibility across all environments without hardcoded paths.

## Consent Model

Before writing anything to memory, the skill's `FIRST_TIME_SETUP` protocol will:

1.  Explain clearly **what data** needs to be saved and **why** (goals drive 40% of task prioritization)
2.  Request **explicit write permission** to the system's long-term memory (MEMORY.md)
3.  Honestly explain the **consequences of each choice**:
    *   **Agree**: Goals and preferences persist across sessions; task sorting is always personalized
    *   **Decline**: Session-only mode; the task prioritization mechanism loses effectiveness over time because goals, preferences, and learned rules cannot be retained across sessions
4.  If you decline, the skill operates in **session-only mode** with no memory writes

You can grant or revoke write permission at any time during any session.

## Data Storage

All data is stored through the system's native memory. Here is a complete breakdown:

| Data | Stored In | Purpose | Created When | Deletion |
| :--- | :--- | :--- | :--- | :--- |
| 5 core annual goals and 8 life areas | MEMORY.md | Task prioritization reference variable | After Waterdrop 520 goal-setting | Edit MEMORY.md to remove |
| Preferences (list mode, review times) | MEMORY.md | Personalize skill behavior | After consent | Edit MEMORY.md to remove |
| Custom evolution rules | MEMORY.md | Adapt task scoring to your patterns | After your explicit approval | Edit MEMORY.md to remove |
| Inbox captures, task logs, daily events | Daily notes | Running context for today | During daily use | Edit or delete daily note file |

## What This Skill Does NOT Do

*   **No ambient monitoring**: Energy sensing is based only on your explicit text (word choices, emotional vocabulary) and file content (item counts in inbox/lists). It does **not** monitor typing speed, typing rhythm, response timing, mouse movements, keystroke patterns, or any other behavioral signals.
*   **No external data transmission**: All data is stored locally. No data is ever sent to any external server, API, or third party.
*   **No silent rule creation**: Custom rules are always shown to you and require your explicit approval before being saved.
*   **No credential storage**: This skill does not store any passwords, API keys, or authentication tokens.
*   **No code execution**: This skill is instruction-only. It contains no scripts, binaries, or executable payloads.
*   **No custom folders or hardcoded paths**: The skill uses only the system's native memory mechanism and never assumes a fixed directory structure.

## Tool Usage

This skill declares the following tool permissions:

| Tool | Purpose | Consent |
| :--- | :--- | :--- |
| `schedule` | Set reminders for calendar events and reviews | Asked before each use |
| System memory (read) | Read MEMORY.md and daily notes for context | Covered by initial consent |
| System memory (write) | Write goals, preferences, and approved rules to MEMORY.md | Covered by initial consent; custom rules require additional approval |

## How to Delete Your Data

You can edit `MEMORY.md` at any time to remove any data this skill has written. You can also delete specific daily note files. The skill will then trigger the first-time setup protocol (with consent request) if you use it again.

## Contact

For questions about this privacy policy, please open an issue on the [GitHub repository](https://github.com/yewubin-jpg/productivity-skill).
