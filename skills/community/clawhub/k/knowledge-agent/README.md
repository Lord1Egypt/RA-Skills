# knowledge-agent

Turn your domain expertise into a 24/7 AI consulting agent on OpenClaw. Clients interact in Feishu groups — your Agent answers accurately, safely, and around the clock.

## What This Solves

You have professional knowledge but limited time. Clients keep asking the same questions. You can't be online 24/7. This skill packages your expertise into an OpenClaw Agent that:
- Answers client questions based on YOUR knowledge, not hallucinations
- Operates 24/7 in Feishu groups without needing to be @mentioned
- Has safety constraints that prevent information leaks or identity exposure
- Can search for real-time information to supplement static knowledge

## What's Included

```
knowledge-agent/
├── SKILL.md                           # Entry point — 6-step interactive workflow
├── references/
│   ├── knowledge-layers.md            # Three-layer architecture (AGENTS.md / MEMORY.md / knowledge/)
│   ├── safety-constraints.md          # Security settings for paid consulting
│   ├── anti-hallucination.md          # Quality controls — "don't fabricate" enforcement
│   ├── feishu-delivery.md             # Feishu group setup + no-@ reply config
│   └── example-douyin.md              # Complete example: Douyin operations consultant
├── templates/
│   ├── AGENTS.template.md             # AGENTS.md skeleton with all required sections
│   ├── SOUL.template.md               # Personality and principles template
│   ├── IDENTITY.template.md           # Agent display name and public image
│   └── MEMORY.template.md             # Long-term memory structure
└── scripts/
    └── setup-consultant.sh            # Creates workspace with template files
```

## Quick Start

1. Install the skill on your OpenClaw instance
2. Tell your main Agent: "Help me build a consulting Agent for [YOUR DOMAIN]"
3. Follow the 6-step interactive workflow — the Agent guides you through everything
4. Share your knowledge materials when prompted
5. Review and confirm the generated configuration files
6. Set up a Feishu group, invite clients, start serving

## Key Principles

- **Independent workspace per agent** — never share workspace with other agents, or they read the same AGENTS.md
- **Deterministic loading > hoping Agent reads it** — critical knowledge goes in AGENTS.md
- **Safety constraints in AGENTS.md, not MEMORY.md** — because MEMORY.md doesn't load in group chats
- **Search capability + knowledge base** — Agent can verify with real-time search, not just static docs
- **Domain-agnostic** — works for any field with a structured knowledge base

## Who This Is For

- Professionals with domain expertise who want to scale their consulting
- Anyone running paid knowledge services through Feishu groups
- OpenClaw users who want to create a client-facing Agent with proper safety

## Author

[@simonlin1212](https://clawhub.ai/simonlin1212) — Based on production experience running paid consulting Agents (2026-04)
