## Description:

Mac laptop clamshell mode assistant that supports running with the lid closed without an external display, keyboard, or mouse, auto-detects Mac model and macOS version, and provides configuration with rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keenlycat](https://clawhub.ai/user/keenlycat)

### License/Terms of Use:

MIT

## Use Case:

External Mac users and developers use this skill to check compatibility, choose a clamshell or headless mode, and run or review shell commands that adjust macOS power settings for lid-closed background work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask users to run administrator-level commands that change system-wide Mac sleep behavior.

Mitigation: Review commands before execution, keep the Mac connected to power for headless operation, and verify power settings before and after changes.

Risk: Server security guidance says the rollback and safety claims are misleading because rollback is not a true backup restore and some documented safety options are not implemented.

Mitigation: Treat rollback output as manual reset guidance rather than full restoration, and confirm the resulting pmset settings after using restore options.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that may require administrator privileges when applied.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
