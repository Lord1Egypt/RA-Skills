## Description:

Read-only GitHub fallback for public repos: direct-first mirror clone/download plus gh api reads. No repository writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youbuwei](https://clawhub.ai/user/youbuwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve public GitHub content, clone public repositories, and download GitHub files when direct access is unreliable. It provides read-only GitHub API access and checks available direct and mirror routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private repository names could reach public mirrors through fallback.

Mitigation: Use this workflow only for public repositories, and keep private project names and sensitive resources out even when a personal proxy is configured.

Risk: Downloads may contact hosts outside the documented limits or return altered content.

Mitigation: Check the destination and compare downloads with an independently obtained official SHA-256 before use; constrain fallback hosts and redirects.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/youbuwei/skills/github-accelerator)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [GitHub text content, cloned repository directories, downloaded files, and status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public repository retrieval; no repository writes.]

## Skill Version(s):

1.3.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
