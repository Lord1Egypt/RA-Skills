## Description:

Milestone Execution helps an agent split large tasks into staged milestones, pause after each milestone for user confirmation, and report progress before continuing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siesta-0402](https://clawhub.ai/user/siesta-0402)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage complex, multi-step coding or review work as milestones that pause for confirmation, recovery, retry, skip, rollback, or modification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the core milestone-executor implementation is missing and that documented commands may invoke an unverified executable from the environment.

Mitigation: Install or use the skill only after the package includes the reviewed milestone-executor implementation and invokes it through a package-relative path.

Risk: The skill manages continuation, rollback, recovery, and possible parallel work through local state.

Mitigation: Review the .milestone-state.json behavior and require explicit user confirmation before continuing, rolling back, recovering, or starting parallel work sessions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown progress reports with inline shell commands and JSON state descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local .milestone-state.json file to track task progress when the executor is available.]

## Skill Version(s):

3.0.1 (source: server release metadata; artifact frontmatter and README state 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
