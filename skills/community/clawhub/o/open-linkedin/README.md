# open-linkedin

A lightweight browser skill that opens **LinkedIn** in Brave.

## What it does

- Opens `https://www.linkedin.com/`
- Reuses an existing LinkedIn tab when possible
- Reuses the user's existing browser session
- Avoids duplicate tabs
- Verifies that LinkedIn loaded
- Never handles credentials

## Example triggers

- "Open LinkedIn"
- "Take me to LinkedIn"
- "Go to LinkedIn"
- "Visit LinkedIn"

## Installation

Place the `open-linkedin` folder under your agent's skills directory:

```text
skills/
└── open-linkedin/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Privacy

This skill does not request, store, or enter passwords, API keys, authentication codes, or other credentials.
