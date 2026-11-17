# open-reddit

A lightweight browser skill that opens **Reddit** in Brave.

## What it does

- Opens `https://www.reddit.com/`
- Reuses an existing Reddit tab when possible
- Reuses the user's existing browser session
- Avoids duplicate tabs
- Verifies that Reddit loaded
- Never handles credentials

## Example triggers

- "Open Reddit"
- "Take me to Reddit"
- "Go to Reddit"
- "Visit Reddit"

## Installation

Place the `open-reddit` folder under your agent's skills directory:

```text
skills/
└── open-reddit/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Privacy

This skill does not request, store, or enter passwords, API keys, authentication codes, or other credentials.
