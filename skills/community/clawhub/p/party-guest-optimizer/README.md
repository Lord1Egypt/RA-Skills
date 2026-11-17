# Party Guest Optimizer

**The food is the easy part. The guest list is where parties die — and hosts
wing it every time.**

## The problem

Two feuding friends in one room. One loud dominator at a table of quiet
people. A birthday guest of honor who knows nobody except the host. The
host spends the night doing damage control instead of enjoying their own
party — and half the guests never really talk to anyone new.

Everyone knows seating and mixing *matter*. Nobody actually engineers them,
because it's a combinatorial problem hiding inside a social one.

## The solution

Model the guest list as a **graph**: guests are nodes (with talker-energy
and interests), relationships are edges (close / know / tension / ex /
strangers). Then compute:

- **`analyze`** — isolation risks ("Dana would know nobody"), friendship
  clusters, talker/listener energy balance, tension pairs, and the best
  new-connection opportunities (strangers who share interests)
- **`invite`** — when the pool exceeds the budget: pick the subset that
  maximizes new-connection spark + comfort while respecting must-invites
  and keep-apart pairs
- **`seat`** — a seating chart (round or long table) via simulated
  annealing: every guest next to a comfort or shared-interest neighbor,
  tension pairs never adjacent, plus a **mix report** — your per-party
  introduction cheat sheet ("Ana + Tom: both climbers — start there")

Built for real hosting: 6-30 guests, imperfect info, host always overrides
(the tool doesn't know Aunt Lea's politics).

## Quick start

```bash
# interactive guest builder
python3 scripts/build_guests.py -o party.json

# see risks and opportunities
python3 scripts/guest_optimizer.py analyze party.json

# 10 of 17 candidates, budget cap
python3 scripts/guest_optimizer.py invite party.json --max 10

# dinner for 8, round table
python3 scripts/guest_optimizer.py seat party.json --table 8 --round
```

## What you get

```
SEATING CHART (round table, 8 guests)
  seat 1: omar  (L: jon  R: dev)
  seat 2: dev   (L: omar R: maya)   ← maya/jon (exes) never adjacent
  ...
MIX REPORT:
  seated together: maya + dev — both into trail
  introduce: jon + lea (jazz)
```

Plus `references/host-playbook.md`: introduction scripts, energy
management per pod, mid-party recovery moves, and the recurring-party
"met-graph" trick that turns a monthly dinner into a real community.

## Who needs this

- Dinner-party hosts (6-10 guests, one table)
- Party hosts blending friend groups (work + old friends + partner's people)
- Anyone whose recurring event keeps collapsing into the same cliques
- People who want their parties to build their friend group, not just
  entertain it

## Files

- `SKILL.md` — model, workflow, pitfalls, examples
- `scripts/build_guests.py` — interactive JSON builder
- `scripts/guest_optimizer.py` — analyze / invite / seat
- `references/host-playbook.md` — the human craft around the math

## License

MIT © Denis Voronin
