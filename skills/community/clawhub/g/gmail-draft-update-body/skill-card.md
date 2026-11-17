## Description:

Atomic node skill to update the body text of an existing Gmail draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when an existing Gmail draft's body text needs to be replaced or updated through the native Gmail CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dynamic draft IDs or body text can be interpreted as shell syntax if passed through a command string.

Mitigation: Use shell-free argument passing for gog, validate draft IDs, and avoid untrusted draft content unless literal argument handling is guaranteed.

Risk: The skill edits an existing Gmail draft and may overwrite the intended body if the wrong draft ID is supplied.

Mitigation: Confirm the target draft ID before execution and verify that the JSON response shows the expected draft update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/gmail-draft-update-body)

## Skill Output:

**Output Type(s):** [Shell commands, JSON]

**Output Format:** [JSON confirmation from the Gmail CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and retries up to 3 times when the update is not confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
