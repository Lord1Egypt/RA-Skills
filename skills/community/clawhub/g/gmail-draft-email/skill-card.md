## Description:

Atomic node skill to draft an email via Gmail using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and operators use this skill to prepare Gmail draft messages for review without sending them. It is suited to workflows where an agent should create a draft email through the gog CLI and report whether draft creation succeeded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-based execution of generated Gmail draft commands could mishandle attacker-controlled recipient, subject, or body values.

Mitigation: Invoke gog with separate argv arguments, validate recipient addresses, treat subject and body as opaque data, and review generated commands before execution.

Risk: Blind retries after uncertain command results could create duplicate Gmail drafts.

Mitigation: Verify draft creation responses and existing drafts before retrying; stop and report uncertainty when confirmation is ambiguous.

## Reference(s):

- [Gmail Draft Email on ClawHub](https://clawhub.ai/zvirb/skills/gmail-draft-email)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown guidance with inline shell command and JSON confirmation expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and Gmail access; the workflow retries draft creation up to three times before reporting failure.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
