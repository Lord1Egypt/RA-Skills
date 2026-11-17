## Description:

Google Forms API integration with managed OAuth. Create forms, inspect structure, review responses, change publishing settings, and manage response notification watches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Google Forms through ClawLink, then create forms, inspect form structure, review responses, adjust publishing settings, and manage response watches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects a user's Google account through ClawLink and can access Google Forms data.

Mitigation: Use it only when the user trusts the ClawLink plugin and hosted OAuth service, and keep access scoped to the connected Google account.

Risk: The available tools can modify forms, publishing settings, watches, questions, and responses.

Mitigation: Preview and confirm the target resource and intended effect before any create, update, or delete operation.

Risk: A missing or stale Google Forms connection can lead to failed or unavailable tool calls.

Mitigation: Verify the connection with ClawLink integration and tool-list checks before relying on Google Forms tools.

## Reference(s):

- [Google Forms API Overview](https://developers.google.com/forms/api)
- [Forms Resource](https://developers.google.com/forms/api/reference/rest/v1/forms)
- [Responses Reference](https://developers.google.com/forms/api/reference/rest/v1/forms.responses)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-forms-surveys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated Google Forms read and write operations through ClawLink; write actions require explicit user confirmation.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
