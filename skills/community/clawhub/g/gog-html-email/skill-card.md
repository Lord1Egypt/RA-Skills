## Description:

Send beautifully formatted HTML emails via gog CLI with templates and styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syedair](https://clawhub.ai/user/syedair)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to select prebuilt HTML email templates, fill placeholders, and send formatted Gmail messages through the gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emails could be sent to unintended recipients or with unintended content.

Mitigation: Require explicit user approval for recipients, subject, and final body before sending through gog.

Risk: Generated HTML may contain unsafe or malformed content.

Mitigation: Preview the final HTML before sending and avoid untrusted template values.

Risk: Shell substitution can break or alter output when placeholder values contain special characters.

Mitigation: Prefer a renderer that escapes HTML and passes arguments safely instead of interpolating values into sed commands.

## Reference(s):

- [gog CLI homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/syedair/skills/gog-html-email)
- [Publisher profile](https://clawhub.ai/user/syedair)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and HTML template content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and Gmail sending capability; templates use bracketed placeholders for recipient-specific content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
