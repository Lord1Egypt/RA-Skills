## Description:

一键同步Hermes配置和数据到GitHub，支持多设备间无缝切换。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangwenhao66](https://clawhub.ai/user/zhangwenhao66)

### License/Terms of Use:

MIT-0

## Use Case:

Hermes users and developers use this skill to back up and move Hermes configuration, memories, skills, and optional session or authentication files between Mac, Windows, and GitHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync flow can upload Hermes secrets, sessions, memories, and skills to GitHub with too little user control.

Mitigation: Use only a private repository you own, remove .env, auth.json, sessions, and other secrets from the sync flow, and inspect git status and diffs before every push.

Risk: Pulling memories or skills from an untrusted repository can restore unsafe or unwanted local agent content.

Mitigation: Pull only from trusted repositories and review the exact changes before copying repository content into the Hermes directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangwenhao66/skills/github-config-sync)
- [Publisher profile](https://clawhub.ai/user/zhangwenhao66)
- [Configured GitHub sync repository](https://github.com/zhangwenhao66/hermes-config.git)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides Git-based push and pull guidance for Hermes backup and restore workflows.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
