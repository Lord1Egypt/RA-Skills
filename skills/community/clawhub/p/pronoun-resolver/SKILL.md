---
name: pronoun-resolver
version: 0.11.0
description: |
  Detects ambiguous pronouns, vague referents, and bare imperatives in user messages
  and flags them for resolution using conversation context. Zero-latency detection via
  hook; resolution happens inside the conversation where context lives. Self-learning
  via correction ledger with adaptive confidence tiering.
capabilities:
  - user-prompt-submit hook (fires on every message, regex-only, no LLM calls)
  - file-write: ~/.claude/skills/pronoun-resolver/.claude/pronoun-ledger.json (resolution metadata, no raw prompts)
  - file-write: ~/.claude/skills/pronoun-resolver/.claude/pronoun-resolver-analytics.jsonl (per-message stats)
data_retention: |
  All data is local-only, never transmitted externally. Prompts are hashed (SHA-256),
  never stored as text. Both data files can be deleted without affecting functionality.
hooks:
  user-prompt-submit:
    - type: command
      command: "bash ${CLAUDE_SKILL_DIR}/bin/detect-pronouns.sh"
      statusMessage: "Scanning for ambiguous references..."
---

# Pronoun Resolver

## Arguments

If invoked with `--stats`: run `python3 ~/.claude/skills/pronoun-resolver/bin/stats.py` and display the output. Do not proceed with the rest of this skill.

---

You are operating with the pronoun resolver active. When the hook detects ambiguous
references in a user message, you will see flags injected before the message.

## Your Role

YOU are the resolver. You have the conversation context. The hook just detects — you decide.

## Resolution Tiering

When you see `[AMBIGUOUS:]` flags, apply this framework:

### GREEN — Resolve silently (90%+ confidence)
The referent is obvious from the last 1-3 messages. Just act. Don't mention the resolution.
- "Fix it" when you just showed them a bug → fix the bug
- "Make that work" after discussing a failing test → fix the test

### YELLOW — State assumption, proceed (70-90% confidence)
You're fairly sure but there's ambiguity. State what you're assuming in one line, then act.
- "I'm taking 'the other one' to mean `auth.ts` since we discussed two files. Acting on that."

### RED — Ask before acting (<70% confidence)
Multiple plausible referents, or no recent context to resolve against. Ask concisely.
- "What should I make good — the UI layout we discussed or the API response format?"

### BLACK — Bare imperative, no context at all
First message of a conversation with no object. Always ask.
- "Make good" with no prior context → "What would you like me to improve?"

## Flag Format

The hook outputs a preamble followed by flags:
```
[PRONOUN-RESOLVER: Resolve these using conversation context. HIGH confidence=act silently. MEDIUM=state assumption then act. LOW/no context=ask user first.]
[AMBIGUOUS: pronouns="it,that" | type=pronoun]
[AMBIGUOUS: vague="other,something" | type=vague_referent]
[AMBIGUOUS: implicit verb="make" | type=bare_imperative | subtype=verb_adjective]
```

## Ledger

Resolution accuracy is tracked at `~/.claude/skills/pronoun-resolver/.claude/pronoun-ledger.json`.
When you resolve an ambiguous reference, log it. When the user corrects you
("no not that", "I meant X"), mark the previous resolution as corrected.

**The hook injects a `[PRONOUN-RESOLVER-LOG: ...]` directive on every fire** with the exact
`bin/log-resolution.py` command and ledger path, so the logging instruction is present even
when this SKILL.md isn't loaded into context (the hook prints it; you run the command). Use that helper rather than hand-editing the JSON — it
does an atomic read-modify-write and keeps `resolution_count` in sync. Do **not** log when
you couldn't resolve (asked the user, false-positive flag, or no real referent).

The ledger schema:
```json
{
  "resolutions": [...],
  "resolution_count": 0,
  "adaptive_threshold": 0.8,
  "context_reliability": {}
}
```

Each resolution entry:
```json
{
  "timestamp": "ISO8601",
  "pronoun": "it",
  "prompt_hash": "sha256 hex of the full prompt (no raw text stored)",
  "resolved_to": "the auth middleware",
  "tier_used": "green|yellow|red|black",
  "confidence": 0.92,
  "was_corrected": false
}
```

Never store raw prompt text in the ledger. Use `prompt_hash` for deduplication only.

## Correction Detection

If the user's next message corrects your resolution:
1. Mark the previous ledger entry as `was_corrected: true`
2. Adjust your confidence calibration — if you're frequently wrong at a given tier, escalate more

## Adaptation

Every 10 resolutions, check your accuracy:
- If >90% correct at green tier → you're well calibrated
- If <75% correct → shift toward yellow/red (ask more often)
- Track which context signals (last edited file, recent discussion topic, etc.) are most reliable

## Disable

If the user creates `.claude/pronoun-resolver-disabled` in the project root, stop resolving.

## What Gets Detected

1. **Personal pronouns** (always flagged): it, them, they, its
2. **Demonstratives** (flagged only when standalone, not as determiners): this, that, these, those
   - "fix this" → flagged ("this" is standalone pronoun)
   - "fix this bug" → NOT flagged ("this" is a determiner for "bug")
3. **Vague referents:** other, something, someone, somewhere, anything, everything, stuff
4. **Bare imperatives:** verb alone ("Fix") or verb + adjective with no object ("Make good", "Clean up", "Make better/faster")

## Install

1. Symlink or copy this directory to `~/.claude/skills/pronoun-resolver`
2. Add the hook to `~/.claude/settings.json`:
```json
"UserPromptSubmit": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "bash /ABSOLUTE/PATH/TO/.claude/skills/pronoun-resolver/bin/detect-pronouns.sh"
      }
    ]
  }
]
```
Note: The path must be absolute. Update it if the skill is moved.
