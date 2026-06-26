# Pet Companion Journal

Local-first pet profiles, journals, health notes, feeding logs, reminders, and compact reports.

## Quick Start

Use a temporary data directory for demos:

```bash
export PET_COMPANION_HOME=/tmp/pet-companion-demo
python3 scripts/pet_manager.py create --pet-id tofu --name Tofu --species cat --breed Ragdoll --birthday 2022-05-01
python3 scripts/record_add.py --pet-id tofu --type health --title "Annual checkup" --body "Vet said overall condition looked normal; follow up on dental cleaning." --tags vet dental
python3 scripts/record_query.py --pet-id tofu --type health --keyword dental
python3 scripts/reminder_manage.py add --pet-id tofu --title "Dental follow-up" --reminder-type follow-up --due-at 2026-07-01T09:00:00+08:00
python3 scripts/export_report.py --pet-id tofu
```

Without `PET_COMPANION_HOME`, data is stored in `~/.pet-companion/`.

## Verification

```bash
python3 -m py_compile scripts/*.py
python3 scripts/verify.py
```

The verification script uses a temporary data directory and covers profile creation, health record writing, querying, reminders, and report export.

## Safety

This is not a veterinary diagnosis or treatment tool. It can organize symptoms, clinic notes, medications, vaccines, and follow-ups, but urgent symptoms should be directed to prompt veterinary care.

Urgent examples include breathing difficulty, collapse, seizures, suspected poisoning, severe bleeding, repeated vomiting, inability to urinate, major trauma, or rapidly worsening pain.

## Privacy

The skill is local-first. Do not share pet photos, clinic details, home context, or identifying records unless the user explicitly asks.
