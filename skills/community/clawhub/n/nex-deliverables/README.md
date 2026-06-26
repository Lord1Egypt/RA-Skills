# Nex Deliverables

Client Deliverable Tracker for agency operators and freelancers. Monitor project status, track deadlines, manage client workload, and generate professional status updates.

## Features

- **Track Deliverables**: Manage projects across multiple clients with status tracking (planned, in progress, review, delivered, approved, rejected)
- **Client Management**: Store client information, contact details, and retainer information
- **Deadline Tracking**: Set deadlines and automatically get alerts for overdue items
- **Workload Overview**: See the big picture of all active projects by status, priority, and type
- **Status Updates**: Generate professional email updates for clients summarizing deliverable status
- **Search & Filter**: Find deliverables by client, status, type, priority, or search terms
- **Export Data**: Export all deliverables to CSV or JSON for reporting
- **Statistics**: Track delivery performance metrics (delivery rate, average time to deliver, overdue percentage)
- **Local Storage**: All data stored locally in SQLite—no external services, no telemetry

## Installation

```bash
bash setup.sh
```

## Quick Start

Add a client:
```bash
nex-deliverables client add --name "Acme Corp" --email "contact@acme.com"
```

Add a deliverable:
```bash
nex-deliverables add --client "Acme Corp" --title "Website redesign" --type website --deadline 2026-05-01 --priority high
```

List all deliverables:
```bash
nex-deliverables list
```

Mark as delivered:
```bash
nex-deliverables mark "Website redesign" delivered
```

View workload:
```bash
nex-deliverables workload
```

Generate status email:
```bash
nex-deliverables email "Acme Corp"
```

## Full Documentation

See `SKILL.md` for complete command reference and examples.

## Data Storage

All data is stored locally at `~/.nex-deliverables/deliverables.db`. No data is sent to external services.

## Requirements

- Python 3.9+
- SQLite 3 (included with Python)

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

## Support

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs
