## Description:

Use for PostHog project-token runtime capture, event batching, and remote feature-flag evaluation with caller-owned tokens, local previews, and explicit confirmation before any provider request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare and review local PostHog event capture, event batching, and feature-flag evaluation workflows before sending provider requests with caller-owned project tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed capture or feature-flag calls may send event, person, group, or evaluation data to PostHog and may affect usage quota.

Mitigation: Review the local preview, destination, data scope, and quota impact before giving explicit confirmation for any provider request.

Risk: Project tokens could be exposed if pasted into source, logs, chat, terminal history, or hosted services.

Mitigation: Keep project tokens in local environment variables or local client options and avoid including them in examples, logs, or shared text.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and code-oriented workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes local previews and explicit confirmation before provider requests.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
