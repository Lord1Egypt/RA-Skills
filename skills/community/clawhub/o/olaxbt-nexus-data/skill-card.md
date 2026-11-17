## Description:

Access OlaXBT Nexus cryptocurrency data APIs for market data, news, KOL tracking, technical indicators, and trading insights using a wallet-linked JWT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olaxbt-dev](https://clawhub.ai/user/olaxbt-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to connect OpenClaw agents to OlaXBT Nexus crypto market, news, sentiment, KOL, technical indicator, smart money, and trading insight data using a pre-obtained JWT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged suspicious because it contains private-key signing code that is under-disclosed relative to the JWT-only user flow.

Mitigation: Use the documented JWT-only path, do not provide wallet private keys to the package, and avoid NexusAuth unless the publisher clarifies and documents that path.

Risk: A JWT bearer token can spend credits or access account-scoped API data.

Mitigation: Keep NEXUS_JWT out of logs and shared configuration, scope access to trusted runtime environments, and rotate or revoke the token if exposure is suspected.

Risk: Configurable auth and data endpoints can receive JWTs if NEXUS_AUTH_URL or NEXUS_DATA_URL is changed.

Mitigation: Leave endpoint overrides unset in production and only override them in trusted test environments.

Risk: The security verdict requires review before deployment.

Mitigation: Install only when the publisher is trusted, review the release evidence, and keep configuration locked down before using the skill with live account credentials.

## Reference(s):

- [OlaXBT Nexus Data ClawHub listing](https://clawhub.ai/olaxbt-dev/skills/olaxbt-nexus-data)
- [Nexus API auth flow](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md)
- [OlaXBT Nexus Data repository](https://github.com/olaxbt/olaxbt-nexus-data)
- [OlaXBT skill documentation](https://olaxbt.xyz/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Python snippets, shell commands, and structured API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXUS_JWT and may use optional NEXUS_AUTH_URL or NEXUS_DATA_URL overrides.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence, released 2026-03-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
