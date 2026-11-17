## Description:

Structured development workflow inspired by Garry Tan's gstack for building features, starting projects, reviewing code, and shipping code through a disciplined Think, Plan, Build, Review, Test, and Ship process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jahonn](https://clawhub.ai/user/jahonn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run a structured development sprint from early product framing through planning, implementation, review, testing, and release preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can reach Build, Test, and Ship phases that modify files, run commands, commit changes, rebase branches, push code, or open pull requests.

Mitigation: Require the agent to show exact files, commands, branch, remote, and PR target before those phases, and confirm before commits, rebases, pushes, or overwriting DESIGN.md or PLAN.md.

Risk: The security review found broad activation and insufficient confirmation gates around ship-phase git push and PR actions.

Mitigation: Install only when an opinionated repository workflow is desired, and keep release actions behind explicit human approval.

## Reference(s):

- [Phase Prompts](references/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown, repository files, review reports, test reports, code changes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update DESIGN.md and PLAN.md, propose or execute code changes, run tests, and prepare branch or PR steps depending on the phase used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
