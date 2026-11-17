## Description:

Automates an end-to-end GitHub issue workflow, from listing and grouping open issues through code fixes, PR creation, CI/CD checks, merge, deployment verification, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdyshi](https://clawhub.ai/user/gdyshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to triage batches of GitHub issues, plan grouped fixes, create a branch and PR, monitor CI/CD, merge, verify deployments, and report results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to modify repository code, push branches, create PRs, merge changes, and check deployments with real write authority.

Mitigation: Require explicit human approval for selected issues, file scope, push, PR creation, merge, and deployment steps before execution.

Risk: GitHub issue bodies can influence the workflow even though they are untrusted problem descriptions.

Mitigation: Treat issue content as untrusted input and validate planned changes against repository policy before applying them.

Risk: The workflow mentions admin merge override behavior that could bypass normal branch protections.

Mitigation: Do not allow admin merge overrides by default; require a separate approval path when repository policy permits it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gdyshi/skills/github-iteration-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow plans, GitHub CLI commands, commit and branch conventions, PR body structure, CI/CD remediation steps, and deployment status reporting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
