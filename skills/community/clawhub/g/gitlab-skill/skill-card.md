## Description:

Provides GitLab operations for creating and cloning repositories, listing projects, and managing issues, merge requests, branches, commits, and pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pickbert](https://clawhub.ai/user/pickbert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to interact with GitLab projects from an agent, including repository discovery, issue and merge request workflows, branch and commit inspection, pipeline checks, and project creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitLab access tokens could be exposed through insecure TLS, unvalidated hosts, token-bearing HTTPS remotes, persistent local credential files, shared terminal logs, or CI logs.

Mitigation: Use a controlled environment with a trusted HTTPS GitLab host, short-lived least-privilege tokens, environment variables or a user config file with restrictive permissions, and avoid --insecure mode, token-bearing remotes, clone helpers, and commands that print tokens or credential files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pickbert/skills/gitlab-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, links, JSON snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform GitLab API and git operations using configured credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
