# open-arxiv

A small browser utility for opening **Open arXiv** in Brave.

## What it does

- Opens `https://arxiv.org/`
- Reuses an existing matching tab when possible
- Reuses the user's existing browser session
- Verifies the destination
- Stops safely if authentication is required
- Never handles credentials

## Example triggers

- Open arXiv
- Take me to arXiv
- Go to arXiv

## Installation

Place the `open-arxiv` folder under your agent's skills directory:

```text
skills/
└── open-arxiv/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave browser automation.

## Privacy

This skill does not request or store passwords, API keys, authentication codes, or other credentials.
