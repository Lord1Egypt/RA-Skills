## Description:

Atomic node skill to create a Google Doc using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill when they need to create a new Google Doc through the gog CLI and receive the created document details as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command template can turn a document title into unsafe shell input if followed literally.

Mitigation: Pass the document title as a literal gog argument, avoid untrusted or unusual titles, and review the skill before installing or using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-docs-create-document)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown guidance with an inline shell command; the invoked command returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI binary and access to create Google Docs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
