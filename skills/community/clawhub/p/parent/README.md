<div align="center">

# parent.skill 👨‍👩‍👧

**One baby. One profile. Every caregiver in sync.**

No more "did she eat?" texts. No more "what time was her last nap?" calls.
Everyone asks the same skill. Everyone gets the same answer.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-blue)](https://clawhub.ai)
[![Hermes](https://img.shields.io/badge/Hermes-compatible-purple)](https://github.com/NousResearch/hermes-agent)

</div>

---

⚠️ **Not medical advice.** This skill tracks patterns and routines. Baby is sick? Call your pediatrician.

---

## What is parent.skill?

A shared parenting co-pilot. One baby profile that mom, dad, grandparents, and babysitter all access. It learns YOUR baby's specific feeding rhythm, sleep patterns, cry signals, and what actually works to soothe them.

At 3am when nothing works, you ask "what usually helps?" and get a ranked list based on YOUR baby's actual history.

## The Soothing Playbook

The feature that makes this different from every baby app:

```
Soothing Playbook for Emma (3 months)

1. Bouncing on yoga ball     — 85% (34/40 times)
2. White noise (dryer sound) — 78% (28/36 times)
3. Driving in car            — 95% ⚠️ not practical at 3am
4. Nursing                   — 70% (depends on hunger)
5. Dad walking + humming     — 65% (better after 6pm)
```

No book has this list. Only YOUR data does.

## Key Features

**Feeding Tracker** — times, amounts, new food reactions, pattern detection

**Sleep Intelligence** — wake windows, nap quality, schedule shift detection

**Cry Decoder** — learns what YOUR baby's different cries mean over time

**Multi-Caregiver Sync** — mom, dad, grandma, babysitter all share one truth

**Milestone Journal** — "she smiled today" → logged with date forever

**Pattern Detection** — "she's been waking earlier each day this week"

## Quick Example

```
You (3am):  "She's crying, I don't know why"

Skill:      Last feed was 11pm (4h ago, longer than her usual 3h15m gap).
            Probably hungry. If feeding doesn't help, white noise
            has worked 78% at this hour.
```

```
You (6pm):  "How was her day? Just got home."

Skill:      Good day. Napped twice (45min + 1h20min). Ate 4 times.
            Tried banana — made a face but ate it. Fussy at 5pm
            (the usual). Grandma used yoga ball. Due for evening
            feed in 20 minutes.
```

## Privacy & Data

- **All data stored locally** at `~/.parent-skill/children/`
- **No cloud sync.** No external transmission.
- **No connection to baby monitors, health apps, or any external service.**
- **Delete anytime.** Remove the folder to delete all data.
- **Not medical advice.** Ever.

## Install

```bash
# OpenClaw
clawhub install realteamprinz/parent

# Hermes Agent
hermes skills install parent-skill

# Claude Code
cp -r parent-skill/ ~/.claude/skills/
```

## Part of the Family

Parenting tier:
- 👨‍👩‍👧 **parent.skill** — Unified parenting co-pilot ← You are here
- 👩 [mom.skill](https://clawhub.ai/realteamprinz/mom) — Mom-specific features
- 👨 [dad.skill](https://clawhub.ai/realteamprinz/dad) — Dad-specific features

Peer tier:
- 🤜 [brother.skill](https://clawhub.ai/realteamprinz/brother) — Distill your bros
- 💅 [sister.skill](https://clawhub.ai/realteamprinz/sister) — Distill your sisters

Legacy tier:
- 🤱 [mother.skill](https://clawhub.ai/realteamprinz/mother) — Preserve her wisdom
- 👔 [father.skill](https://clawhub.ai/realteamprinz/father) — Preserve his legacy
- 👵 [grandma.skill](https://clawhub.ai/realteamprinz/grandma) — Her stories and recipes
- 👴 [grandpa.skill](https://clawhub.ai/realteamprinz/grandpa) — His stories and strength

Other:
- 🐾 [paw.skill](https://clawhub.ai/realteamprinz/paw) — Distill your pet's soul
- 💰 [midas.skill](https://clawhub.ai/realteamprinz/midas) — Extract wealth systems
- 👔 [colleague.skill](https://clawhub.ai/realteamprinz/colleague) — Institutional knowledge

> *"We distill what time takes away."*
>
> Built by [@realteamprinz](https://github.com/realteamprinz) · [PRINZCLAW](https://prinzclaw.ai)

## License

MIT License
