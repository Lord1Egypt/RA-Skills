## Description:

Iterative code review using multiple independent subagent reviewers, assisting with PR or code review through parallel analysis and optional automated fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciuscao](https://clawhub.ai/user/luciuscao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run iterative PR and code reviews with parallel reviewer subagents, severity-ranked findings, user-controlled fix rounds, and final full-review validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional automation can modify code or continue review rounds without prompting each time.

Mitigation: Keep the default interactive mode for important repositories and enable autoFix or autoContinue only when unattended edits are acceptable.

Risk: Automated fixes or review suggestions may introduce incorrect changes or miss project-specific intent.

Mitigation: Review generated changes, require user confirmation where appropriate, and run project build and test commands before accepting fixes.

Risk: Build or test commands may rely on unpinned registry fallback behavior when local project binaries are unavailable.

Mitigation: Prefer project-local build and test binaries or pinned dependencies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luciuscao/skills/iterative-code-review)
- [Automation Preferences](references/automation.md)
- [Pre-flight Checks](references/preflight.md)
- [Workflow](references/workflow.md)
- [Code Review Checklist](references/checklist.md)
- [Issue Severity](references/issue-severity.md)
- [Final Round Guide](references/final-round.md)
- [Exit Criteria](references/exit-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown review findings with severity labels, code guidance, configuration snippets, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default behavior asks for user confirmation before fixes; optional automation can edit code or continue review rounds when explicitly configured.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact SKILL.md reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
