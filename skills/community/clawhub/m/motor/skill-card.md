## Description:

Motor specification and selection tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to run a command-line helper for recording, listing, searching, exporting, and configuring local motor-related entries. Server security evidence notes that the artifact behaves as a generic local data store rather than performing substantive motor selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact does not perform the motor-selection task it claims and may mislead users about its capabilities.

Mitigation: Confirm the intended motor-selection behavior before deployment and treat current command output as local record management only.

Risk: The shell script writes persistent local files and can delete or overwrite its own data and export files.

Mitigation: Run only in a contained environment with a dedicated MOTOR_DIR and review file-changing commands before use.

Risk: Server security guidance reports an unsafe config command and command-injection risk.

Mitigation: Fix shell input handling and validate configuration keys and values before enabling the skill for shared or production use.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/motor)
- [Publisher profile](https://clawhub.ai/user/bytesagain1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output and JSONL/CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MOTOR_DIR when set and otherwise writes persistent data under ~/.motor/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
