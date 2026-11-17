## Description:

Atomic node skill to delete a file in Google Drive using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user needs a specified Google Drive file moved to trash through the configured gog CLI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move a Google Drive file to trash through the permissions of the configured gog account.

Mitigation: Run it only after the user provides or confirms the exact Google Drive file ID and understands the effect.

Risk: The artifact does not include target-verification or explicit confirmation instructions before deletion.

Mitigation: Add an operator review step around the command in workflows that use this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-drive-delete-file)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a gog drive delete command and expects confirmation that the file was moved to trash.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
