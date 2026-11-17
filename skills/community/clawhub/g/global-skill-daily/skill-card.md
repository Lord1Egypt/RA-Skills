## Description:

Global Skill Daily scans ClawHub and SkillHub every three days, compares skill ecosystem trends, recommends skills across rotating dimensions, and can save the resulting report to Obsidian, IMA FIM, and Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to monitor global and Chinese skill ecosystems, receive periodic recommendations, and publish a daily ecosystem brief to their configured destinations. It is useful for recurring skill discovery and trend comparison rather than for publishing, editing, or auditing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans local TRAE memory, project metadata, knowledge files, and installed skill names by default.

Mitigation: Use --no-context-scan for privacy-sensitive runs, and review the local context file before enabling scheduled operation.

Risk: Generated reports can be published to external Feishu and IMA destinations, and can also be written to an Obsidian vault.

Mitigation: Use --dry-run or disable individual channels with --no-feishu, --no-ima, or --no-obsidian, and verify recipient environment variables before use.

Risk: The skill requires Feishu and IMA credentials for full publishing behavior.

Mitigation: Provide only the intended FEISHU_* and IMA_* environment variables for the current runtime and remove or rotate them when access is no longer needed.

## Reference(s):

- [Global Skill Daily ClawHub listing](https://clawhub.ai/edwardwason/skills/global-skill-daily)
- [Publisher profile](https://clawhub.ai/user/edwardwason)
- [Project homepage from OpenClaw metadata](https://github.com/trae-solo/global-skill-daily)
- [Pain points reference](references/pain-points.md)
- [ClawHub](https://clawhub.ai)
- [SkillHub API](https://api.skillhub.cn)

## Skill Output:

**Output Type(s):** [markdown, json, text, shell commands, configuration]

**Output Format:** [Markdown reports, JSON snapshot and recommendation files, and command status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports can be written locally and published to Obsidian, IMA FIM, and Feishu when credentials and channel settings permit.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
