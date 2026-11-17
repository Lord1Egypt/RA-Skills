# open-vercel

A small browser utility for opening **Open Vercel** in Brave.

## What it does

- Opens `https://vercel.com/`
- Reuses an existing matching tab when possible
- Reuses the user's existing browser session
- Verifies the destination
- Stops safely if authentication is required
- Never handles credentials

## Example triggers

- Open Vercel
- Take me to Vercel
- Go to Vercel

## Installation

Place the `open-vercel` folder under your agent's skills directory:

```text
skills/
└── open-vercel/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave browser automation.

## Privacy

This skill does not request or store passwords, API keys, authentication codes, or other credentials.
