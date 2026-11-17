## Description:

Automates multi-round code review and iteration, with a defensive-programming mode for incremental coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingzhao-l](https://clawhub.ai/user/jingzhao-l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to review and improve a codebase across multiple rounds, or to carry out an incremental coding task with pre-checks, validation, and a review gate. Its review-only mode supports read-only code health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated iterations can change project files or introduce regressions.

Mitigation: Use a clean branch or worktree, confirm the project scope, review edits, and run configured validation; choose review-only mode for read-only checks.

Risk: The bundle ends during onboarding and omits the referenced CLI implementation, so its safeguards cannot be assessed from these files alone.

Mitigation: Review any separately installed tooling before relying on its onboarding, validation, or execution safeguards.

## Reference(s):

- [Project README](https://github.com/jingzhao-l/iterate-skill)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Markdown, Guidance]

**Output Format:** [Code and file changes, shell commands, and Markdown review reports or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify project files in iteration mode; review-only/dry-run mode is read-only.]

## Skill Version(s):

0.0.7 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
