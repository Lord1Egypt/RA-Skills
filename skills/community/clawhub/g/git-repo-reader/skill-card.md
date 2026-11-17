## Description:

Git Repo Reader gives agents a structured five-step method for quickly analyzing GitHub or local Git repositories, including project purpose, usage, entry points, core modules, and dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laojun509](https://clawhub.ai/user/laojun509)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly understand open-source or internal Git repositories for technical evaluation, onboarding, code review preparation, and contribution planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query GitHub for repository metadata and file listings when given a GitHub URL.

Mitigation: Use it only with repositories whose metadata can be queried through GitHub, and account for expected network access.

Risk: The skill may read files under a local repository path supplied by the user.

Mitigation: Point it only at the intended repository directory and avoid paths that contain unrelated private material.

## Reference(s):

- [Reading patterns reference](artifact/references/reading-patterns.md)
- [ClawHub skill page](https://clawhub.ai/laojun509/skills/git-repo-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown repository quick-read report with concise findings and inline commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize repository metadata, dependency files, entry points, and core module candidates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
