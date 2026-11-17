## Description:

Build, extend, debug, scaffold, and package Discord bots and bot systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypjo](https://clawhub.ai/user/hypjo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, extend, debug, scaffold, and package Discord bots, dashboards, APIs, ticket systems, moderation tools, persistence layers, worker queues, and deployment assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled dashboard and moderation examples can expose or alter moderation data without authentication if deployed as-is.

Mitigation: Treat these examples as development starters and add authentication, guild-level authorization, restricted CORS, strong session secrets, secure cookies, and dependency lockfiles before exposing them to users or the internet.

Risk: Ticket transcripts and dashboard records can contain sensitive Discord server or user data.

Mitigation: Define transcript retention, access, and deletion rules before using transcript or moderation storage features in production.

## Reference(s):

- [Discord Bot Planning](references/discord-bot-planning.md)
- [discord.js Patterns](references/discord-js-patterns.md)
- [discord.py Patterns](references/discord-py-patterns.md)
- [Dashboard and API Patterns](references/dashboard-api-patterns.md)
- [Discord OAuth Dashboard Patterns](references/oauth-dashboard-patterns.md)
- [CSRF and Session Persistence Patterns](references/csrf-session-patterns.md)
- [Ticket System Patterns](references/ticket-system-patterns.md)
- [Deployment Patterns](references/deployment-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/hypjo/skills/hypdiscordgod)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, shell commands, configuration snippets, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify an existing repository or scaffold bundled starter files for Discord bot, API, dashboard, worker, persistence, and deployment workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
