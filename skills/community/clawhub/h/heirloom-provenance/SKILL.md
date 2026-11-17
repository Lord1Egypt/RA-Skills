---
name: heirloom-provenance
description: "Use when someone dies or downsizes and the family objects need their stories captured before the people who know them are gone — structured provenance registry for heirlooms (origin, owner chain, story, appraisal, photo refs, audio-interview transcripts), provenance question scripts for interviewing elderly relatives before it is too late, estate-ready provenance reports for executors and appraisers, printed heirloom labels/tags with QR codes linking to the full record, and fairness tools for distribution (wish-list matching and rotation drafting) so the division of objects does not destroy the family."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [heirlooms, family-history, provenance, estate, genealogy, oral-history]
---

# Heirloom Provenance — Family Object Storyteller

## Overview

Every family has a drawer of objects nobody can explain anymore: the pocket watch, the odd ceramic, the medal in a language nobody reads. The stories die with their keepers — and estates get settled by people who don't know that the worthless-looking chair is the one that survived the fire, or that two siblings have silently wanted the same ring for twenty years.

This skill is a **provenance system for family objects**:

1. **Registry** — each heirloom gets a record: description, origin (when/where/made by whom), owner chain with dates, story (free text, as rich as available), appraisal value, photo references, condition.
2. **Interview kit** — structured question scripts for recording the knowledge while the knowers are alive: object-by-object walk-throughs, prompts that unlock stories ("what did Grandma say about this?"), and an audio-first workflow with transcript linking.
3. **Reports** — estate-ready provenance report per object (for executors, appraisers, insurance) and a family storybook export that turns the registry into readable narrative.
4. **Tags** — printable heirloom labels: object name + ID + QR code pointing to the full record (or a local file reference), so the physical object carries its own story.
5. **Distribution fairness** — when objects must be divided: sealed wish-list collection (who wants what, in order), conflict detection before the family meeting, rotation-draft settlement proposals that respect top wishes, and equalization pricing for the residual.

## When to Use

- **A death in the family** — executor work: inventory, provenance documentation, appraisal support, fair distribution
- **Downsizing / moving a parent to assisted living** — decide what's kept, document why it matters, tag what goes to whom
- **Elderly relatives still alive** — THE critical window: run the interview kit before the stories are gone (the #1 regret families report)
- **Insurance / estate valuation** — structured records with appraisal history that appraisers and insurers actually accept
- **Pre-empting inheritance fights** — sealed wish-lists + conflict detection before emotions peak
- Don't use for: full estate administration (executor accounting, probate law — different domain), museum-grade cataloging (different standards), or digital accounts (digital-legacy covers that).

## How It Works

1. **Record objects** — `object add` with description, origin, owner chain, story, value. IDs are stable (`HL001`).
2. **Interview** — `interview "Aunt Maria"` prints the question script for an object-by-object session (or the whole house walkthrough); record audio separately, link transcripts to objects with `story append`.
3. **Report** — `report HL003` prints the provenance sheet; `storybook` exports the whole registry as narrative markdown.
4. **Tag** — `tag HL003` prints a cut-out label with QR payload (file path or URL to the record).
5. **Distribute** — `wish add HL003 --by "Sam" --rank 1` (sealed: stored per person, revealed together with `wishes`); `conflicts` shows overlap; `draft` computes a settlement maximizing top-wish satisfaction with rotation fairness and prints equalization payments for high-value residuals.

## Commands

```bash
# Registry
python3 scripts/heirloom.py object add "Grandfather's pocket watch" \
    --origin "c.1920s, Zurich, bought by Otto H. Weiss" \
    --owners "Otto H. Weiss (1889-1968) > Maria Weiss (b. 1940)" \
    --story "Otto traded a rifle for it after WWI. Wound it every Sunday." \
    --value 450 --condition "running, worn case"
python3 scripts/heirloom.py story append HL001 "Maria says Otto's father also carried it in the war — unclear which war."
python3 scripts/heirloom.py objects

# Interview kit (do this NOW, while the knowers are alive)
python3 scripts/heirloom.py interview "Aunt Maria"          # whole-collection script
python3 scripts/heirloom.py interview "Aunt Maria" --object HL001

# Reports
python3 scripts/heirloom.py report HL001
python3 scripts/heirloom.py storybook > family_storybook.md

# Tags
python3 scripts/heirloom.py tag HL001

# Distribution fairness
python3 scripts/heirloom.py wish add HL001 --by Sam --rank 1
python3 scripts/heirloom.py wish add HL001 --by Alex --rank 2
python3 scripts/heirloom.py wishes                  # reveals sealed lists together
python3 scripts/heirloom.py conflicts
python3 scripts/heirloom.py draft --people Sam,Alex --seed 7
```

Storage: `heirlooms.json` in cwd. 100% local — family data stays in the family.

## Interview Kit — The Core Questions

The `interview` script is built around prompts that unlock stories rather than facts:

1. "Who did this belong to first, as far as you know?"
2. "Where did it live in the house when you were young?"
3. "What did [owner] say about it? Any sayings attached?"
4. "Was there ever a fight or a funny accident about it?"
5. "Who was 'supposed' to get it? Did anyone ever say?"
6. "Is there anything else in the family that goes with it?"
7. "If this could talk, what's the first story it would tell?"

Record audio; transcribe later; link with `story append`. One session per room, not per object — objects cue each other.

## Common Pitfalls

1. **Waiting for the estate.** Provenance captured after the keeper dies is guesswork. The interview kit exists to be used *early* — at holidays, during downsizing, any visit.
2. **Recording values without stories.** Appraisal value without provenance is just a number; story without value fails at insurance/estate time. Record both; the schema requires both fields (unknown is a valid entry).
3. **Wish-lists shared early.** Sealed wish-lists work because nobody anchors. Collect all first (`wish add`), reveal with `wishes` at the same moment, then run `conflicts`.
4. **Equal split obsession.** Objects are not fungible. `draft` maximizes *wish satisfaction*, not dollar equality; equalization payments cover only large value gaps.
5. **No physical linkage.** A registry nobody can connect to the physical object is worthless after one move. Print tags (`tag`) and attach them.

## Verification Checklist

- [ ] Every family-significant object has a registry record with owner chain
- [ ] At least one interview session recorded per living knowledge-holder
- [ ] Stories linked (audio refs or transcripts appended to object records)
- [ ] Values recorded (or marked unknown) for insurance/estate use
- [ ] Tags printed and attached to objects
- [ ] Wish-lists collected from all parties before any reveal
- [ ] Conflicts identified and settled (or explicitly parked) before division
- [ ] Storybook exported and shared; provenance reports archived with estate papers
