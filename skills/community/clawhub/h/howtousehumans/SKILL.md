---
name: howtousehumans
description: >-
  Umbrella skill for the HowToUseHumans collection: catalog of all published life-survival agent skills, install commands, and pointers to the maintainer heartbeat checklist. Use when the user installs the whole collection, needs a slug list, or wants orientation before picking a topic-specific skill.
metadata:
  category: life
  tagline: >-
    Full catalog of HowToUseHumans skills: install the collection, browse slugs and ClawHub links, then open heartbeat.md for maintainer checks.
  display_name: "HowToUseHumans (collection)"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-26"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install howtousehumans"
---

# HowToUseHumans (collection)

Agent skills for surviving real life: money, work, housing, health, relationships, home and outdoor skills, safety, and rights. Each topic lives in its own skill under `howtousehumans/<slug>`. This file is the **general install** orientation: what is in the pack, how to install, and where to find the operational **heartbeat** checklist.

## Heartbeat

For maintainers and agents doing periodic health checks (build sync, publish, site smoke tests), read **`heartbeat.md`** in this same directory as this `SKILL.md`.

## Install

```bash
npx clawhub install howtousehumans
npx clawhub install howtousehumans/<skill-slug>
```

Repository layout (source of truth): `skills/<slug>/SKILL.md` per topic. This directory (`skills/howtousehumans/`) holds the collection index plus `heartbeat.md`.

## Skills in this collection

Each line is the slug; the canonical browse URL on ClawHub is `https://clawhub.ai/howtousehumans/<slug>`. The bullet list between the HTML comments is rewritten by `npm run build:skills` (including from `clawhub:prepare` / `skills:prepare`).

