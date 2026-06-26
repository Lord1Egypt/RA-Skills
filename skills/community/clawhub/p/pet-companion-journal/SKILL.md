---
name: pet-companion-journal
description: Create and maintain dedicated archives for each pet, including profiles, daily journals, photos, feeding logs, health records, and care reminders. Use when the user wants to record pet basics such as name and birthday, save pet photos with captions, track food and health history, review warm moments, or manage reminders per pet. Local-first and privacy-conscious.
version: 1.1.0
---

# Pet Companion Journal

## Overview

Use this skill to maintain a local-first companion archive for one or more pets. Record profiles, daily moments, feeding changes, photos, health history, and reminders in a way that stays organized per pet and is easy to search later.

This skill is best for:
- creating or updating pet profiles
- recording daily logs, warm moments, and growth notes
- attaching photos and captions to a pet timeline
- tracking food, supplements, and feeding changes
- storing symptom, clinic, medication, vaccine, and deworming notes
- checking upcoming care reminders
- reviewing a pet’s recent history or exporting a summary

## Workflow

### 1. Identify the pet first
Always determine which pet the record belongs to.

Rules:
- if the household has only one pet, you may infer the pet after a quick confirmation when needed
- if the user has multiple pets and did not specify which one, ask before writing
- for reads, prefer showing likely matches and ask only if ambiguous

Use `scripts/pet_manager.py list` or `view` to inspect existing pets.

### 2. Create or update the pet profile
When the user is creating a profile, collect the minimum useful fields first:
- name
- species
- birthday or approximate age
- breed if known
- gender if known

Optional fields:
- nickname
- adoption date
- neutered status
- color markings
- personality tags
- notes
- avatar photo reference

Use `scripts/pet_manager.py create` and `update`.

### 3. Add records by type
Use `scripts/record_add.py` to save records under the correct pet.

Supported record types:
- `daily`: ordinary daily notes
- `moment`: warm scenes, funny moments, growth milestones
- `photo`: a photo plus caption and optional media path
- `feeding`: food, supplements, quantity, feeding change notes
- `health`: symptoms, clinic visits, medicines, vaccines, deworming, follow-up
- `reminder-note`: notes related to reminders or care planning

If the user gives semi-structured text, store the narrative in the body and place structured fields such as symptom lists, medicine names, or scene labels inside `extra`.

### 4. Manage reminders
Use `scripts/reminder_manage.py` to create or list per-pet reminders.
Use `scripts/reminder_check.py` to find due or upcoming reminders.

Typical reminder types:
- birthday
- vaccine
- deworming
- checkup
- grooming
- bath
- refill-food
- medication
- follow-up

### 5. Query and review
Use `scripts/record_query.py` for structured retrieval.
Support filtering by:
- pet
- record type
- time range
- keyword

Use `scripts/export_report.py` to produce a compact summary for a time range.

## Output Rules

- Keep responses warm, clear, and organized.
- For write actions, confirm what was saved and under which pet.
- For read actions, prefer concise summaries plus the most relevant entries.
- For health-related notes, record and organize them, but do not present veterinary diagnosis.
- If a photo path or detail is uncertain, label it as a note or estimate instead of pretending certainty.

## Storage Rules

Default storage root: `~/.pet-companion/`

For tests, demos, or shared machines, set `PET_COMPANION_HOME` to isolate data:

```bash
PET_COMPANION_HOME=/tmp/pet-demo python3 scripts/pet_manager.py list
```

Structure:
- `pets/`: one JSON profile per pet
- `records/YYYY/MM/`: markdown records with JSON frontmatter
- `reminders/`: one JSON reminder file per pet
- `media/YYYY/MM/`: pet photos or attachment files
- `reports/`: exported summaries if needed

## Verification

Before publishing or after installation, run:

```bash
python3 -m py_compile scripts/*.py
python3 scripts/verify.py
```

The verification script uses a temporary `PET_COMPANION_HOME`, creates a sample
pet profile, writes a health record, queries it, creates a reminder, checks
upcoming reminders, and exports a compact report.

See:
- `references/data-schema.md`
- `references/query-patterns.md`
- `references/template-examples.md`
- `references/safety-boundaries.md`

## Privacy and Safety

This skill is local-first. Do not share pet photos, clinic notes, or identifying details unless the user explicitly asks. This skill may organize health records, but it must not act like a veterinary diagnosis or treatment tool. If the user describes urgent symptoms, advise prompt veterinary care.

Urgent symptom examples include difficulty breathing, collapse, seizures,
suspected poisoning, severe bleeding, repeated vomiting, inability to urinate,
major trauma, or rapidly worsening pain. In those cases, record the note if the
user asks, but keep the response focused on seeking prompt veterinary care.
