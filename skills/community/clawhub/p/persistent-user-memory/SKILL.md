# Skill: Persistent User Memory

**Version:** 1.0.0  
**Author:** community  
**Tags:** `memory`, `personalization`, `context`, `learning`, `stateful`  
**Requires:** file system access, optional: vector store or SQLite

---

## Overview

This skill gives OpenClaw a long-term, structured memory of the user it works with. Unlike session-scoped context, this memory persists across restarts, learns from patterns over time, and is actively consulted before every significant action.

The goal: make OpenClaw behave less like a capable stranger and more like a trusted assistant who actually knows you.

---

## Memory Store Location

All memory is stored in a local file:

```
~/.openclaw/memory/user_profile.json
```

Never store memory in a temp directory. Never delete this file unless the user explicitly says `"reset my memory"` or `"forget everything"`.

---

## Memory Schema

```json
{
  "identity": {
    "name": "",
    "timezone": "",
    "language": "en",
    "preferred_name": ""
  },
  "preferences": {
    "communication": {
      "email_tone": "formal | casual | neutral",
      "response_length": "concise | detailed",
      "sign_off": ""
    },
    "scheduling": {
      "protected_hours": [],
      "preferred_meeting_times": [],
      "buffer_between_meetings_minutes": 15
    },
    "work": {
      "tools": [],
      "stacks": [],
      "working_hours": { "start": "", "end": "" }
    }
  },
  "relationships": {
    "contacts": [
      {
        "name": "",
        "alias": [],
        "relationship": "boss | colleague | client | friend | family",
        "communication_notes": "",
        "last_interaction": ""
      }
    ]
  },
  "patterns": {
    "recurring_tasks": [],
    "common_mistakes": [],
    "frequent_requests": []
  },
  "episodic": [
    {
      "date": "",
      "summary": "",
      "outcome": "",
      "tags": []
    }
  ],
  "meta": {
    "created_at": "",
    "last_updated": "",
    "version": "1.0.0"
  }
}
```

---

## Core Behaviors

### 1. Read Before Acting
Before any significant action (sending email, scheduling, running a script, making a purchase), silently load and consult `user_profile.json`. Apply relevant preferences without asking the user to repeat themselves.

**Example:**
> User asks to draft an email to "Sarah"  
> → Look up Sarah in `relationships.contacts`  
> → Find she's a client, communication_notes says "very formal, always address as Ms. Chen"  
> → Draft accordingly, without prompting the user for tone

---

### 2. Write After Learning
After completing any task where a new preference, pattern, or fact was revealed, update memory silently. Do not announce every write. Do announce if a conflict is detected (see edge cases).

**Trigger conditions for a memory write:**
- User corrects you → update the relevant field
- User states a preference explicitly ("I always want...", "never do X")
- A contact is mentioned with context for the first time
- A recurring task is completed for the 3rd+ time
- An error occurred and the user explained why it was wrong

---

### 3. Surface Memory Proactively
Occasionally surface relevant memory when it adds value. Do not do this constantly — only when it meaningfully changes what action should be taken.

**Good:**
> "You mentioned last week the deploy failed because of a missing env var — want me to check for that before running?"

**Bad (annoying):**
> "I remember you like concise emails! Here is a concise email."

---

### 4. Episodic Log
After any multi-step task or significant interaction, append a brief episode to `episodic[]`:

```json
{
  "date": "2026-03-02",
  "summary": "Drafted contract email to Ms. Chen re: Q2 renewal",
  "outcome": "sent",
  "tags": ["email", "contract", "sarah-chen"]
}
```

Keep episodes short (1–2 sentences). Do not log trivial or one-line tasks. Trim episodes older than 180 days unless tagged `important`.

---

## Edge Cases

### ❗ Conflicting Preferences
If a new instruction contradicts stored memory:

1. Do NOT silently overwrite.
2. Surface the conflict:
   > "You previously told me to always CC your manager on client emails, but this time you haven't mentioned it — should I still CC them, or update that preference?"
3. Wait for explicit resolution before writing.

---

### ❗ Ambiguous Contacts
If a name matches multiple contacts (e.g., two "Davids"):

1. Do NOT guess.
2. Ask: "Which David — David Kim (colleague) or David Okafor (client)?"
3. After resolution, update the episodic log and consider adding an alias.

---

### ❗ Sensitive or Private Data
Never store:
- Passwords or API keys
- Banking or payment details
- Medical information unless user explicitly requests it
- Verbatim message contents (summarize instead)

If the user tries to ask you to remember sensitive data, respond:
> "I don't store that kind of information for your safety. You can use a password manager or secure vault instead."

---

### ❗ Memory Corruption / Parse Failure
If `user_profile.json` fails to parse:

1. Do NOT overwrite or delete it.
2. Back it up to `user_profile.backup.json`.
3. Notify the user: "Your memory file appears corrupted. I've backed it up and started fresh. Want me to try to recover it?"
4. Start with an empty profile.

---

### ❗ First Run (No Memory File)
If no memory file exists:

1. Create the file with empty defaults.
2. Do NOT ask the user a long onboarding questionnaire.
3. Learn passively through normal interaction — fill in fields as they naturally emerge.
4. After the 5th session, you may ask 1–2 targeted questions to fill obvious gaps (e.g., timezone, preferred name).

---

### ❗ User Asks "What Do You Know About Me?"
Respond with a human-readable summary, not raw JSON:

> "Here's what I know about you so far:
> - You prefer concise, casual communication except with clients
> - Your protected hours are 9–10am and noon–1pm
> - You work primarily in Python and use VS Code
> - I have notes on 4 contacts including your manager (Alex) and a client (Ms. Chen)
> - I've logged 12 recent tasks"

Then offer: "Want to correct or add anything?"

---

### ❗ User Says "Forget [X]"
Surgically remove only the referenced data. Confirm before deleting:
> "Just to confirm — you want me to forget everything about Ms. Chen, or just the communication notes?"

Never bulk-delete unless user says "forget everything" or "reset my memory."

---

## Memory Hygiene (Automated)

Run silently on each startup:
- Remove episodic entries older than 180 days (unless tagged `important`)
- Deduplicate contacts with identical names
- Flag fields that haven't been updated in 90+ days as `stale` (do not delete, just mark)
- Rewrite `meta.last_updated` timestamp

---

## Privacy Notes

- All memory is stored **locally only**. Never send `user_profile.json` to any remote server or include it in API calls as raw context.
- When passing memory to an LLM, extract only the **relevant subset** for the task at hand.
- Memory is the user's property. Always honor deletion requests immediately.

---

## Example Interactions

**Learning a preference:**
> User: "Don't schedule anything before 9:30am."  
> Agent writes: `preferences.scheduling.protected_hours: ["00:00–09:30"]`  
> Agent: "Got it, I'll keep your mornings free."

**Applying memory:**
> User: "Send the weekly report to the team."  
> Agent: checks `patterns.recurring_tasks`, finds this has been done before on Fridays at 4pm to a specific list → pre-fills recipients and subject line automatically.

**Conflict resolution:**
> Stored: email tone for Alex = formal  
> User: "Send Alex a quick casual message about lunch"  
> Agent: Sends casual (user's explicit in-context instruction overrides stored default), then asks: "Should I update your default tone for Alex to casual?"

---

## Installation

```bash
claw skill install persistent-user-memory
```

Or manually place this file at:
```
~/.openclaw/skills/persistent-user-memory/SKILL.md
```

---

## Changelog

| Version | Notes |
|---------|-------|
| 1.0.0 | Initial release — full schema, edge cases, episodic log |
