## Description:

Interact with the Maestro API to create tasks, list tasks, and send room messages using the configured OpenClaw Maestro connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohammadsheikhian](https://clawhub.ai/user/mohammadsheikhian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate a configured Maestro connection from an agent, including creating tasks, listing tasks, and sending room messages without exposing configured credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Maestro credentials can authorize task creation, task listing, and room messages through the connected Maestro account.

Mitigation: Install only with a trusted Maestro connection, validate channels.omadeus configuration before requests, and never expose or hardcode baseUrl, apiKey, or openClawMemberId.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohammadsheikhian/skills/omadeus)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Concise text or Markdown summaries with Maestro API actions performed when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or list Maestro tasks and send room messages through configured OpenClaw Maestro credentials; does not expose raw credential values.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
