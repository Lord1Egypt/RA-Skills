# open-youtube

A lightweight browser skill that opens **YouTube** in Brave.

## What it does

- Opens `https://www.youtube.com/`
- Reuses an existing YouTube tab when possible
- Reuses the user's existing browser session
- Avoids duplicate tabs
- Verifies that YouTube loaded
- Never handles credentials

## Example triggers

- "Open YouTube"
- "Take me to YouTube"
- "Go to YouTube"
- "Visit YouTube"

## Installation

Place the `open-youtube` folder under your agent's skills directory:

```text
skills/
└── open-youtube/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave browser automation.

## Privacy

This skill does not request, store, or enter passwords, API keys, authentication codes, or other credentials.
