## Description:

Lynse CLI lets agents call Lynse.ai APIs to query account information, manage files, transcripts, summaries, devices, AI models, teams, and send messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johneyzhao-lynse](https://clawhub.ai/user/johneyzhao-lynse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an assistant to Lynse.ai account and workspace workflows, including account lookup, file transcription and summary management, device and team administration, AI model management, and outbound messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Lynse API key for powerful account, file, device, AI model, team, and message-sending actions.

Mitigation: Install only in a private, trusted agent environment with a least-privileged Lynse API key and require explicit confirmation before delete, unbind, team-management, or message-sending actions.

Risk: A misconfigured API host could route credentials or actions to an unintended endpoint.

Mitigation: Set LYNSE_API_HOST only to the legitimate HTTPS Lynse endpoint before use.

Risk: Private account data such as phone numbers, points, files, transcripts, and summaries may be exposed in shared contexts.

Mitigation: Configure owner binding where available and redact sensitive fields unless the user explicitly requests them in a private context.

## Reference(s):

- [Lynse homepage](https://www.lynse.ai)
- [Lynse CLI compatibility table](artifact/compatibility.md)
- [ClawHub skill listing](https://clawhub.ai/johneyzhao-lynse/skills/lynse-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LYNSE_API_HOST and LYNSE_API_KEY; uses curl and bash.]

## Skill Version(s):

1.2.3 (source: server release evidence; artifact frontmatter lists 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
