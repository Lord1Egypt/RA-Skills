## Description:

Git助手专业版 helps development teams analyze Git conflicts, suggest limited automatic fixes, run repository health diagnostics, and provide recovery guidance for common Git workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect Git conflicts, diagnose repository health across one or more projects, generate Git workflow guidance, and review recovery steps before applying repository-changing commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill teaches automatic repository-changing recovery steps, including hard resets labeled as safe.

Mitigation: Review the exact repository path and commands, create a backup branch or stash, and require explicit confirmation before running automatic recovery or hard reset steps.

Risk: Conflict auto-fixes can modify files and may choose an incorrect resolution for non-trivial conflicts.

Mitigation: Limit automatic fixes to simple conflict classes, inspect diffs after changes, and keep complex conflicts in manual review.

## Reference(s):

- [Detailed Reference](references/detail.md)
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/git-helper-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell/Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository diagnostics, conflict analysis, recovery plans, and suggested commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
