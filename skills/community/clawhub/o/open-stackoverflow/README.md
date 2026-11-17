# open-stackoverflow

A small browser utility for opening **Open Stack Overflow** in Brave.

## What it does

- Opens `https://stackoverflow.com/`
- Reuses an existing matching tab when possible
- Reuses the user's existing browser session
- Verifies the destination
- Stops safely if authentication is required
- Never handles credentials

## Example triggers

- Open Stack Overflow
- Take me to Stack Overflow
- Go to Stack Overflow

## Installation

Place the `open-stackoverflow` folder under your agent's skills directory:

```text
skills/
└── open-stackoverflow/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave browser automation.

## Privacy

This skill does not request or store passwords, API keys, authentication codes, or other credentials.
