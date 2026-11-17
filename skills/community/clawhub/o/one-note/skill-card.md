## Description:

Helps agents access and organize OneNote notebooks, sections, and pages through a user-authorized Microsoft Graph connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to find, create, and organize OneNote notebooks, sections, and pages with their authorized account. It also documents optional automations for connected services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting OneNote grants access within the user's authorized account.

Mitigation: Authorize only if comfortable with the requested access; prefer read and list actions, and confirm each write.

Risk: Optional functions, triggers, and destinations can run persistently or forward event data.

Mitigation: Review each function, trigger, and destination before approving it.

## Reference(s):

- [ClawHub Microsoft OneNote skill](https://clawhub.ai/byungkyu/skills/one-note)
- [Maton homepage](https://maton.ai)
- [OneNote REST API reference](https://learn.microsoft.com/en-us/graph/api/resources/onenote-api-overview)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton API reference](https://docs.maton.ai/api-reference/overview)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OneNote access requires an authorized connection; writes require user confirmation.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
