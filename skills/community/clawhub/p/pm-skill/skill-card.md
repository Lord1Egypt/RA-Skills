## Description:

PM Skill helps an agent act as a product manager and technical architect to scaffold and write structured PRDs with acceptance criteria and testing strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leio9511](https://clawhub.ai/user/leio9511)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to convert a discussed feature request into a structured PRD, including problem statement, architecture notes, BDD acceptance criteria, and testing strategy. It is intended for OpenClaw-style SDLC workflows that use PRDs as planner input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local helper scripts and writes under OpenClaw workspace paths.

Mitigation: Install and run it only in workspaces where the user accepts those local file mutations, and review the target project and title inputs before execution.

Risk: The PRD initializer has weaker path controls than the skill purpose requires.

Mitigation: Review and constrain init_prd.py path handling before use, especially project name handling and the generated output path.

Risk: Deployment and rollback scripts can replace installed skill files and restart the OpenClaw gateway.

Mitigation: Treat deploy.sh and rollback.sh as administrative operations and run them only after reviewing their effects in the target environment.

## Reference(s):

- [PM Skill on ClawHub](https://clawhub.ai/leio9511/skills/pm-skill)
- [PRD_001: Technical PM Skill Core Architecture](artifact/docs/PRDs/PRD_001_PM_Skill_Core_Architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown PRD files with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates PRD documents under the target workspace and may invoke local workflow scripts.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
