## Description:

Guides agents through iterative, multi-dimension code review and fixes, with a defensive workflow for incremental coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingzhao-l](https://clawhub.ai/user/jingzhao-l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review and improve code through repeated review and validation rounds, or to carry out incremental coding tasks with defensive checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Onboarding instructions may create ITERATE.md and iterate.config.yaml during review-only or dry-run workflows; the security scan was partial.

Mitigation: Before onboarding, confirm those project files may be created, then inspect the working tree and generated files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jingzhao-l/skills/iterate-skill-slimtest)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration files, Guidance]

**Output Format:** [Code and project file changes, Markdown reports, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Onboarding may create ITERATE.md and iterate.config.yaml in the project.]

## Skill Version(s):

0.0.9 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
