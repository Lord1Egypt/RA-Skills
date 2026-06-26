# Nex Onboarding

Client Onboarding Checklist Runner for agency operators. Manage the complete client setup workflow, track progress, and ensure nothing falls through the cracks.

## Installation

1. Clone or extract this skill into your ClawHub skills directory
2. Run the setup script:

```bash
bash setup.sh
```

This will:
- Check for Python 3
- Create the data directory (`~/.nex-onboarding`)
- Initialize the SQLite database
- Create a command wrapper in `~/.local/bin`

3. Add `~/.local/bin` to your PATH if not already there:

```bash
export PATH="$PATH:$HOME/.local/bin"
```

## Quick Start

Start a new client onboarding:

```bash
nex-onboarding start "Bakkerij Peeters" --tier starter --email "info@bakkerijpeeters.be"
```

View progress:

```bash
nex-onboarding progress "Bakkerij Peeters"
```

Mark the next step as complete:

```bash
nex-onboarding next "Bakkerij Peeters" --done
```

## Commands

- `start` - Start a new client onboarding
- `progress` - Show onboarding progress
- `next` - Show or mark next step complete
- `complete` - Mark a specific step complete
- `skip` - Skip a step
- `block` - Block a step (waiting on something)
- `list` - List all onboardings
- `show` - Show full onboarding details
- `finish` - Complete an entire onboarding
- `pause` - Pause an onboarding
- `stats` - View statistics
- `export` - Export onboarding data (JSON/CSV)
- `template` - Manage templates

Run `nex-onboarding --help` for full documentation.

## Default Onboarding Template

The skill includes a default 20-step onboarding checklist optimized for web agencies:

1. Contract & betaling
2. Subdomein aanmaken
3. GHL sub-account
4. Demo website bouwen
5. Logo & branding opvragen
6. Content verzamelen
7. Welkomstmail sturen
8. Kickoff call plannen
9. DNS overdracht
10. Google Analytics/Search Console
11. SSL certificaat
12. Email forwarding
13. Formulieren testen
14. Mobiel testen
15. Go-live check
16. Domein live zetten
17. Klant training
18. Handover documentatie
19. Feedback vragen
20. Afronding

Steps are categorized as: admin, technical, design, content, communication, delivery, qa

## Data Storage

All data is stored locally in `~/.nex-onboarding/`:

```
~/.nex-onboarding/
├── onboarding.db      # SQLite database
└── templates/         # Custom templates
```

No data is sent to external servers. Everything stays on your machine.

## Requirements

- Python 3.9 or higher
- No external dependencies

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

## Support

Built by Nex AI - https://nex-ai.be
