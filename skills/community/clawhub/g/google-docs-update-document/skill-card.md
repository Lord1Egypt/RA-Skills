## Description:

Atomic node skill to update a Google Doc using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to write, insert, or replace text in an existing Google Doc through the gog command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently change Google Docs content.

Mitigation: Confirm the exact document ID and intended edit before running the gog command.

Risk: Raw shell command construction can mishandle document text or replacement strings.

Mitigation: Prefer structured argument execution or stdin/file input instead of interpolating untrusted document text into a shell command.

Risk: Google Docs credentials may grant access beyond the intended document.

Mitigation: Use only trusted gog credentials with the minimum access needed for the target document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-docs-update-document)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [JSON object or confirmation string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and trusted Google Docs credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
