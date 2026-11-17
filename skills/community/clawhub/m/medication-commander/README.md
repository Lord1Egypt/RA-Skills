# Medication Commander

An agent skill for managing medication schedules, detecting drug interactions, tracking adherence, and generating refill reminders.

## Features

- 🕐 **Safe Schedule Generation** — conflict-free daily medication timeline
- ⚠️ **Drug Interaction Detection** — 30+ common drug pairs with severity ratings
- ✅ **Adherence Tracking** — records taken/missed doses, calculates compliance %
- 🔔 **Refill Reminders** — flags medications running low
- 📋 **Printable Checklist** — daily checklist for print or screen reader

## Installation

Copy the skill folder into your agent's skills directory:

```bash
cp -r medication-commander /path/to/skills/
```

## Usage

```bash
# Generate a daily schedule
python3 scripts/medication_commander.py schedule medications.json

# Check for drug interactions
python3 scripts/medication_commander.py interactions medications.json

# Printable daily checklist
python3 scripts/medication_commander.py checklist medications.json

# Refill status
python3 scripts/medication_commander.py refills medications.json
```

### Example medications.json

```json
[
  {
    "name": "Metformin",
    "dose": "500 mg",
    "frequency": "twice daily",
    "times": ["08:00", "20:00"],
    "pills_remaining": 42,
    "pills_per_dose": 1
  }
]
```

## Input Format

Each medication entry:

| Field | Type | Description |
|---|---|---|
| `name` | string | Medication name |
| `dose` | string | Dosage (e.g., "500 mg") |
| `frequency` | string | How often (e.g., "once daily", "twice daily") |
| `times` | list | Times in 24h HH:MM format |
| `pills_remaining` | int | Current supply count |
| `pills_per_dose` | int | Pills taken per dose |

## Output

All commands output JSON to stdout (except `checklist`, which outputs plain text).

## Reference Documentation

- [Interaction Database](references/interactions.md) — full list of 30+ monitored drug pairs
- [Usage Guide](references/usage.md) — detailed command reference and output examples

## Safety Disclaimer

⚠️ **Not medical advice.** This tool is for organizational purposes only. Always consult a licensed healthcare provider regarding medication interactions, dosing, and treatment decisions.

## License

MIT © Denis Voronin
