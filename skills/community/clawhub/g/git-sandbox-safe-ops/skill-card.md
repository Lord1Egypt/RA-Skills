## Description:

指导开发者在 WorkBuddy 沙箱中安全执行 Git fetch、push 和仓库恢复，并排查引用丢失、推送被拒等问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

开发者在受限的 WorkBuddy 沙箱中排查 Git 仓库和远端同步问题，恢复丢失的仓库元数据，并核对推送结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guidance encourages agents to inspect and reuse stored GitHub credentials without asking first.

Mitigation: Require explicit approval before accessing tokens, environment secrets, or SSH keys; prefer interactive login or scoped credentials for the specific repository.

Risk: Git recovery steps can change repository state, remote URLs, Git configuration, or persistent PATH settings.

Mitigation: Review the target repository and proposed changes, preserve important work, and obtain approval before persistent configuration changes or pushes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/git-sandbox-safe-ops)
- [ClawHub publisher profile](https://clawhub.ai/user/oracis)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repository-specific steps require review before execution.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
