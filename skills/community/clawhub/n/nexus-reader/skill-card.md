## Description:

从微信读书飙升榜抓取热门书籍数据，并生成每日读书推荐卡片（HTML/PNG）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwter](https://clawhub.ai/user/lwter)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to fetch WeRead rising-list book data, create recommendation copy, and render shareable daily reading cards. It also supports recurring daily recommendation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML and PNG rendering can expose users to browser injection or outbound requests when card JSON contains untrusted cover_url or book_url values.

Mitigation: Use card JSON only from trusted sources, validate URLs before rendering, and review generated HTML before previewing or sharing it.

Risk: The skill contacts WeRead and writes local cache/card files during normal operation.

Mitigation: Run it only in workspaces where those network requests and local files are acceptable, preferably with restricted filesystem access until URL validation and template escaping are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lwter/skills/nexus-reader)
- [WeRead rising category](https://weread.qq.com/web/category/rising)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; generated artifacts are JSON, HTML, and optional PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local card/cache files; PNG rendering requires an optional html2image dependency.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
