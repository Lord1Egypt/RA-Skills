## Description:

Inspect environment variables, critical directories, and write permissions, then produce a health report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment engineers use this skill to check required environment variables, critical directories, and write access before running an application or validating a local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filesystem write checks can overwrite or delete files in user-supplied directories without adequate safeguards.

Mitigation: Use the skill only on directories where temporary probe-file creation and deletion is acceptable, and avoid sensitive or shared paths.

Risk: The output report path can be overwritten.

Mitigation: Choose a report path that can be safely replaced, or review the target path before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neo1307/skills/neo1307-env-health-check)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report file plus JSON console summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports OK, WARN, and FAIL findings for requested environment variables and directories.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
