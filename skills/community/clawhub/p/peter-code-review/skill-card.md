## Description:

Pre-commit quality gate that runs local tests, static checks, and risk review to decide whether a change is ready to commit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasilva](https://clawhub.ai/user/chinasilva)

### License/Terms of Use:


## Use Case:

Developers use this skill before committing or opening a pull request to review workspace or HEAD changes, run relevant quality checks, summarize failures, and produce a commit readiness recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run local repository validation commands, which may execute project scripts in the current workspace.

Mitigation: Install and run it only in repositories where local validation commands are trusted, and review command output before treating any check as passed.

Risk: For Node and TypeScript projects, the documented typecheck command uses npx and may download or resolve tooling dynamically.

Mitigation: Prefer a pinned project script or local ./node_modules/.bin/tsc invocation when adapting the workflow for a project.

Risk: UI changes may still need manual smoke validation even when lint, typecheck, and tests pass.

Mitigation: Record UI validation as not executed unless manual smoke checks were actually completed, and include the remaining UI risk in the final conclusion.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown code review report with command results, risk findings, remediation guidance, and a commit readiness conclusion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes a fixed checklist, git change summary, command outcomes, severity-ranked issues, and one of the documented commit conclusions.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
