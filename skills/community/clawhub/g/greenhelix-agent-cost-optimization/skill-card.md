## Description:

A practical cookbook for reducing AI agent operational costs through LLM cost analysis, prompt caching, model routing, token optimization, observability cost control, outcome-based metering, and infrastructure right-sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and FinOps practitioners use this guide to identify and reduce AI agent operating costs across inference, routing, telemetry, storage, batching, and infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide declares a WALLET_ADDRESS environment value that may be unnecessary for some users.

Mitigation: Provide a wallet address only when the platform clearly requires it, and use a public wallet address only.

Risk: A batch API example writes a timestamp-named file under /tmp if copied into real code.

Mitigation: Replace the sample path with secure temporary-file handling and cleanup before production use.

Risk: The guide includes illustrative Python examples that users may adapt for real agent fleets.

Mitigation: Review, test, and scan adapted code before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-cost-optimization)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [Publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python examples and inline command/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide content; examples require user review before use in production.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
