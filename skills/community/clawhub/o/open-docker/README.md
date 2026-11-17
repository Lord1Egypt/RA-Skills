# open-docker

A small browser utility for opening **Open Docker** in Brave.

## What it does

- Opens `https://www.docker.com/`
- Reuses an existing matching tab when possible
- Reuses the user's existing browser session
- Verifies the destination
- Stops safely if authentication is required
- Never handles credentials

## Example triggers

- Open Docker
- Take me to Docker
- Go to Docker

## Installation

Place the `open-docker` folder under your agent's skills directory:

```text
skills/
└── open-docker/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave browser automation.

## Privacy

This skill does not request or store passwords, API keys, authentication codes, or other credentials.
