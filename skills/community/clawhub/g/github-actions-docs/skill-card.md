## Description:

Use when users ask how to write, explain, customize, migrate, secure, or troubleshoot GitHub Actions workflows, workflow syntax, triggers, matrices, runners, reusable workflows, artifacts, caching, secrets, OIDC, deployments, custom actions, or Actions Runner Controller, especially when they need official GitHub documentation, exact links, or docs-grounded YAML guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer GitHub Actions workflow, runner, security, deployment, migration, and troubleshooting questions with current official GitHub documentation and concise docs-grounded examples when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce outdated or misleading GitHub Actions guidance if it answers from memory or relies on an imprecise documentation page.

Mitigation: Follow the artifact workflow to search and open current official docs.github.com Actions pages before answering, and cite the closest authoritative page.

Risk: Security-sensitive topics such as secrets, GITHUB_TOKEN, OIDC, and artifact attestations could be mishandled if guidance is not grounded in official documentation.

Mitigation: Use the GitHub Actions security documentation as the source of truth and provide examples only when they are necessary and documentation-grounded.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eohmig/skills/github-actions-docs)
- [GitHub Actions Topic Map](references/topic-map.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Migrating to GitHub Actions](https://docs.github.com/en/actions/tutorials/migrate-to-github-actions)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with documentation links and optional YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be grounded in current official GitHub Actions documentation and include concise examples only when useful.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
