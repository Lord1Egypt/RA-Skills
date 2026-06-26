# Lesson types

## Low-cost routing

### Let local/Ollama handle
- Short feedback classification
- Compact rewrite into 1-2 lines
- Daily-memory candidate detection

### Escalate to stronger model
- Long-term operating rules
- Billing / auth / routing policies
- Safety-sensitive lessons
- Strategic priorities or nuanced intent


## Preference
Use for tone, format, pacing, and report style.

Examples:
- Keep replies concise
- Use voice only when Boss sends voice
- Prefer result-first updates

## Rule
Use for hard defaults and operating constraints.

Examples:
- Prefer Codex OAuth by default; use paid API only after usable OAuth quota is exhausted
- Default to short answers, minimal tools, and minimal context
- Report immediately when blocked or risk rises

## Mistake
Use for repeated errors or preventable failures.

Examples:
- Avoid high token burn without visible output
- Do not treat partial usage logs as billing-grade reconciliation
- Do not assume Telegram media can be downloaded reliably

## Priority
Use for current optimization focus.

Examples:
- First priority: memory continuity
- Current urgent issue: reduce token cost drift
