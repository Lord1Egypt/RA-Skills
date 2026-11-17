## Description:

Review daily memory logs and consolidate durable knowledge into the existing memory hierarchy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review daily memory logs, identify durable signals, resolve them against existing canonical memory, and update or report on the memory hierarchy without accumulating duplicate or transient notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can be tricked into writing state JSON outside the intended workspace if the scan file is tampered with.

Mitigation: Only run the skill on trusted workspaces and trusted scan files until the helper restricts commit-state writes to the intended workspace state file and rejects absolute or traversal paths.

## Reference(s):

- [Memory Review Specification](references/spec.md)
- [ClawHub memory-review release page](https://clawhub.ai/axelhu/skills/memory-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON decision plans, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write canonical memory files, daily review reports, execution logs, and scan state when the workflow is followed.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
