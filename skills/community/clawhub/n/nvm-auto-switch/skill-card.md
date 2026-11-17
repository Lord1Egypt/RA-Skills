## Description:

根据 package.json 中的 engines 字段自动检测 Node.js 版本要求，如未安装 nvm 则自动安装，并切换到正确的 Node 版本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[piaolingwuyu](https://clawhub.ai/user/piaolingwuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to detect a Node.js version requirement from a project's package.json and switch the local nvm-managed Node version for development setup, project entry, version mismatch fixes, or CI/CD setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download and execute an unverified remote nvm installer and change the local developer environment.

Mitigation: Review before installing; prefer manually installing nvm from a trusted source first, then use this skill only for version switching or require download verification and an explicit consent gate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piaolingwuyu/skills/nvm-auto-switch)
- [nvm installer script referenced by artifact](https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to run scripts that change the local Node.js and nvm environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
