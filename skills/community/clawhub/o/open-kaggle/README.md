# open-kaggle

A small browser utility for opening **Open Kaggle** in Brave.

## What it does

- Opens `https://www.kaggle.com/`
- Reuses an existing matching tab when possible
- Reuses the user's existing browser session
- Verifies the destination
- Stops safely if authentication is required
- Never handles credentials

## Example triggers

- Open Kaggle
- Take me to Kaggle
- Go to Kaggle

## Installation

Place the `open-kaggle` folder under your agent's skills directory:

```text
skills/
└── open-kaggle/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave browser automation.

## Privacy

This skill does not request or store passwords, API keys, authentication codes, or other credentials.
