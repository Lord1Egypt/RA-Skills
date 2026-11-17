# open-notion

A small browser skill that opens Notion in Brave and takes the user to their Notion workspace/dashboard when an existing authenticated session is available.

## What it does

- Opens `https://www.notion.com/`
- Reuses an existing Notion tab when possible
- Reuses the user's existing authenticated Brave session
- Attempts to reach the workspace/home area after authentication
- Stops safely at login if authentication is required
- Never handles credentials

## Example triggers

- "Open Notion"
- "Take me to Notion"
- "Open my Notion workspace"
- "Go to my Notion dashboard"

## Installation

Place the `open-notion` folder under your agent's skills directory.

Example:

```text
skills/
└── open-notion/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave, while allowing the browser automation layer to focus an existing Brave session.

## Privacy

This skill does not request or store passwords, API keys, authentication codes, or other credentials.
