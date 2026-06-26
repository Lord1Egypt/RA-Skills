# Pronoun Resolver

A Claude Code hook that detects ambiguous references in user prompts and flags them for resolution. Zero-latency detection via regex/heuristics — Claude resolves using its own conversation context.

No LLM calls. No external API keys. Fires on every message, produces output only when ambiguity is detected.

## The Problem

When you type "fix it", Claude has to guess what "it" refers to. Sometimes it guesses right. Sometimes it confidently refactors the wrong file.

When you type "Make good" with no context, Claude may invent an interpretation rather than asking.

This hook makes the ambiguity visible so Claude asks instead of guessing.

## How It Works

```
User types: "fix it"
                |
    +-----------v-----------+
    |  Hook: detect-pronouns |
    |  (regex + heuristic)   |
    |  ~0ms, no LLM calls    |
    +-----------+-----------+
                | ambiguity detected
    +-----------v-----------+
    |  Output: flags +       |
    |  compact preamble      |
    +-----------+-----------+
                |
    +-----------v-----------+
    |  Claude receives:      |
    |  [PRONOUN-RESOLVER: Resolve using context. HIGH=act. LOW=ask.]  |
    |  [AMBIGUOUS: pronouns="it" | type=pronoun]                      |
    |  fix it                |
    +--------------------+---+
                |
    +-----------v-----------+
    |  Claude resolves using |
    |  conversation context  |
    |  (GREEN/YELLOW/RED)    |
    +------------------------+
```

Claude is the resolver. It has the conversation context. The hook just makes ambiguity explicit.

## Detection Categories

### 1. Personal Pronouns (always flagged)

`it`, `them`, `they`, `its`

These are always referential — they can't be determiners.

### 2. Demonstratives (smart filtering)

`this`, `that`, `these`, `those`

Only flagged when used as standalone pronouns, NOT as determiners:

| Prompt | Flagged? | Why |
|--------|----------|-----|
| `fix this` | Yes | "this" is standalone, no object |
| `fix this bug` | No | "this" is a determiner for "bug" |
| `do that and deploy` | Yes | "that" followed by conjunction |
| `update that file` | No | "that" is a determiner for "file" |
| `these tests are failing` | No | "these" is a determiner for "tests" |

### 3. Vague Referents

`other`, `something`, `someone`, `somewhere`, `anything`, `everything`, `stuff`

### 4. Bare Imperatives (implicit subject)

Detected when no pronouns or vague words are found. Catches commands with no explicit object:

| Prompt | Detected | Subtype |
|--------|----------|---------|
| `Fix` | Yes | bare_verb |
| `Make good` | Yes | verb_adjective |
| `Make better/faster` | Yes | verb_adjective |
| `Clean up` | Yes | verb_adjective |
| `Fix the bug` | No | has explicit object |
| `Add tests` | No | has noun object |

## Resolution Tiering

When Claude sees flags, it applies this framework:

| Tier | Confidence | Action |
|------|-----------|--------|
| GREEN | 90%+ | Resolve silently, just act |
| YELLOW | 70-90% | State assumption in one line, then act |
| RED | <70% | Ask the user before acting |
| BLACK | No context | Always ask (first message bare imperative) |

## Self-Learning Ledger

Resolution accuracy is tracked at `~/.claude/skills/pronoun-resolver/.claude/pronoun-ledger.json` (inside the skill directory, never in your project). When Claude resolves a reference, it logs metadata — no raw prompt text is stored. When the user corrects it, the entry is marked and confidence calibration adjusts.

```json
{
  "resolutions": [],
  "resolution_count": 0,
  "adaptive_threshold": 0.8,
  "context_reliability": {}
}
```

### How logging actually fires

The hook injects a `[PRONOUN-RESOLVER-LOG: ...]` directive on **every** flagged
message, carrying the exact `bin/log-resolution.py` command and ledger path. The
hook only *prints* this directive — Claude runs the command to record a
resolution. The point is that the instruction is now present on every fire even
when `SKILL.md` isn't loaded into context; previously the "log it" instruction
lived only in the skill body, so it was almost never in context and the ledger
almost never updated. Claude logs only when it actually resolved a reference (not
when it asked the user, or when a regex flag had no real referent).

