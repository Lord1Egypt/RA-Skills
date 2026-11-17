## Description:

Audits an app's App Store discoverability with MetaRun across keyword rankings, listing metadata, Apple search analytics, competitors, and AI assistant visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iderasyh](https://clawhub.ai/user/iderasyh)

### License/Terms of Use:

MIT-0

## Use Case:

App developers and marketers use this skill to identify App Store search opportunities, assess listing quality and competitor changes, and understand whether AI assistants recommend their app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned MetaRun CLI invocation could run an unexpected version.

Mitigation: Avoid unpinned CLI examples in highly privileged environments; review the version before execution.

Risk: MetaRun or Apple account credentials could grant access beyond the audit's needs.

Mitigation: Use least-privilege credentials and keep access tokens private.

Risk: Answer-engine scans may incur plan usage, and monitoring or promotional scheduling can continue or make changes beyond the audit.

Mitigation: Confirm metered scans, background monitoring, and any promotional scheduling or write operation with the user first.

## Reference(s):

- [MetaRun for agents](https://metarun.dev/agents)
- [MetaRun: aso audit on ClawHub](https://clawhub.ai/iderasyh/skills/metarun-aso-audit)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [One-page Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized findings and proposed metadata changes; writes require preview and user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
