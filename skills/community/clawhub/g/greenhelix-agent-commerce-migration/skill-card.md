## Description:

Guides developers through retrofitting existing REST APIs with agent commerce capabilities, including x402 payment headers, GreenHelix escrow integration, authentication bridging, migration validation, rollback planning, and performance comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API platform teams use this guide to plan a gradual migration from human-oriented REST endpoints to agent-ready commerce endpoints. It helps them assess readiness, add payment and identity layers, validate behavior, plan rollback, and compare performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shadow traffic and baseline recorder examples may expose credentials or sensitive API data if copied directly into production.

Mitigation: Use strict header allowlists, redact request and response bodies, restrict destination hosts, and keep raw production captures out of version control.

Risk: Non-idempotent request examples can cause unintended side effects when replayed or shadowed.

Mitigation: Require dry-run controls or explicit allowlists before replaying write operations.

Risk: Authenticated agent access depends on identity verification behavior that the security guidance says must be fixed before reliance.

Mitigation: Review and correct identity verification to fail closed before enabling authenticated agent commerce paths.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mirni/skills/greenhelix-agent-commerce-migration)
- [GreenHelix platform documentation](https://docs.greenhelix.net)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [x402 specification](https://www.x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with API migration patterns, code examples, configuration snippets, validation steps, rollback guidance, and performance comparison notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable educational guide; references GREENHELIX_API_KEY and AGENT_SIGNING_KEY as user-supplied credentials.]

## Skill Version(s):

1.3.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
