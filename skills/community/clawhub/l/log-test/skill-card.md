## Description:

按级别筛选日志文件并生成 Markdown 摘要报告

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinaadler77-max](https://clawhub.ai/user/chinaadler77-max)

### License/Terms of Use:

MIT-0

## Use Case:

开发者和工程师可在需要分析日志、提取错误或生成日志报告时，提供日志文件路径并按级别筛选条目。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安全扫描未发现问题并判定为 benign，但由于 SKILL.md 中一个类似路径的引用无法解析，分析并未覆盖完整证据。

Mitigation: 部署前核对该路径引用并确认完整文件已纳入审查。

## Reference(s):

- [Log Test on ClawHub](https://clawhub.ai/chinaadler77-max/skills/log-test)

## Skill Output:

**Output Type(s):** [Markdown]

**Output Format:** [Markdown summary with severity counts and matching log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [筛选指定级别及以上的条目；可限制输出条目数。]

## Skill Version(s):

1.0.0 (source: frontmatter; confirmed by server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
