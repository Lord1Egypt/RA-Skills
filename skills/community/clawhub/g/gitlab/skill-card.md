## Description:

Avoid common GitLab CI/CD mistakes - rules gotchas, silent failures, and YAML merge traps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as reference guidance when authoring or reviewing GitLab CI/CD pipelines, especially around rules behavior, silent CI failures, YAML reuse, artifacts, cache behavior, Docker-in-Docker, and pipeline triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker-in-Docker guidance can lead to unsafe plaintext Docker daemon usage if copied outside an isolated, ephemeral CI job network.

Mitigation: Use plaintext Docker port 2375 or disabled TLS only inside isolated CI job networks, and prefer properly configured TLS or safer build approaches where possible.

## Reference(s):

- [ClawHub GitLab Skill Page](https://clawhub.ai/ivangdavila/skills/gitlab)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with inline GitLab CI/CD configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-only guidance; does not run code or request access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
