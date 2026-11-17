## Description:

Browse and extract content from webpages using a local browser service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingagi](https://clawhub.ai/user/pingagi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to open webpages and retrieve useful page content, including titles, text, partial HTML, and optional screenshot data through a local browser service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve text, HTML, and screenshot data from requested URLs, which may expose private, internal, authenticated, or sensitive page content if used on inappropriate targets.

Mitigation: Use only with URLs intended for agent inspection; avoid private, internal, authenticated, or sensitive URLs unless the local browser service is explicitly trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pingagi/skills/pingagi-web)

## Skill Output:

**Output Type(s):** [Text, HTML, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with an inline curl command; browser service responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned JSON can include page title, page text, partial HTML, and optional base64 screenshot data.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata and artifact skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
