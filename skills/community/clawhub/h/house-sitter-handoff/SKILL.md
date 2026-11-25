---
name: house-sitter-handoff
description: Generates the leave-behind briefing packet for whoever watches your home, pets, and plants. Structured home registry -> printable HANDOFF.md + one-page EMERGENCY_CARD.md, with a completeness audit that refuses to call a packet ready when pets exist without a vet, no emergency contact, or alarm codes left lying in plaintext. Covers feeding routines, quirky locks, breaker/water-shutoff locations, trash days, plant watering, escalation tree.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [travel, pets, house-sitting, handoff, safety, checklist]
---

# House-Sitter Handoff

You're leaving for a week. Someone trustworthy is staying or checking in.
The packet you leave them decides whether your trip is quiet or a stream of
"how does the shower faucet work???" texts at 2 AM their time.

This skill turns a structured JSON description of your home into a
**printable handoff document** and a **fridge-door emergency card**, and
audits it for the gaps that actually ruin sitting gigs.

## When to trigger
- "we're going away, need to write instructions for the house sitter"
- "pet sitter coming, what do I need to tell them"
- "what should I leave for someone watching my house"
- annual pre-vacation handoff refresh, or after anything changes
  (new heating, new alarm, new pet)

## How it works

1. **Fill the registry** (copy `sample_home.json` as a template): household
   basics, pets with feeding/meds, plants, trash days, house quirks
   (tricky locks, temperamental boiler), utility shutoff locations,
   contacts, and a "what to do if X" escalation list.
2. **Audit first**: `python3 scripts/build_brief.py sample_home.json --audit-only`
   - CRITICAL findings: pets without a vet phone; no emergency contact;
     no heating-failure instruction in winter (registry `winter` flag);
     alarm mentioned but no handoff protocol for the code.
   - WARN: secrets hygiene — the generator deliberately keeps alarm codes
     and door keypad PINs OUT of the printed doc (verbal/split handoff),
     unless you explicitly opt in with `"in_doc": true`.
3. **Generate**: `python3 scripts/build_brief.py sample_home.json --out-dir out/`
   - `HANDOFF.md` — the full briefing, ordered by how sitters actually
     read (first 30 minutes → daily routine → weekly → "if something
     goes wrong").
   - `EMERGENCY_CARD.md` — one page: key phones, shutoffs, vet, poison
     line, "call owner before spending >X" rule.
4. **Hand over properly**: printed doc + verbal walkthrough of anything
   marked quirk; emergency card goes on the fridge.

## Pitfalls encoded
- **Alarm codes in writing get photographed and shared.** Default policy:
  verbal handoff, or split code across two channels; the audit flags any
  `code` fields not marked `in_doc`.
- **Pets without vet info** is the #1 critical gap — emergencies don't
  respect office hours.
- **Heating failure in winter = burst pipes**: the packet must say where
  the water main shutoff is BEFORE that matters (audit checks).
- Sitters won't re-read a wall of text — the doc is front-loaded:
  today's routine fits on page 1, deep detail lives later.
- "Spare key under the pot" belongs in the doc only as *where the sitter's
  key is*, not as a broadcast location — write it as a named hiding place.

## Examples

```bash
# 1. Audit readiness (exit 1 if CRITICAL gaps)
python3 scripts/build_brief.py sample_home.json --audit-only

# 2. Generate packet into ./out/
python3 scripts/build_brief.py sample_home.json --out-dir out/

# 3. Winter mode audit (adds heating-failure requirement)
python3 scripts/build_brief.py sample_home.json --audit-only --winter
```

## Output contract
- CRITICAL/WARN audit list with exact missing fields
- HANDOFF.md: first-30-minutes list, daily/weekly routines per pet+plant,
  quirks, shutoffs, contacts, escalation playbook
- EMERGENCY_CARD.md: fridge one-pager
