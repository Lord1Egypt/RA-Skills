## Description:

Reliable webhook infrastructure for AI agents that helps receive webhooks from Stripe, GitHub, Slack, Shopify, and Vercel with signature verification, durable queuing, and automatic retries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linyiru](https://clawhub.ai/user/linyiru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure hookpipe CLI workflows that route external service webhooks into an agent gateway with durable buffering, retries, provider discovery, and event streaming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external hookpipe CLI package.

Mitigation: Review package provenance before installing and prefer a pinned, verified release when available.

Risk: Example commands place webhook secrets and API tokens directly in shell command arguments.

Mitigation: Use a secret manager, protected file, or interactive prompt where supported instead of exposing real secrets in shell history or process listings.

Risk: Broad provider or event filters can route unintended webhook events to an agent.

Mitigation: Keep provider and event filters narrow so only intended webhook events reach the agent.

## Reference(s):

- [hookpipe GitHub](https://github.com/hookpipe/hookpipe)
- [Provider Design Guide](https://github.com/hookpipe/hookpipe/blob/main/packages/providers/DESIGN.md)
- [Publisher profile](https://clawhub.ai/user/linyiru)
- [ClawHub skill page](https://clawhub.ai/linyiru/skills/hookpipe)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-output CLI options for provider discovery, event streaming, health checks, and dry-run validation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
