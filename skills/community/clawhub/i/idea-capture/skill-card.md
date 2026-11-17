## Description:

Capture or update an idea, append an update log, and write a session summary for later retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kid0114](https://clawhub.ai/user/kid0114)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to capture project ideas, update existing idea records, and preserve concise session summaries for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unconstrained idea IDs or catalog IDs could cause writes outside the intended ideas directory.

Mitigation: Restrict idea IDs to a slug format, validate IDs loaded from catalog.json, and enforce that resolved write paths stay under the ideas directory.

Risk: Using untrusted titles, idea IDs, or catalog data may lead to unintended local file changes.

Mitigation: Review or fix the script before installing it in workspaces that process untrusted idea data, and review changed files after each run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kid0114/skills/idea-capture)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown idea files, JSON catalog data, and a short JSON status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace-local files under the ideas directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
