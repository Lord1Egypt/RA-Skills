---
name: party-guest-optimizer
description: "Use when planning a party or dinner and the GUEST LIST is the hard part - who to invite together, who to keep apart, how to seat them, and how to grow a network of strangers into friends. Guest-graph analysis, invite scenarios, and seating charts that maximize spark and minimize clash."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [party-planning, social-graphs, seating-chart, guest-list, events, entertaining]
---

# Party Guest Optimizer

## Overview

The food is the easy part. The guest list is where parties succeed or die:
two feuding friends in one room, one loud dominator at a dinner table of
quiet people, a birthday where the guest of honor knows nobody except the
host. Hosts wing it — and then spend the night doing damage control instead
of enjoying their own party.

This skill treats the guest list as a **graph problem**:

- **Nodes** = guests; **edges** = relationship (know-well / know-awkward /
  strangers) plus per-guest traits: energy (listener↔talker), humor,
  interests.
- **Invite scenarios**: given a candidate pool larger than the budget,
  find the subset that maximizes new-connection potential (strangers who
  share interests) while respecting must-invites and keep-apart pairs.
- **Seating chart**: for a single table (dinner) or pods (stand-up party),
  optimize placement so every guest sits next to at least one comfort
  neighbor and no clash pair is adjacent — simulated annealing over
  adjacency constraints.
- **Mix report**: per-guest briefing — who they already know, who to
  introduce them to and why ("Ana and Tom both climb — start there").

Built for real-world hosting: 6-30 guests, imperfect information, hosts
who know their friends better than any algorithm. The tool computes, you
decide.

## When to Use

- Planning a dinner party: "who sits next to whom?"
- Deciding between invite list variants (budget cap: 10 of these 17 people)
- Blending friend groups (work friends + old friends + partner's family)
- Parties where guests won't know each other — engineered introductions
- Recurring events: track which pairs have already met to keep mixing
- "Is it rude to invite X but not Y?" — model the graph, see isolation risk

**Don't use for:** corporate seating with protocol/hierarchy rules,
weddings with family politics (use a dedicated wedding seating tool —
this works but the constraints are different), or events > ~60 guests
(the annealer gets slow and single-table assumptions break).

## Files

| File | Purpose |
|---|---|
| `scripts/guest_optimizer.py` | Guest-graph tool: `analyze`, `invite`, `seat` subcommands |
| `references/host-playbook.md` | Host craft: introduction scripts, energy balancing, pod design, recovery moves |
| `README.md` | The problem and 60-second intro |

## Usage

Guests are defined in a JSON file (or built interactively):

```json
{
  "guests": [
    {"id": "ana", "energy": 3, "interests": ["climbing", "jazz"], "talker": 4},
    {"id": "tom", "energy": 4, "interests": ["climbing", "tech"], "talker": 5},
    {"id": "lea", "energy": 2, "interests": ["jazz", "garden"], "talker": 2}
  ],
  "edges": [
    {"a": "ana", "b": "tom", "type": "know"},
    {"a": "ana", "b": "lea", "type": "tension"}
  ],
  "keep_apart": [["ana", "lea"]],
  "must_invite": ["tom"]
}
```

```bash
# Overall graph analysis: isolation risks, energy balance, clusters
python3 scripts/guest_optimizer.py analyze party.json

# Pick 10 of 17 candidates: maximize stranger-interest connections
python3 scripts/guest_optimizer.py invite party.json --max 10

# Seating chart for one table of 8 (round or long)
python3 scripts/guest_optimizer.py seat party.json --table 8 --round

# Pods for a 24-person stand-up party (hosts pre-place pods)
python3 scripts/guest_optimizer.py seat big.json --pods 6
```

## The model in 90 seconds

**Edge types:** `know` (comfort +), `close` (comfort ++), `tension`
(clash), `ex` (romantic history — treat as tension unless both confirmed
fine), absent = strangers.

**Invite scoring** for subset S:
```
score(S) = Σ strangers-pairs-shared-interests × 2      (new spark potential)
         + Σ know/close edges inside S × 1             (comfort)
         − Σ tension edges inside S × 4                (clash)
         − isolation_penalty(guests with 0 connections)
         + energy_balance_bonus (mix of talkers/listeners)
```
Greedy + local swap improvement (NP-hard in general; ~17 candidates is
trivial in practice).

**Seating:** seats are a cycle (round table) or path (long table). Each
guest's seat score = comfort of LEFT + RIGHT neighbors + across-table
partner (round tables: the person opposite matters for conversation):
`close` +3, `know` +2, shared-interest strangers +2, `tension` −6,
adjacent extreme talker+extreme listener at a dinner of 2 → mild plus
(complementary), two 5-talkers adjacent → minus (competition).

Simulated annealing: start random, ~5000 iterations, cooling schedule;
accept uphill moves early to escape local optima. Verifies all hard
constraints (keep_apart never adjacent) before printing.

## Workflow

1. Build the guest JSON with the user. Unknown relationships are simply
   absent edges — no guessing required.
2. `analyze` — read isolation risks aloud ("Dana would know nobody — pair
   invite with a friend or skip") and cluster structure.
3. If pool > budget: `invite --max N` — review the suggested subset AND
   the cut list; hosts override (the tool doesn't know Aunt Lea's politics).
4. `seat` — print the chart. Sanity-check against your own knowledge;
   rerun with constraints if needed (`--keep-apart` can be added ad hoc).
5. On party night, use the **mix report** per guest as your introduction
   cheat sheet.

## Common Pitfalls

1. **Over-modeling.** If the host says "those two are fine now," remove
   the tension edge — data serves the host, not vice versa.
2. **Optimizing for strangers too hard.** 100% new-connection parties
   feel like networking events. The scoring already balances; don't crank
   stranger bonuses by hand.
3. **Forgetting +1s.** Partners count as nodes (usually `close` to their
   +1); a seating chart that splits couples at a dinner causes more harm
   than any optimization gain unless it's explicitly a matchmaking event.
4. **The isolated guest.** A guest with zero edges is a hard problem no
   seating chart solves — either give them a "buddy" invite or don't
   invite them to a small dinner. `analyze` flags this first.
5. **Static chart, dynamic party.** Seating charts matter for the first
   45 minutes; after that people move. For stand-ups use pods, not seats.
6. **Talker-listener balance is per-pod, not global.** Six listeners and
   one talker at a table = monologue. Check `energy` in each pod, not
   just the average.

## Example Session

> Host: "Dinner for 8. Maya and Jon divorced last year — different tables
> impossible, different END of table maybe. Priya knows nobody except me."
>
> Build JSON: `keep_apart: [["maya","jon"]]`, maya/jon `tension` edge
> (same-table penalty), priya with interests `[design, trail]`.
> `analyze` → "priya: 0 connections — risk". Add priya's friend Dev
> (knows: priya; interests: trail) → risk clears.
> `seat --table 8 --round` → chart where maya and jon sit maximally apart
> with comfort neighbors between; mix report: "Introduce priya↔sam:
> both trail runners; priya↔dev already close."

## Verification Checklist

- [ ] keep_apart pairs are NOT adjacent (or at the same small table)
- [ ] No isolated guest (everyone adjacent to ≥1 comfort/interest link)
- [ ] Talker/listener balance checked per table or pod
- [ ] Mix report lists a specific, interest-grounded intro per stranger
- [ ] Host reviewed and overrode at least one machine choice (they know
      things the graph doesn't)
