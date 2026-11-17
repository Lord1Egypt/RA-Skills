## Description:

Prioritizes issues from a named GitHub repository or supplied issue set by ROI, solution sanity, architectural impact, and actionability without modifying repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucksberg](https://clawhub.ai/user/glucksberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and contributors use this skill to rank GitHub issues, identify quick wins, filter non-actionable items, and match work to contributor skill levels before deciding what to work on.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: History cleanup can delete unrelated local directories if --history-dir points at a broad or shared path.

Mitigation: Use a dedicated empty state directory for --history-dir, avoid home directories, project roots, /tmp, and shared directories, and keep --retain conservative until cleanup logic is constrained.

## Reference(s):

- [Issue Prioritizer on ClawHub](https://clawhub.ai/glucksberg/skills/issue-prioritizer)
- [GitHub CLI](https://cli.github.com/)
- [jq](https://jqlang.github.io/jq/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown issue prioritization report with optional JSON summaries and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only ranking and recommendations; no repository mutations.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
