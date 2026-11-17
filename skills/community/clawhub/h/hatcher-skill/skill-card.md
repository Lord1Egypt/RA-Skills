## Description:

Deploy and control AI agents on Hatcher, a managed hosting platform for OpenClaw, Hermes, ElizaOS, and Milady agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hatcherlabs](https://clawhub.ai/user/hatcherlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to register Hatcher accounts, create hosted agents, manage lifecycle state, configure integrations, and choose payment or tier options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide creation and operation of live Hatcher agents, including starts, restarts, stops, and deletion.

Mitigation: Require explicit human confirmation before lifecycle actions, especially deletion; use stop instead of delete when state should be preserved.

Risk: The skill handles long-lived API keys and integration tokens for Hatcher and connected services.

Mitigation: Use dedicated least-privilege accounts and tokens, avoid exposing secrets in logged shell commands, store credentials securely, and rotate any exposed keys.

Risk: The skill includes payment and tier-change workflows that can spend credits or external funds.

Mitigation: Require explicit human confirmation before purchases, upgrades, addons, wallet transactions, or hosted checkout flows.

Risk: Installing third-party skills or plugins can change a hosted agent's behavior and access.

Mitigation: Review every third-party skill or plugin before installation and install only what the target agent needs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hatcherlabs/skills/hatcher-skill)
- [Hatcher Homepage](https://hatcher.host)
- [Hatcher Skill Entry Point](https://hatcher.host/skill.md)
- [Hatcher Auth Guide](https://hatcher.host/skill/auth.md)
- [Hatcher Agents Guide](https://hatcher.host/skill/agents.md)
- [Hatcher Pricing Guide](https://hatcher.host/skill/pricing.md)
- [Hatcher Integrations Guide](https://hatcher.host/skill/integrations.md)
- [Hatcher OpenAPI Specification](https://api.hatcher.host/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples and JSON request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint instructions, lifecycle guidance, integration setup, and payment workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
