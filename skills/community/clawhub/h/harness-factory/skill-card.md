## Description:

Use when building features, fixing complex bugs, or doing major refactoring. Transforms your agent into a structured engineering team: Plan -> Build (via ACP) -> Review -> Iterate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guixiang123124](https://clawhub.ai/user/guixiang123124)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan, delegate, review, iterate, and ship non-trivial code changes through a structured harness workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow delegates repository reads and writes to Claude/ACP agents.

Mitigation: Require explicit approval before launching external-agent sessions and limit each session to the intended project and file scope.

Risk: The workflow includes commit, push, deploy, and production verification steps.

Mitigation: Require explicit approval for commit, push, deploy, and production checks before those actions run.

Risk: A broad AGENTS.md auto-trigger can keep the workflow persistently active.

Mitigation: Avoid adding the broad auto-trigger unless persistent activation is desired for the repository.

Risk: Using git add -A may stage unrelated files.

Mitigation: Stage reviewed files explicitly instead of staging the entire working tree.

Risk: Bare npx commands may use unpinned project tooling.

Mitigation: Prefer project-pinned build and check commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guixiang123124/skills/harness-factory)
- [Code Quality Checklist](references/code-quality-checklist.md)
- [Evaluation Dimensions](references/evaluation-dimensions.md)
- [Harness Engineering Metrics](references/metrics.md)
- [Security Checklist for Harness Reviews](references/security-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to produce sprint plans, review reports, harness reports, code changes, commits, pushes, and deployment checks.]

## Skill Version(s):

0.7.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
