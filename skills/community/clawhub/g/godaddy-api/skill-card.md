## Description:

Work with GoDaddy's gddy CLI, public Domains MCP, REST and GraphQL APIs, domains and DNS, Commerce, Hosting, Email, experimental Platform apps, and Agent Name Service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarx56](https://clawhub.ai/user/solarx56)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover current GoDaddy CLI, MCP, REST, and GraphQL workflows, then plan and verify domain, DNS, hosting, email, platform, and account-related actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that change real GoDaddy resources or incur charges.

Mitigation: Require the agent to show the exact target, effect, cost, and rollback or verification plan, then obtain explicit approval before any purchase, DNS edit, hosting change, email provisioning, or API mutation.

Risk: CLI installation or updates could execute untrusted or mutable code if source and integrity are not checked.

Mitigation: Use the versioned official gddy release with SHA-256 verification; review any optional npx agent installer package and version before running it with normal user privileges.

Risk: Credentials or debug output could expose OAuth tokens, PATs, or request details.

Mitigation: Use browser OAuth or scoped PAT storage, avoid pasting tokens into chat, and avoid debug output around secrets unless necessary.

Risk: DNS mutations can duplicate records, replace existing values, or leave partial state after a failure.

Mitigation: Read current records, preserve rollback data, use dry-run where supported, obtain approval for the concrete plan, execute once, and verify with a fresh read.

Risk: Retries for billed or asynchronous operations can duplicate purchases or other account-impacting work.

Mitigation: Poll returned operation IDs and inspect account or resource state before deciding whether another call is safe.

## Reference(s):

- [GoDaddy API Skill on ClawHub](https://clawhub.ai/solarx56/skills/godaddy-api)
- [GoDaddy CLI, MCP, and agent platform](references/agent-platform.md)
- [Dynamic API catalog](references/api-catalog.md)
- [Mutation safety](references/safety.md)
- [Errors, retries, and limits](references/errors-and-limits.md)
- [GoDaddy CLI](https://github.com/godaddy/cli)
- [GoDaddy CLI v0.2.12 release](https://github.com/godaddy/cli/releases/tag/v0.2.12)
- [GoDaddy Domains MCP](https://developer.godaddy.com/en/docs/api-users/mcp)
- [GoDaddy Domains v3 OpenAPI](https://developer.godaddy.com/openapi/domains-v3.json)
- [GoDaddy Domains v2 OpenAPI](https://developer.godaddy.com/openapi/domains-v2.json)
- [GoDaddy Domains v1 OpenAPI](https://developer.godaddy.com/openapi/domains-v1.json)
- [GoDaddy API rate limits](https://developer.godaddy.com/en/docs/api-users/rate-limits)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes approval, verification, retry, and credential-handling guidance for GoDaddy workflows.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
