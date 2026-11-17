## Description:

Atomic node skill to send an existing Gmail draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill when an agent needs to send a preexisting Gmail draft by draft ID through the gog CLI and return confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Gmail drafts immediately and the security evidence notes no built-in recipient, subject, content preview, or explicit confirmation requirement.

Mitigation: Use only in workflows that verify the draft ID, recipients, subject, and content and require clear user approval before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/gmail-draft-send)

## Skill Output:

**Output Type(s):** [shell commands, json]

**Output Format:** [Shell command followed by JSON confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gog; retries failed or invalid attempts up to three times.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
