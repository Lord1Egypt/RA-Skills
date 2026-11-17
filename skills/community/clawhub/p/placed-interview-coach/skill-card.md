## Description:

Placed Interview Coach helps users practice technical, system design, and behavioral interviews through the Placed career platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run mock technical, system design, and behavioral interview practice with Placed, including question generation, answer feedback, STAR story preparation, and session review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist the user's Placed API key in a plaintext shell credentials file.

Mitigation: Set PLACED_API_KEY through the environment or a secret manager; if a local credentials file is used, restrict file permissions and use only on a trusted machine.

Risk: Interview materials and answers may be sent to the external Placed API.

Mitigation: Avoid submitting sensitive resumes, proprietary interview content, or confidential personal information unless the user accepts the service's handling of that data.

## Reference(s):

- [Placed Homepage](https://placed.exidian.tech)
- [Placed API Key Settings](https://placed.exidian.tech/settings/api)
- [Placed Interview Coach API Reference](artifact/references/api-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/ajitsingh25/skills/placed-interview-coach)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Placed API key; responses may include interview questions, feedback, story-bank entries, and session identifiers.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
