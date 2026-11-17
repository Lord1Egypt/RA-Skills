## Description:

Provides troubleshooting guidance and push templates for GitHub, Gitee, and AtomGit authentication failures and network timeouts, including a Git Data API fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose failed Git pushes and prepare platform-specific commands or API steps for publishing repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested pushes or API ref updates may publish unintended repository contents or target the wrong branch.

Mitigation: Review generated commands and confirm the remote, branch, and repository contents before execution.

Risk: Changing a private repository to public can expose previously restricted content.

Mitigation: Confirm repository visibility and inspect the contents before any visibility change.

Risk: Authentication tokens or other secrets may be exposed in command history or published code.

Mitigation: Keep credentials out of command history and repository contents; review commands for secret exposure.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/github-api-push-workaround)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the repository, authentication method, network conditions, and error logs.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; skill document states 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
