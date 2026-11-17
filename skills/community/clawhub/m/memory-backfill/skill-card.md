## Description:

Standardizes agent memory backfill by upgrading abstract memory into project-level records with result status, evidence anchors, gaps, and reusable acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangwill2023](https://clawhub.ai/user/jiangwill2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to standardize memory backfill tasks, acceptance checks, and archive records across agent workspaces. It is intended for cases where memory files need project facts, result closure status, and evidence paths rather than abstract principles alone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to read sensitive context files and persist memory entries that may influence future agent behavior.

Mitigation: Require the agent to show exact files and diffs, approve changes manually, and limit reads and writes to intended workspace memory files.

Risk: Stored memory text could be mistaken for instructions in later work.

Mitigation: Treat stored memory as project context rather than executable instruction, and review proposed memory content before accepting it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiangwill2023/skills/memory-backfill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with task templates and acceptance checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead an agent to propose or edit workspace memory files after user review.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact _meta.json and skill text list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
