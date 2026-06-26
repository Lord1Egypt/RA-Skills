
---
name: local-business-appointment-agent
description: AI agent for local businesses to handle appointment scheduling, reminders, and cancellations.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "node",
              "bins": ["node"],
              "label": "Install Node.js",
            },
          ],
      },
  }
---

# Local Business Appointment Agent

AI agent for local businesses (salons, clinics, etc.) to automate appointment scheduling, reminders, and cancellations.

## Features

- 24/7 appointment booking via chat
- Automated reminders (SMS/email)
- Cancellation and rescheduling handling
- Calendar integration (Google Calendar, Outlook)

## Usage

1. Configure business hours and services
2. Connect calendar
3. Deploy to website or messaging platform

## Installation

```bash
npm install
```

## Start

```bash
node index.js
```
