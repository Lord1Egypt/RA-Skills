## Description:

Atomic node skill to update the subject of an existing Gmail draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when they need to set or update the subject line on an existing Gmail draft through the native Gmail CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted draft IDs or subject text could be used unsafely when constructing the Gmail CLI invocation.

Mitigation: Invoke `gog` with separated arguments or validated inputs, and avoid concatenating an executable shell command string from user-controlled values.

Risk: The command may fail or update the wrong value if parameters are malformed or hallucinated.

Mitigation: Check the JSON response to confirm the subject was updated, retry only with corrected parameters, and stop after the documented retry limit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/gmail-draft-update-subject)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [JSON confirmation and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `gog` binary and should validate JSON responses before confirming completion.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-04-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
