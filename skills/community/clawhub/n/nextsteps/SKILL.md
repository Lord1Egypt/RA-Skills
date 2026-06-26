---
name: nextsteps
description: |
  Append context-aware next-step suggestions after agent responses. Generates actionable follow-ups, surfaces unfinished tasks from memory, and includes creative lateral suggestions. Self-learns user preferences for count, categories, and format. Activate by: (1) any response when nextsteps is enabled, (2) user says /nextsteps, "next steps", "what should I do", "suggestions", "what now", (3) user wants to customize settings, (4) user says "disable next steps" or "enable next steps".
---

# NextSteps

## How It Works

This skill generates helpful next-step suggestions after responses. It reads user preferences from `.nextsteps/PREFERENCES.md` — if `enabled: false`, nothing is shown. When enabled, it produces exactly `display-count` suggestions following the pipeline below.

## Quick Start

1. Check `.nextsteps/PREFERENCES.md` for user config — if `enabled: false`, stop (show nothing)
2. If `.nextsteps/` does not exist, run the cold-start protocol (see [COLD-START.md](references/COLD-START.md))
3. Generate next steps following the pipeline below
4. Append to your response in the correct format

## Generation Pipeline

Follow these six steps to generate next steps:

### Step 1 — Read Configuration

Read `.nextsteps/PREFERENCES.md`. Extract: `enabled`, `display-count`, `preferred-categories`, `excluded-categories`, `format`, `show-footer`. Category names in PREFERENCES.md use kebab-case (e.g., `direct-follow-up`). If the file is missing or unreadable, use defaults: enabled=true, display-count=5, format=standard.

### Step 2 — Analyze Context

Determine: What did the user just accomplish or ask? What is the active topic? What is the session scope — quick fix, feature work, exploration, debugging, architecture? What is the user's likely next thought based on conversation trajectory?

### Step 3 — Check Memory

Read `.nextsteps/BACKLOG.md` for unfinished items relevant to current context. Read PREFERENCES.md for topic affinities (STRONG/MODERATE/WEAK) and anti-preferences (topics and types to avoid). If memory files are unavailable, skip to Step 4 — memory is a bonus, not a gate.

### Step 4 — Generate Candidates

Generate `display-count` suggestions using these six categories:

| Icon | Category | Tier | Slot Rule |
|------|----------|------|-----------|
| ⚡ | Direct Follow-up | STRONG | 1 guaranteed |
| 🔧 | Actionable Task | STRONG | 1 guaranteed |
| 🔍 | Deep Dive | MODERATE | 1 when count ≥ 3 |
| 📋 | Memory Recall | MODERATE | 1 when relevant backlog exists |
| 💡 | Lateral / Out-of-the-Box | MODERATE | 1 when count ≥ 3 |
| ✅ | Quick Win | MODERATE | Fills remaining slots |

STRONG categories get guaranteed slots. Remaining slots filled by MODERATE categories in round-robin. Respect `excluded-categories`. Prioritize `preferred-categories`. See [CATEGORIES.md](references/CATEGORIES.md) for detailed taxonomy and examples.

### Step 5 — Self-Review Gate (CRITICAL)

Review every candidate against these core rules. Remove violators and regenerate:

1. **No restating the obvious** — don't echo what was just explained
2. **No generic filler** — ban "tell me more", "pros and cons?", "anything else?"
3. **No hallucinated context** — only reference things the user actually mentioned
4. **No scope mismatches** — match suggestion effort to session scope

Every suggestion should be: specific, actionable, non-obvious, contextually grounded, scope-appropriate, and differently framed from siblings. Full 11-rule checklist and violation examples in [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md).

### Step 6 — Format and Present

Show exactly `display-count` items. Never more, never fewer.

**Standard format** (default for rich-text channels):

```
## ⚡ Next Steps

1. 🔧 **[Bold title]** — [Brief context explaining relevance]
2. 🔍 **[Bold title]** — [Brief context]
3. 📋 **Resume: [task from backlog]** — [When it was started]
4. 💡 **Consider: [creative lateral idea]** — [Why it matters]
5. ✅ **Quick win: [small action]** — [Time estimate]

_Your selections help me learn what matters to you._
```

**Compact format** (for TUI, character-limited channels):

