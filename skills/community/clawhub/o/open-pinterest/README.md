# open-pinterest

A lightweight browser skill that opens **Pinterest** in Brave.

## What it does

- Opens `https://www.pinterest.com/`
- Reuses an existing Pinterest tab when possible
- Reuses the user's existing browser session
- Avoids duplicate tabs
- Verifies that Pinterest loaded
- Never handles credentials

## Example triggers

- "Open Pinterest"
- "Take me to Pinterest"
- "Go to Pinterest"
- "Visit Pinterest"

## Installation

Place the `open-pinterest` folder under your agent's skills directory:

```text
skills/
└── open-pinterest/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Privacy

This skill does not request, store, or enter passwords, API keys, authentication codes, or other credentials.
