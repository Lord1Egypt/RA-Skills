## Description:

Find and fix code issues before publishing a PR. Single-pass review with auto-fix. Use when reviewing code changes before submission or auditing existing code for bugs/security. Don't use when running a coding agent to write code (use coding-agent) or checking GitHub CI status (use github).

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucksberg](https://clawhub.ai/user/glucksberg)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to review branch changes before opening a pull request or to audit selected code for correctness, security, reliability, performance, and quality issues. It can apply high-confidence fixes directly and returns a review or audit report for human verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may edit repository files automatically when it finds high-confidence issues.

Mitigation: Run it on a branch or clean working tree and review the resulting git diff before committing or publishing changes.

Risk: The skill reads local project guidance and configuration files as review context, which may include sensitive local instructions.

Mitigation: Avoid using it in repositories where CLAUDE.md, .claude/settings.json, or similar local guidance contains sensitive information that should not be included in review context.

Risk: Broad audit scopes can lead to large review contexts and wider auto-fix impact.

Mitigation: Prefer focused paths for audits and narrow or confirm scope before reviewing large codebases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glucksberg/skills/pr-review)
- [Artifact README](artifact/plugins/pre-review/README.md)
- [Pre-review command](artifact/plugins/pre-review/commands/pre-review.md)
- [Code-audit command](artifact/plugins/pre-review/commands/code-audit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with file references, issue classifications, applied-fix summaries, recommendations, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify repository files when high-confidence issues meet the skill's auto-fix thresholds. Requires git for branch-diff review mode.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
