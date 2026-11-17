## Description:

Apply safe Git workflow rules for local repositories, including branch naming, commits, staging review, and history handling without risking unrelated or shared work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sf0799](https://clawhub.ai/user/sf0799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep agent-assisted Git work scoped, reversible, and respectful of existing workspace changes and shared history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence Git branch, commit, staging, and history guidance, where incorrect advice could affect repository state.

Mitigation: Review proposed Git commands and repository status before execution, especially for history-changing operations.

Risk: The skill is guidance-only and does not include executable safeguards.

Mitigation: Rely on the agent and reviewer to inspect changes, avoid unrelated workspace edits, and prevent secrets from entering commits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sf0799/skills/git-discipline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with concise status summaries, recommendations, and inline Git commands when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language skill interface; implicit invocation is disabled.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
