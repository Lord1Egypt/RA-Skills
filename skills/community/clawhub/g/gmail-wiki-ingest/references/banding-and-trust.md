# What the server does with a verdict

Background for anyone editing `rubric.md`. **None of this is reachable from the
skill** — it is here so that a rubric change is made with the consequences in
view, not so the agent can aim at a band.

Source: `javis-server/app/services/skill_preferences.py` (the skill-agnostic
rails) and the gmail bindings in `app/services/gmail_wiki_ingest.py`. Specs:
`2026-08-27-gmail-cold-launch-bands-design.md`, and §PR 1 of
`javis.is/docs/superpowers/specs/2026-08-28-gmail-wiki-ingest-skill-migration-design.md`.

## The band

```python
def resolve_band(score, trusted, *, high_cut, low_cut):
    if score < low_cut:                  return LOW
    if score >= high_cut and trusted:    return HIGH
    return MIDDLE
```

| band | what happens |
|---|---|
| **LOW** | no card, no page. An auto-discard row on the ledger, `source='auto'`. |
| **MIDDLE** | a pending `SkillData` row — the review card the user answers with Confirm / Discard. This is the day-one behavior and still the common case. |
| **HIGH** | auto-confirmed and distilled into the wiki on the spot, with an undo offered on the card for a bounded window. |

**The score alone never reaches HIGH.** The measured bands overlap — true-keep
mail scores as low as 0.70, unwanted mail as high as 0.80 — so no cut point
separates them, and a trusted actor is what earns the bypass. This is the
load-bearing safety property; the E2E plan asserts it twice (TC8 end to end,
plus a direct `resolve_band(0.99, trusted=False, …)` unit assertion).

Gmail's defaults, all env-overridable for cold-launch tuning: `low_cut = 0.6`,
`high_cut = 0.8`, `trust_min = 3`, `trust_window_days = 90`.

**The cuts are a low-tail trim, not a precision knob.** Raising `high_cut`
does not fix precision — the category gate and the machine-mail filter are what
do that. If unwanted mail is reaching the wiki, the fix is almost always
`rubric.md`, which is the entire reason the judging moved out here and the
reason it is its own file.

## Trust

```python
trusted = confirms >= trust_min and discards_in_window == 0
```

- `confirms` is **unbounded in time** — an actor who earned trust keeps it until
  something revokes it.
- `discards_in_window` is **windowed**, because a revocation is a statement
  about the actor *now*.
- Which clause carries the gate matters: `>= trust_min` confirms **grants**;
  zero discards only ever **revokes**. An unseen sender satisfies the discard
  clause vacuously, so that clause can never be the whole rule. The predicate
  reads simplifiable and is not.
- Only `source='user'` rows are counted. Letting the machine's own auto-confirms
  feed the trust that authorized them is a loop that ends with the wiki full of
  whatever it ingested first.

## The ledger

`skill_preference_decisions` — one row per decision, per skill:
`subject_key`, `actor`, `title`, `related_to`, `reason`, `category`, `score`,
`decision`, `source`, `decided_at`.

It is three things at once, which is why it is written before anything is
deleted:

1. the trust count above,
2. the ≤20-row replay handed back in `recent_decisions` — the whole learning
   mechanism, no training and no embeddings,
3. the audit trail that makes a cut point answerable against real outcomes.

Two orderings are load-bearing on the confirm side and must never be relaxed:
`record_decisions` runs **before** `/skill/data/discard` deletes the row, and
`undo_ingest` runs before that delete too. A discard whose ledger row never
landed is a discard the audit trail lost, and — worse — one the trust
calculation will never see.

## Two kill switches, not one

`SkillDispatchState.consecutive_discards` is a **per-skill** kill switch: enough
consecutive discards and the skill stops being run for that user at all.
`actor_trust` is **per-actor** learning. They are complementary and both remain
— neither is a substitute for the other, and disabling one because the other
exists has been considered and rejected.

## Why "the agent proposes, the server disposes" is structural

Banding never leaves Python, so a confused or prompt-injected agent cannot
auto-confirm anything: the worst it can do is score honestly-labelled mail
wrongly, which lands a MIDDLE card in front of the user — exactly the state the
system is designed around. That containment is what makes it safe to put the
rubric in an editable, ClawHub-shipped prompt in the first place — and, since
the `content` command, what makes it safe for the agent to read message bodies
before anyone has approved them. The injection surface grew; the blast radius
did not. Every gate in this file runs after the agent is finished.
