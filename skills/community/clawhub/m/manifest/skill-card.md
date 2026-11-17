## Description:

Manifest is an OpenClaw plugin that helps route LLM requests to cost-effective models and provides cost, token, and health monitoring tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Manifest to configure OpenClaw request routing, local or cloud monitoring, and in-conversation usage, cost, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud mode can create a trust boundary around prompts, responses, metadata, costs, tokens, and API-key handling.

Mitigation: Prefer local mode for sensitive workloads unless Manifest privacy, security, retention, and key-rotation practices have been reviewed.

Risk: Request routing can affect model choice, cost, latency, and response behavior across supported providers.

Mitigation: Review routing configuration, provider access, spending limits, and monitoring results before using the plugin in production workflows.

## Reference(s):

- [Manifest OpenClaw plugin homepage](https://github.com/mnfst/manifest)
- [Manifest ClawHub skill page](https://clawhub.ai/seanford/skills/manifest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local or cloud setup guidance, OpenClaw plugin commands, environment variable references, and monitoring tool descriptions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