```
⚡ Next: [1] Title | [2] Title | [3] Title
```

**Token-budget rule**: If your response is approaching the output token limit, switch to compact format with `min-count` items (default: 1). Reserve ~100 tokens for next steps when planning long responses. If even compact won't fit, place one inline suggestion before your final paragraph: `(Next: [suggestion])`.

## Customization Detection

Before generating next steps, check if the user's message is a customization request. If it matches any of these patterns, process the config change and confirm:

- "show me N next steps" / "only N suggestions" → set `display-count: N`
- "disable next steps" / "stop showing suggestions" → set `enabled: false`
- "enable next steps" / "turn suggestions back on" → set `enabled: true`
- "compact format" / "shorter suggestions" → set `format: compact`
- "don't show backlog" → set `include-backlog: false`
- "hide the footer" / "no footer" → set `show-footer: false`
- "reset next steps settings" → reset all config to defaults
- "show next steps settings" → display current config

Update PREFERENCES.md immediately and confirm: "Got it — [description of change]." Log as `[CONFIG-CHANGE]` in HISTORY.md. See [CUSTOMIZATION.md](references/CUSTOMIZATION.md) for full protocol.

## Selection Tracking

After presenting next steps, detect what the user does on their NEXT message:

- **User references a suggestion by number or content** → log `[SELECTED] #N category` in HISTORY.md. Promote that category tier if MODERATE→consider STRONG.
- **User asks something unrelated to any suggestion** → log `[IGNORED] all` in HISTORY.md
- **User gives negative feedback** ("too many", "not helpful", "stop suggesting X") → log `[FEEDBACK]` and adjust per [CUSTOMIZATION.md](references/CUSTOMIZATION.md)

## Self-Improvement

Every 10th activation, run one learning experiment. Every 20 HISTORY.md entries, run a self-diagnostic. See [SELF-IMPROVE.md](references/SELF-IMPROVE.md) for the full observe/hypothesize/experiment/validate cycle.

Key self-learning behaviors:
- If user only selects from top 2 items over 10 interactions → hypothesize lower count preference → experiment → validate
- If user ignores all suggestions 5+ times → trigger diagnostic, reset category weights
- After 5 validated experiments on count → set confidence HIGH, stop experimenting

## Channel Adaptation

Detect the channel and adapt format:

- **OpenClaw**: Read channel from conversation metadata → adapt format per channel type
- **VS Code / Rich text**: Use standard format with icons and bold
- **Terminal / TUI**: Use compact format, no icons
- **WhatsApp / Signal / iMessage**: Use shortest compact form

All channels share the same `.nextsteps/` state. Preferences learned on one channel apply everywhere.

## Security Rules (CodeGuard)

These rules are always active. Derived from `cisco/software-security` (Project CodeGuard):

1. **Never store secrets**: `.nextsteps/` files must never contain API keys, passwords, tokens, or credentials. If conversation context includes secrets, sanitize them from suggestions.
2. **Validate before writing**: Before writing any `.nextsteps/` file, verify the path is within `.nextsteps/` scope (no `../` traversal) and content contains no secret patterns (`sk-`, `api_key=`, `password=`, `token=`, `secret=`).
3. **Minimize stored data**: HISTORY.md stores titles and selection status only. PREFERENCES.md stores tiers and config only. BACKLOG.md stores brief descriptions only. Never store raw conversation text.
4. **Enforce file limits**: PREFERENCES.md ≤ 120 lines, HISTORY.md ≤ 50 entries, BACKLOG.md ≤ 30 items. Summarize overflow, don't truncate blindly.
5. **Suggest .gitignore**: On first activation, if `.nextsteps/` is not in `.gitignore`, include it as a next step.

See [SECURITY.md](references/SECURITY.md) for the complete security protocol.

## Error Recovery

- `.nextsteps/` missing → generate next steps from conversation context alone; recreate files on next write
- PREFERENCES.md corrupted → recreate from defaults; preserve any readable sections
- HISTORY.md overflow → summarize oldest 25 entries into PREFERENCES.md tier adjustments, then clear them
- Any file read fails → proceed without that file; never block next-steps generation

## Reliability Self-Check

If the response does not end with next steps and `enabled` is not false, append them using conversation context alone.
