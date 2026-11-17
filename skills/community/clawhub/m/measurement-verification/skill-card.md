## Description:

Maintains a measurement and verification system for Shelby-style workflows, including three evaluation criteria, consistency checks, drift defenses, and extension guidance for synchronized keywords and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hechunxian](https://clawhub.ai/user/hechunxian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to preserve measurement criteria, run or interpret consistency checks, identify drift, and migrate the verification setup across local WorkBuddy-style environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references local WorkBuddy paths, maintenance files, and daily logs that may not exist or may differ in another environment.

Mitigation: Confirm the local paths and review RULES, MAINTENANCE, CAPABILITY, TODO, USER, and daily logs before running the suggested scripts or recreating automation.

Risk: Consistency checks can give misleading confidence if path or format assumptions drift.

Mitigation: Review check output for attempted paths, candidate counts, and actual matched formats, then rerun checks until the reported state is clear.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local WorkBuddy paths and maintenance files that must exist in the target environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
