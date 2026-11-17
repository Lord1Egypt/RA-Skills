## Description:

Confidential RWA portfolio agent on Fhenix CoFHE that reads encrypted balances, stages buy and yield-claim intents, and requires human confirmation before state-changing actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hastodev](https://clawhub.ai/user/hastodev)

### License/Terms of Use:

MIT

## Use Case:

External MuHaven users and agents use this skill to inspect encrypted real-world-asset portfolio data, review yields and audit context, and prepare buy, claim, or pause intents for separate user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account JWTs and financial intents while some runtime protections may be advisory in host-native deployments.

Mitigation: Install only if you trust MuHaven, keep backend_url, dashboard_url, and broker_endpoint at expected values, and prefer a runtime that enforces the declared network allowlist.

Risk: Misconfigured broker or account session could affect financial-intent handling.

Mitigation: Verify the broker daemon and account session are yours before use; enable read-only mode when portfolio viewing is sufficient.

## Reference(s):

- [MuHaven homepage](https://muhaven.app)
- [ClawHub skill page](https://clawhub.ai/hastodev/skills/muhaven-rwa-skill)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Structured MCP tool responses and human-readable text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing actions are returned as staged intents for external confirmation; the skill does not auto-submit them.]

## Skill Version(s):

0.1.4 (source: frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
