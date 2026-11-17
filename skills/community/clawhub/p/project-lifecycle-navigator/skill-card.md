## Description:

Audits project direction, scope drift, repository health, and recent delivery alignment to produce bounded go, narrow, pivot, archive, or stop recommendations without changing code or governance state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[englandtong](https://clawhub.ai/user/englandtong)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and project owners use this skill to decide whether to start, continue, narrow, pivot, archive, or stop a project. It supports new project intake, mid-project realignment, read-only repository health review, latest delivery alignment, and owner-led target rebaseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated implementation plans, task queues, or code snippets may be mistaken for authorization to change a project.

Mitigation: Require explicit owner approval and a separate execution workflow before any agent or engineer modifies code, files, or governance state.

Risk: Repository audits may encounter hardcoded credentials, personal contact data, or other sensitive values in shipped artifacts.

Mitigation: Report only the file path and exposure category; do not copy secret or sensitive values into the report.

Risk: Lifecycle recommendations can be based on incomplete or unverified evidence.

Mitigation: Label unknowns as cannot-confirm or not-executed and keep facts, inferences, risks, and owner decisions visibly separate.

## Reference(s):

- [Project Lifecycle Navigator Skill Page](https://clawhub.ai/englandtong/skills/project-lifecycle-navigator)
- [Quickstart](artifact/QUICKSTART.md)
- [Security](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown reports with structured findings, recommendations, and handoff instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only advisory output; implementation plans, task queues, and code snippets require explicit approval before execution.]

## Skill Version(s):

2.1.1 (source: server release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