<!-- HOWTOUSEHUMANS_SKILL_CATALOG_BEGIN -->
- [addiction-self-assessment](https://clawhub.ai/howtousehumans/addiction-self-assessment)
- [adult-social-skills](https://clawhub.ai/howtousehumans/adult-social-skills)
- [ai-scam-defense](https://clawhub.ai/howtousehumans/ai-scam-defense)
- [anxiety-emergency](https://clawhub.ai/howtousehumans/anxiety-emergency)
- [austerity-living](https://clawhub.ai/howtousehumans/austerity-living)
- [basic-home-repair](https://clawhub.ai/howtousehumans/basic-home-repair)
- [basic-masonry](https://clawhub.ai/howtousehumans/basic-masonry)
- [basic-plumbing-troubleshooting](https://clawhub.ai/howtousehumans/basic-plumbing-troubleshooting)
- [beekeeping-basics](https://clawhub.ai/howtousehumans/beekeeping-basics)
- [benefits-navigator](https://clawhub.ai/howtousehumans/benefits-navigator)
- [blue-collar-mental-health](https://clawhub.ai/howtousehumans/blue-collar-mental-health)
- [body-mechanics-injury-prevention](https://clawhub.ai/howtousehumans/body-mechanics-injury-prevention)
- [boundaries-saying-no](https://clawhub.ai/howtousehumans/boundaries-saying-no)
- [budget-meal-prep](https://clawhub.ai/howtousehumans/budget-meal-prep)
- [burnout-recovery](https://clawhub.ai/howtousehumans/burnout-recovery)
- [career-reinvention](https://clawhub.ai/howtousehumans/career-reinvention)
- [caregiving-physical-skills](https://clawhub.ai/howtousehumans/caregiving-physical-skills)
- [chainsaw-tree-work](https://clawhub.ai/howtousehumans/chainsaw-tree-work)
- [childcare-essentials](https://clawhub.ai/howtousehumans/childcare-essentials)
- [clear-thinking](https://clawhub.ai/howtousehumans/clear-thinking)
- [cook-from-scratch](https://clawhub.ai/howtousehumans/cook-from-scratch)
- [dance-movement](https://clawhub.ai/howtousehumans/dance-movement)
- [death-preparation](https://clawhub.ai/howtousehumans/death-preparation)
- [debt-survival](https://clawhub.ai/howtousehumans/debt-survival)
- [difficult-conversations](https://clawhub.ai/howtousehumans/difficult-conversations)
- [electrical-backup-power](https://clawhub.ai/howtousehumans/electrical-backup-power)
- [emergency-financial-triage](https://clawhub.ai/howtousehumans/emergency-financial-triage)
- [emergency-fund-builder](https://clawhub.ai/howtousehumans/emergency-fund-builder)
- [emotional-regulation](https://clawhub.ai/howtousehumans/emotional-regulation)
- [family-emergency-planning](https://clawhub.ai/howtousehumans/family-emergency-planning)
- [fermentation-food-preservation](https://clawhub.ai/howtousehumans/fermentation-food-preservation)
- [fire-skills](https://clawhub.ai/howtousehumans/fire-skills)
- [fishing-basics](https://clawhub.ai/howtousehumans/fishing-basics)
- [fitness-for-desk-workers](https://clawhub.ai/howtousehumans/fitness-for-desk-workers)
- [foraging-wild-edibles](https://clawhub.ai/howtousehumans/foraging-wild-edibles)
- [grief-navigation-basics](https://clawhub.ai/howtousehumans/grief-navigation-basics)
- [grow-food-anywhere](https://clawhub.ai/howtousehumans/grow-food-anywhere)
- [habit-formation](https://clawhub.ai/howtousehumans/habit-formation)
- [hosting-feeding-groups](https://clawhub.ai/howtousehumans/hosting-feeding-groups)
- [hygiene-without-infrastructure](https://clawhub.ai/howtousehumans/hygiene-without-infrastructure)
- [identity-rebuild](https://clawhub.ai/howtousehumans/identity-rebuild)
- [knot-tying-rope-work](https://clawhub.ai/howtousehumans/knot-tying-rope-work)
- [land-assessment](https://clawhub.ai/howtousehumans/land-assessment)
- [layoff-72-hours](https://clawhub.ai/howtousehumans/layoff-72-hours)
- [loneliness-first-aid](https://clawhub.ai/howtousehumans/loneliness-first-aid)
- [mental-reset-suite](https://clawhub.ai/howtousehumans/mental-reset-suite)
- [mentorship](https://clawhub.ai/howtousehumans/mentorship)
- [minor-injury-first-response](https://clawhub.ai/howtousehumans/minor-injury-first-response)
- [money-crisis-ladder](https://clawhub.ai/howtousehumans/money-crisis-ladder)
- [navigation-without-screens](https://clawhub.ai/howtousehumans/navigation-without-screens)
- [negotiation-trade](https://clawhub.ai/howtousehumans/negotiation-trade)
- [neighbor-mutual-aid](https://clawhub.ai/howtousehumans/neighbor-mutual-aid)
- [nutrition-physical-labor](https://clawhub.ai/howtousehumans/nutrition-physical-labor)
- [orchard-fruit-trees](https://clawhub.ai/howtousehumans/orchard-fruit-trees)
- [outdoor-recreation-skills](https://clawhub.ai/howtousehumans/outdoor-recreation-skills)
- [parenting-psychology](https://clawhub.ai/howtousehumans/parenting-psychology)
- [pet-first-aid](https://clawhub.ai/howtousehumans/pet-first-aid)
- [physical-de-escalation](https://clawhub.ai/howtousehumans/physical-de-escalation)
- [play-physical-instrument](https://clawhub.ai/howtousehumans/play-physical-instrument)
- [privacy-cleanup](https://clawhub.ai/howtousehumans/privacy-cleanup)
- [public-speaking-embodied](https://clawhub.ai/howtousehumans/public-speaking-embodied)
- [raising-livestock](https://clawhub.ai/howtousehumans/raising-livestock)
- [record-keeping-documentation](https://clawhub.ai/howtousehumans/record-keeping-documentation)
- [romantic-relationship-maintenance](https://clawhub.ai/howtousehumans/romantic-relationship-maintenance)
- [safe-exit-planner](https://clawhub.ai/howtousehumans/safe-exit-planner)
- [self-defense-fundamentals](https://clawhub.ai/howtousehumans/self-defense-fundamentals)
- [sharpening](https://clawhub.ai/howtousehumans/sharpening)
- [shift-work-recovery](https://clawhub.ai/howtousehumans/shift-work-recovery)
- [sleep-hygiene-overhaul](https://clawhub.ai/howtousehumans/sleep-hygiene-overhaul)
- [small-engine-repair](https://clawhub.ai/howtousehumans/small-engine-repair)
- [soil-water-management](https://clawhub.ai/howtousehumans/soil-water-management)
- [someone-is-struggling](https://clawhub.ai/howtousehumans/someone-is-struggling)
- [start-a-micro-business](https://clawhub.ai/howtousehumans/start-a-micro-business)
- [stoicism-daily-practice](https://clawhub.ai/howtousehumans/stoicism-daily-practice)
- [survival-basics](https://clawhub.ai/howtousehumans/survival-basics)
- [teaching-physical-skills](https://clawhub.ai/howtousehumans/teaching-physical-skills)
- [tenant-rights-housing](https://clawhub.ai/howtousehumans/tenant-rights-housing)
- [textile-clothing-repair](https://clawhub.ai/howtousehumans/textile-clothing-repair)
- [tool-fluency](https://clawhub.ai/howtousehumans/tool-fluency)
- [values-clarification](https://clawhub.ai/howtousehumans/values-clarification)
- [vehicle-survival-kit](https://clawhub.ai/howtousehumans/vehicle-survival-kit)
- [wage-theft-defense](https://clawhub.ai/howtousehumans/wage-theft-defense)
- [water-safety-swimming](https://clawhub.ai/howtousehumans/water-safety-swimming)
- [weather-reading-outdoor-awareness](https://clawhub.ai/howtousehumans/weather-reading-outdoor-awareness)
- [woodworking-maker-basics](https://clawhub.ai/howtousehumans/woodworking-maker-basics)
- [workplace-injury-rights](https://clawhub.ai/howtousehumans/workplace-injury-rights)
<!-- HOWTOUSEHUMANS_SKILL_CATALOG_END -->

## Agent instructions

1. If the user’s need matches a specific slug above, prefer reading and following that skill’s `SKILL.md` rather than improvising from this index alone.
2. If the user is maintaining the repo or release pipeline, open **`heartbeat.md`** next to this file and work through the sections that apply.
3. Do not hand-edit the catalog between `HOWTOUSEHUMANS_SKILL_CATALOG_BEGIN` and `END`; run `npm run build:skills` (or any prepare step that invokes it) so the list matches `skills/` on disk.