`bin/log-resolution.py` owns all writes so logging is safe by construction:

- **Locked, atomic writes.** The whole read-modify-write runs under an exclusive
  `flock`, so concurrent hook fires (e.g. parallel agents) never drop each
  other's entries; the file is replaced atomically and never left half-written.
- **Secret/PII redaction.** Every free-text field (`resolved_to`, the pronoun
  token, context signal) is scanned before it touches disk. Known credential
  shapes (API keys, tokens, JWTs, PEM keys, DB-URL creds, emails, SSNs, phone
  numbers, long hex/base64 blobs) are replaced with `[redacted: possible
  secret/PII]`; control characters (except tab/newline) are stripped and
  over-long values truncated.
- **Validated fields.** `prompt_hash` must be a hex digest or it's dropped (so
  raw prompt text can't be smuggled in); `confidence` is clamped to `[0,1]` with
  non-finite values falling back to `0.5`, and the writer refuses to emit
  `NaN`/`Infinity` to the file (`allow_nan=False`).
- **Corruption-safe.** A non-empty ledger that can't be parsed (or isn't the
  expected object shape) is moved aside to `*.corrupt` rather than silently
  overwritten.

The redactor is pattern-based defense-in-depth, not a guarantee: a novel
secret format or plain-English PII (a name, a street address) can still slip
through. Prompts themselves are only ever hashed, never stored.

## Data Retention

This skill stores two local files inside the skill directory (`~/.claude/skills/pronoun-resolver/.claude/`):

- **pronoun-ledger.json** — resolution metadata (pronoun, resolved referent, confidence tier, correction status). Prompts are hashed, never stored as text.
- **pronoun-resolver-analytics.jsonl** — per-message stats (timestamp, flag count, word count). No message content is stored.

No data is sent externally. Both files are local-only and can be deleted at any time without affecting functionality. To clear all stored data: `rm ~/.claude/skills/pronoun-resolver/.claude/pronoun-ledger.json ~/.claude/skills/pronoun-resolver/.claude/pronoun-resolver-analytics.jsonl`

## File Structure

```
pronoun-resolver/
  SKILL.md                  # Skill definition + resolution framework
  README.md                 # This file
  bin/
    detect-pronouns.sh      # Hook entry point — regex + orchestration
    detect-implicit.py      # Bare imperative heuristic detector
    log-resolution.py       # Locked, sanitizing ledger writer (the learning loop)
    stats.py                # Analytics summary display
  .claude/
    pronoun-ledger.json     # Resolution metadata (auto-created)
    pronoun-resolver-analytics.jsonl  # Per-message stats (auto-created)
  tests/
    test_log_resolution.py  # Unit tests for the ledger writer + sanitizer
  evals/
    cases.json              # Eval test cases
    results.json            # Eval results
```

## Tests

```bash
python3 tests/test_log_resolution.py   # ledger writer, sanitizer, concurrency (no deps)
```

The `evals/` suite exercises resolution *behavior* via the `claude` CLI and is
separate from these deterministic unit tests.

## Install

### 1. Clone/symlink the skill

```bash
git clone https://github.com/kaicianflone/coding-pronoun-prompt-resolver.git
ln -s "$(pwd)/coding-pronoun-prompt-resolver" ~/.claude/skills/pronoun-resolver
```

### 2. Add the hook to `~/.claude/settings.json`

```json
{
  "hooks": {
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
  }
}
```

Replace the path with your actual absolute path. The hook requires an absolute path.

## Configuration

### Disable for a project

```bash
mkdir -p .claude && touch .claude/pronoun-resolver-disabled
```

### Re-enable

```bash
rm .claude/pronoun-resolver-disabled
```

### Reset the ledger

```bash
rm ~/.claude/skills/pronoun-resolver/.claude/pronoun-ledger.json
```

## Requirements

- Python 3.6+ (for bare imperative detection)
- Bash 4+ (for arrays)
- Claude Code with hooks support

## License

MIT
