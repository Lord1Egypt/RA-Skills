## Description:

审计项目中的 AGENTS.md、CLAUDE.md 与 skills 配置，生成评分卡和优先级修复建议，并可在用户确认后协助修改；可选编排宿主环境检查，密钥检测仅静态扫描正文模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT-0

## Use Case:

外部开发者可用它检查项目的 AGENTS.md、CLAUDE.md 和 Agent skills 配置，获得评分、定性复核与优先级修复建议；需要时可在确认后修改配置文件。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker examples may use image references that are not pinned to a trusted version or digest, and the project directory is mounted writable.

Mitigation: Before running an example, verify the image source and pin a trusted version or digest; ensure the writable mount points to the intended project directory.

Risk: The security review was partial and did not resolve all referenced paths or assess GIF binary behavior.

Mitigation: Review unresolved referenced files and inspect binary assets separately before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huiyonghkw/skills/hekouwang-claude-md-doctor-skill)
- [Project homepage](https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill)
- [Doctor suite guide](artifact/references/doctor-suite.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Configuration]

**Output Format:** [Text or JSON score report with Markdown findings and prioritized remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest or apply configuration edits after user confirmation.]

## Skill Version(s):

1.3.7 (source: frontmatter, changelog, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
