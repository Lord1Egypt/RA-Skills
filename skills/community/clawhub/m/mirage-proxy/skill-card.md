## Description:

Install and configure mirage-proxy as a transparent PII/secrets filter for OpenClaw LLM API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chandika](https://clawhub.ai/user/chandika)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install a local mirage-proxy service and configure OpenClaw providers to route model traffic through it for PII and secrets filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes LLM prompts, responses, and provider authorization traffic through a local downloaded proxy.

Mitigation: Install only when the publisher and mirage-proxy upstream are trusted, and prefer running the proxy in an isolated container.

Risk: The installer can fall back to building from the upstream Git repository if the downloaded binary does not run.

Mitigation: Avoid the unpinned cargo fallback unless the source and revision have been reviewed and pinned by the operator.

Risk: The setup can create restart persistence and leaves provider configuration for manual cleanup on uninstall.

Mitigation: Enable restart persistence only when needed and remove the OpenClaw provider configuration manually during uninstall.

## Reference(s):

- [Mirage Proxy ClawHub Skill](https://clawhub.ai/chandika/skills/mirage-proxy)
- [mirage-proxy GitHub Repository](https://github.com/chandika/mirage-proxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON5, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, verification, uninstall, provider-routing, and persistence guidance for OpenClaw.]

## Skill Version(s):

0.5.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
