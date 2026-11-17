# Lexicon — Persistence and Lifecycle

The lexicon is what makes repairs compound instead of repeat. Everything persistent lives in `~/Clawic/data/listen/`. If you have data at an old location (`~/listen/` or `~/clawic/listen/`), move it to `~/Clawic/data/listen/`.

```
~/Clawic/data/listen/
├── lexicon.md      # correction pairs, patterns, never list
└── config.yaml     # the variables from SKILL.md Configuration
```

## Entry Format (canonical)

One line per pair:

```
wrong → right | status: candidate|confirmed|never | last seen: YYYY-MM-DD
web look → webhook | confirmed | 2026-07-23
one → Juan (es name) | confirmed | 2026-07-20
coffee → kafka | candidate | 2026-07-23
```

- Parenthetical after the right side is an optional scope tag: language (`es name`, `multilingual.md`) or type (`person`, `branch`). A scoped entry fires only when context matches; unscoped fires everywhere — scope any pair whose wrong side is a word the user legitimately says.
- Optional sections for structure when the file grows: `## Pairs`, `## Patterns`, `## Never`. Patterns are one-line observed regularities that widen candidate generation ("brand names get lowercased", "L1 Spanish: b/v swaps") — never auto-applied, only used as signals.

## Lifecycle (SKILL.md Rule 3, operational form)

```
first sighting ──► candidate     apply + surface ("...on Kubernetes, got it")
second sighting ─► confirmed     apply silently
user rejects ────► never         exempt from flagging, forever until user revokes
```

- Promotion requires two independent sightings — two messages, not one message containing the token twice.
- Demotion is single-strike at any stage: one rejection outweighs any number of sightings, because a rejection is ground truth and sightings are inference.
- `never` also takes direct entries without a wrong side: codenames and slang spotted in the user's world (`names.md`) — write `krakatoa | never | <date>`.

## Loading and Applying

- Load the lexicon before interpreting any voice message. Order of application: `never` check first (exempts tokens from flagging), then `confirmed` pre-emptive substitutions, then `candidate` entries as top-priority candidates in the repair pipeline (`repair.md`).
- Write new pairs immediately after the exchange that produced them — session end loses everything held in memory (SKILL.md Traps).
- Never log pairs from noise-storm messages (`degraded.md`): acoustic errors stored as lexical pairs poison future repairs.

## Pruning

- Drop entries whose `last seen` is older than `lexicon_ttl_days` (default 90): stale pairs from a finished project cause wrong repairs in the next one ("coffee → kafka" misfires hard once the user actually discusses coffee).
- Keep the active file under ~50 lines. Every entry is prompt budget spent on each voice message; past ~50, promote the recurring terms upstream to engine biasing (`tuning.md`) — that is the natural graduation path, not deletion.
- Touch `last seen` whenever an entry fires, or TTL will prune your most reliable pairs at the same age as dead ones.
- `never` entries age too, at the same TTL — a codename from a finished project eventually stops deserving its exemption.

## config.yaml

Keys mirror the SKILL.md Configuration table exactly; values are short:

```yaml
dictation_mode: cleaned
number_echo: actions-only
confirmation_posture: standard
languages: [en, es]
lexicon_ttl_days: 90
# test sentence for tuning verification (tuning.md):
# "Sara Kowalski deploys Krakatoa webhooks to the Kubernetes cluster at 8:15"
```

- config is what the user declared; the lexicon is what the agent observed. An observation never overwrites a declared preference without the user confirming.
- Universal variables (locale, timezone, currency) fall back to `~/Clawic/profile.yaml` when unset here; precedence: this config > profile > table default.
