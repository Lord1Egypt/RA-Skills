## Description:

Set up or audit an OpenClaw agent workspace with standardized governance files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[u0003-yxuan](https://clawhub.ai/user/u0003-yxuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up a new OpenClaw agent workspace or audit an existing workspace for required governance, memory, and daily log files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the skill can create or update persistent governance and memory files in an existing OpenClaw workspace.

Mitigation: Review proposed AGENTS.md and MEMORY.md changes before applying them, and keep a backup of existing workspace files.

Risk: The inspected artifact references template files that were not included in the artifact.

Mitigation: Verify that the expected references/ templates are present and correct before using the skill to generate workspace files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell command examples, file paths, and audit status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or verify persistent governance and memory files in an OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
