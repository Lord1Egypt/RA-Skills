# open-instagram

A lightweight browser skill that opens **Instagram** in Brave.

## What it does

- Opens `https://www.instagram.com/`
- Reuses an existing Instagram tab when possible
- Reuses the user's existing browser session
- Avoids duplicate tabs
- Verifies that Instagram loaded
- Never handles credentials

## Example triggers

- "Open Instagram"
- "Take me to Instagram"
- "Go to Instagram"
- "Visit Instagram"

## Installation

Place the `open-instagram` folder under your agent's skills directory:

```text
skills/
└── open-instagram/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Privacy

This skill does not request, store, or enter passwords, API keys, authentication codes, or other credentials.
