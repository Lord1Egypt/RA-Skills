## Description:

Helps agents inspect GitLab projects, issues, merge requests, and pipelines, and perform requested GitLab write operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiguang1017](https://clawhub.ai/user/weiguang1017)

### License/Terms of Use:

MIT

## Use Case:

Developers and DevOps engineers use this skill to inspect GitLab projects, issues, merge requests, and CI/CD pipelines, and to create issues or merge requests, merge changes, or start pipelines when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A GitLab token with write access can enable consequential repository changes without an enforced confirmation gate.

Mitigation: Prefer project-scoped or read-only tokens where possible; require explicit human confirmation before creating issues or merge requests, merging, or triggering pipelines, and keep protected-branch and approval rules enabled.

## Reference(s):

- [GitLab Skills usage guide](references/USAGE.md)
- [Release source repository](https://github.com/weiguang1017/gitlab-devops-skill)
- [ClawHub skill release](https://clawhub.ai/weiguang1017/skills/gitlab-devops-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Text guidance and commands; GitLab CLI responses in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [GitLab command failures return a non-zero exit status.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
