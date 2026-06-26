## Description: <br>
Build, extend, debug, scaffold, and package Discord bots and bot systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hypjo](https://clawhub.ai/user/hypjo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, extend, troubleshoot, and package Discord bot projects, including slash commands, moderation, ticketing, persistence, deployment, dashboards, OAuth flows, and worker queues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ticket and dashboard starters may need privacy and production-hardening review before deployment. <br>
Mitigation: Review generated code before deployment and add authentication, authorization, restrictive CORS, HTTPS, secure cookies, CSRF checks, and transcript or session retention controls before public exposure. <br>
Risk: Discord bot, OAuth, and webhook projects can expose tokens, secrets, or excessive permissions if configured carelessly. <br>
Mitigation: Keep tokens and OAuth secrets out of source control, use least-privilege Discord permissions, and run scaffolds in a fresh directory for review. <br>


## Reference(s): <br>
- [Discord Bot Planning](references/discord-bot-planning.md) <br>
- [discord.js Patterns](references/discord-js-patterns.md) <br>
- [discord.py Patterns](references/discord-py-patterns.md) <br>
- [Persistence Patterns](references/persistence-patterns.md) <br>
- [Postgres, Prisma, and Drizzle Patterns](references/postgres-prisma-drizzle-patterns.md) <br>
- [Deployment Patterns](references/deployment-patterns.md) <br>
- [Dashboard and API Patterns](references/dashboard-api-patterns.md) <br>
- [Discord OAuth Dashboard Patterns](references/oauth-dashboard-patterns.md) <br>
- [CSRF and Session Persistence Patterns](references/csrf-session-patterns.md) <br>
- [Webhook Integration Patterns](references/webhook-patterns.md) <br>
- [Worker and Queue Patterns](references/worker-queue-patterns.md) <br>
- [Moderation Dashboard Patterns](references/moderation-dashboard-patterns.md) <br>
- [Mono-repo Starter Patterns](references/monorepo-starter-patterns.md) <br>
- [Ticket System Patterns](references/ticket-system-patterns.md) <br>
- [Ticket Advanced Patterns](references/ticket-advanced-patterns.md) <br>
- [Ticket Bot Starter Notes](references/ticket-bot-starter-notes.md) <br>
- [Discord Bot Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration notes, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May scaffold Discord bot, API, dashboard, worker, persistence, and deployment files from bundled templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
