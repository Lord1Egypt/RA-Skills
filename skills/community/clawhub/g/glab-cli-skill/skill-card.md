## Description:

Guidance for using the GitLab CLI (`glab`) from the terminal for merge requests, issues, CI/CD pipelines and jobs, repository targeting and inspection, clone and fork workflows, self-hosted GitLab instances, and direct GitLab REST or GraphQL API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to work with GitLab from the terminal through `glab`, including merge requests, issues, CI/CD pipelines and jobs, repository context, self-hosted GitLab instances, and direct API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutating GitLab commands can affect the wrong project, host, branch, or object.

Mitigation: Before running mutating commands, verify the repository, host, branch, target object, and credentials.

Risk: GitLab tokens passed directly as command-line arguments can be exposed through shell history or process inspection.

Mitigation: Prefer interactive login or stdin-based token input, and avoid pasting real GitLab tokens into command-line arguments.

## Reference(s):

- [glab Quick Reference](references/quick-reference.md)
- [Authentication and Repository Context](references/auth.md)
- [Merge Requests](references/merge-requests.md)
- [Issues](references/issues.md)
- [CI/CD Pipelines and Jobs](references/ci.md)
- [glab api](references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command guidance is scoped to GitLab CLI workflows and should be checked against the installed `glab` version before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
