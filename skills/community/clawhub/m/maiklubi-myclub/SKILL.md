---
name: maiklubi-myclub
description: "Access Finnish sports club events, invoices, notifications, and RSVP on myclub.fi for AI agents and parents. Works with myclub and MyClub clubs across Finland."
metadata:
  {
    "openclaw":
      {
        "emoji": "⚽",
        "requires": { "bins": ["maiklubi"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "maiklubi",
              "bins": ["maiklubi"],
              "label": "Install maiklubi CLI (npm)",
            },
          ],
      },
  }
---

# maiklubi skill

The maiklubi skill enables AI agents to access Finnish sports club information on myclub.fi. It retrieves upcoming events with RSVP status, open invoices, notifications, event participants, and manages calendar subscriptions for parents and athletes.

## Installation

```bash
npm install -g maiklubi
# then log in once (prompts for email + password, auto-discovers members/clubs):
maiklubi login
```

Credentials are stored in `~/.config/maiklubi/config.json`. Run `maiklubi login` to re-authenticate or switch account, or `maiklubi config clear` to remove the saved account.

## Primary Commands

### Daily summary (recommended starting point for agents)
```bash
maiklubi summary --member <name> --club <club> --json
maiklubi summary --member <name> --club <club> --days 7 --json
maiklubi summary --all-members --json
```
Returns upcoming events (with indication status), open invoices, and recent notifications in one call. Default lookahead: 14 days.

### Events
```bash
# List upcoming events with RSVP status
maiklubi events list --member <name> --club <club> --json
maiklubi events list --member <name> --club <club> --with-participants --json

# RSVP (indicate attendance)
maiklubi events indicate --member <name> --club <club> --id <eventId> --status yes|no|no_response|maybe --json

# Show who is attending an event
maiklubi events participants --member <name> --club <club> --id <eventId> --json

# Read an event's discussion thread (e.g. to summarize carpooling plans)
maiklubi events comments --member <name> --club <club> --id <eventId> --json
```

### Invoices
```bash
# Lists both open and paid invoices (open marked "!", paid marked "✓")
maiklubi invoices list --member <name> --club <club> --json
```

### Notifications
```bash
# List notifications (returns id, title, url)
maiklubi notifications list --member <name> --club <club> --limit 10 --json

# Read the FULL TEXT of one notification (body + links), by id from the list
maiklubi notifications show --member <name> --club <club> --id <notificationId> --json
```

**Important — read myclub for myclub questions, not the web.** Club-internal
information such as **tournament play-groups / team assignments / line-ups**
(e.g. "which Helsinki Cup team is X in"), match times, kit info, and coach
announcements are posted as **myclub notifications**, not on public websites.
To answer these: run `notifications list` to find the relevant item (match by
title, e.g. one containing "Peliryhmät"/"Helsinki Cup"), then
`notifications show --id <id>` to read the full text and find the member's name.
Do NOT use web search for information that lives inside myclub.

### Calendar subscriptions (webcal / iCalendar)
```bash
# List existing subscriptions
maiklubi calendar list --json

# Create a new subscription (returns webcal:// URL)
maiklubi calendar create --member <name> --indication yes --json
```

### Account info
```bash
maiklubi users list --json          # configured family members
maiklubi accounts list --json       # all club memberships from myclub.fi
maiklubi version --json             # current CLI version
```

## Key Concepts

- **member**: A person in your family config (e.g. "Aino", "Veikko"). Use `maiklubi users list` to see available names.
- **club**: The club slug (e.g. "topola", "ppj") or full URL. Required when a member belongs to multiple clubs.
- **indication**: RSVP status — `yes` (attending), `no` (not attending), `no_response` (not yet responded), `maybe`.
- **--all-members**: Run the command for every configured member/club pair. Produces one JSON block per pair.

## Indication Symbols (text output)

- `✓` = yes (attending)
- `✗` = no (not attending)
- `?` = maybe
- `—` = no_response (not yet answered)

## Actionability Guidance

When summarizing for a parent, prioritize:
- Events with `indication = "no_response"` that are within 3 days — these need an RSVP
- Open invoices with a due date within 7 days
- Notifications mentioning schedule changes or mandatory actions

De-emphasize:
- Events already indicated `yes` or `no`
- Notifications that are purely informational (newsletters, results)

## Notes

- All list commands support `--json` for structured output
- Multiple `--member` flags are not supported; use `--all-members` for all members
- The `summary` command is the most efficient single call for an agent briefing
- myclub.fi does not have a separate inbox; club communication is via event comments (shown by `maiklubi events list`) and notifications

## Repository

https://github.com/aikarjal/maiclub (or local build at `~/WorkspacesInStudio/maiklubi`)
