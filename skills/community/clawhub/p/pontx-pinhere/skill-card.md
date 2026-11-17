## Description:

Integrate Pinhere safely through Pontx for private issue collaboration, browser-extension capture, project setup, Webhooks, PATs, OAuth, and explicitly approved state changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Pinhere through Pontx while preserving privacy boundaries, resolving live API details, and requiring explicit approval before persistent or security-sensitive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pinhere workflows may expose private project data, issue content, DOM context, screenshots, token metadata, Webhook diagnostics, PATs, OAuth values, or one-time secrets.

Mitigation: Fetch and return only the minimum needed data, keep credentials in caller-owned secret storage, and avoid sending sensitive values or screenshots to logs, analytics, support tickets, chat, or Hub.

Risk: State-changing requests, token actions, and Webhook actions can persist changes or affect security-sensitive resources.

Mitigation: Preview the exact target, method, path, redacted input, and expected effect, then require explicit approval before executing the unchanged request.

Risk: Ambiguous issue, project, credential, or Webhook targets can cause the agent to act on the wrong resource.

Mitigation: Read the active project, Origin, and resource identity first, and stop for user selection when names or targets are ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-pinhere)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill emphasizes redacted previews, explicit approval for state changes, and minimal disclosure of sensitive Pinhere data.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
