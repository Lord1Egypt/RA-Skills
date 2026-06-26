---
name: nex-onboarding
description: Comprehensive client onboarding workflow management system for web agencies, design studios, and service providers. Manage complete client setup processes from contract signing through go-live with structured checklists (opstarten), task progress tracking, and bottleneck detection. Create onboarding workflows covering administrative tasks (contract, payment processing, afronding), technical setup (domain configuration, DNS transfers, SSL certificates, email setup), design and branding (logo requests, brand guidelines), content gathering, and communication milestones (welcome emails, kickoff calls, training, feedback collection). Track progress with completion percentages, visual checklists, and status indicators. Mark steps complete, skip steps when clients handle them independently, or block steps when waiting on client input. Identify most commonly blocked steps to improve workflow efficiency. Assign onboarding steps to team members, export progress data for reporting, and view onboarding statistics across multiple active clients. Support different engagement tiers (starter, standard, premium, enterprise) with customizable templates. Perfect for Belgian agency operators who need systematic client onboarding to reduce errors, improve client satisfaction, and scale client acquisition.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      bins:
        - python3
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-onboarding.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Onboarding

Client Onboarding Checklist Runner for agency operators. Manage the complete client setup workflow from contract to go-live, track progress, and ensure nothing falls through the cracks.

## When to Use

Use this skill when the user asks about:

- Starting a new client onboarding
- Tracking onboarding progress for a client
- Marking onboarding steps as complete, blocked, or skipped
- Viewing the next action item in an onboarding workflow
- Managing multiple active onboardings
- Exporting onboarding data
- Viewing onboarding statistics
- Managing onboarding templates

Trigger phrases: "start onboarding", "new client", "nieuwe klant", "checklist", "opstarten", "go-live", "setup client", "next step", "onboarding progress"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, initializes the database, and sets up the command wrapper.

## Available Commands

### Start Onboarding

Start a new client onboarding:

```bash
nex-onboarding start "Bakkerij Peeters" --tier starter --email "info@bakkerijpeeters.be"
```

Options:
- `--email` - Client email address
- `--phone` - Client phone number
- `--tier` - Retainer tier (starter, standard, premium, enterprise)
- `--template` - Template to use (default: default)
- `--assigned-to` - Assign to team member

### Progress

Show complete onboarding progress with checklist:

```bash
nex-onboarding progress "Bakkerij Peeters"
```

Shows:
- Overall progress percentage
- Completed/total steps
- Visual checklist with status indicators
- Next step to work on
- Any blocked steps

### Next Step

Show the next pending step:

```bash
nex-onboarding next "Bakkerij Peeters"
```

Mark it complete with the `--done` flag:

```bash
nex-onboarding next "Bakkerij Peeters" --done --notes "Kickoff call completed"
```

### Complete Step

Mark a specific step as complete:

```bash
nex-onboarding complete "Bakkerij Peeters" 5 --notes "Logo received via email"
```

### Skip Step

Skip a step (e.g., client handles it themselves):

```bash
nex-onboarding skip "Bakkerij Peeters" 12 --reason "Client manages email forwarding"
```

### Block Step

Block a step when waiting on something:

```bash
nex-onboarding block "Bakkerij Peeters" 6 --reason "Waiting for content from client"
```

### List Onboardings

List all active onboardings:

```bash
nex-onboarding list --status active
```

Filter by tier:

```bash
nex-onboarding list --tier starter
```

### Show Details

Show full onboarding details:

```bash
nex-onboarding show "Bakkerij Peeters"
```

### Finish Onboarding

Complete an entire onboarding:

```bash
nex-onboarding finish "Bakkerij Peeters"
```

### Pause Onboarding

Pause an onboarding:

```bash
nex-onboarding pause "Bakkerij Peeters"
```

### Statistics

View onboarding statistics:

```bash
nex-onboarding stats
```

Shows:
- Total and active onboardings
- Completion rate
- Bottleneck steps (most commonly blocked)

### Export

Export onboarding data:

```bash
nex-onboarding export "Bakkerij Peeters" --format json --output bakkerij.json
```

Formats: `json` or `csv`

### Templates

List available templates:

```bash
nex-onboarding template list
```

Show template details:

```bash
nex-onboarding template show default
```

## Default Onboarding Checklist

The default template includes 20 steps across 7 categories:

### Admin
1. Contract & betaling - Contract signed, first payment received
20. Afronding - Complete onboarding, transition to retainer support

### Technical
2. Subdomein aanmaken - Configure demo.clientname.nex-ai.be on Cloudflare
3. GHL sub-account - Create and configure GoHighLevel sub-account
9. DNS overdracht - Point domain to new hosting/Cloudflare
10. Google Analytics/Search Console - Set up analytics and Search Console
11. SSL certificaat - Configure SSL via Cloudflare
12. Email forwarding - Configure email forwarding for client domain
16. Domein live zetten - Switch DNS to production

### Design
5. Logo & branding opvragen - Request logo, colors, fonts from client

### Content
6. Content verzamelen - Request text, photos, testimonials

### Communication
7. Welkomstmail sturen - Send onboarding welcome email with timeline
8. Kickoff call plannen - Schedule first video call with client
17. Klant training - Brief training on CMS/dashboard usage
19. Feedback vragen - Check feedback and satisfaction after 1 week

### Delivery
4. Demo website bouwen - Build demo site on subdomain
18. Handover documentatie - Share login credentials and documentation

### QA
13. Formulieren testen - Test contact forms and automations
14. Mobiel testen - Test website on mobile and tablet
15. Go-live check - Final checklist before go-live

## Data Storage

All data is stored locally in `~/.nex-onboarding/`:

- `onboarding.db` - SQLite database with all onboarding data
- `templates/` - Custom templates directory

## Examples

### Scenario: Starting a new web design project

```bash
# Start the onboarding
nex-onboarding start "ECHO Management" --tier premium --email "info@echo.be" --assigned-to "Kevin"

# Check progress
nex-onboarding progress "ECHO Management"

# Complete first contract step
nex-onboarding next "ECHO Management" --done --completed-by "Kevin"

# Look at next step
nex-onboarding next "ECHO Management"
```

### Scenario: Unblock a waiting step

```bash
# We're waiting on content from client
nex-onboarding block "ECHO Management" 6 --reason "Waiting for testimonials from client"

# Later, when content arrives
nex-onboarding complete "ECHO Management" 6 --notes "Received testimonials via email"

# See updated progress
nex-onboarding progress "ECHO Management"
```

### Scenario: Viewing team workload

```bash
# See all active onboardings assigned to a team member by listing and filtering
nex-onboarding list --status active

# Export for reporting
nex-onboarding export "ECHO Management" --format csv --output echo_progress.csv
```

## Architecture

- `lib/config.py` - Configuration and default template
- `lib/storage.py` - SQLite database layer
- `lib/formatter.py` - Output formatting and display
- `nex-onboarding.py` - CLI interface with all commands

## Requirements

- Python 3.9+
- No external dependencies

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
