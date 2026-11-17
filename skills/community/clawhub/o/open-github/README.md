# open-github

A small browser utility for opening **Open GitHub** in Brave.

## What it does

- Opens `https://github.com/`
- Reuses an existing matching tab when possible
- Reuses the user's existing browser session
- Verifies the destination
- Stops safely if authentication is required
- Never handles credentials

## Example triggers

- Open GitHub
- Take me to GitHub
- Go to GitHub

## Installation

Place the `open-github` folder under your agent's skills directory:

```text
skills/
└── open-github/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave browser automation.

## Privacy

This skill does not request or store passwords, API keys, authentication codes, or other credentials.
