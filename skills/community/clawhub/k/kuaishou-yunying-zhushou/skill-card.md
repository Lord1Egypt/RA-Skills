## Description:

快手运营分析助手 helps agents search Kuaishou videos, list creator posts, and fetch video comments as structured JSON for content planning, competitor monitoring, KOL screening, and sentiment or trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketing teams, analysts, and agent operators use this skill to collect public Kuaishou search results, creator posts, and video comments for trend research, competitor monitoring, KOL screening, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou search terms, profile or video URLs, limits, and GUAIKEI_API_TOKEN are sent to the third-party API service.

Mitigation: Use approved tokens and approved inputs only, and confirm that third-party API use is authorized before submitting business-sensitive targets.

Risk: Generated logs may contain sensitive business research, URLs, comments, or analysis inputs.

Mitigation: Protect the logs directory with appropriate access controls and delete generated logs when they are no longer needed.

Risk: The skill depends on third-party API availability and may return empty, failed, delayed, or incomplete public-data results.

Mitigation: Check the returned status and error_code fields before relying on results, and verify important findings before using them in decisions.

## Reference(s):

- [完整选项参数说明](artifact/references/options.md)
- [更新日志](artifact/references/changelog.md)
- [快手运营助手官网](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishou-yunying-zhushou)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful command output includes status, request metadata, execution metadata, and results, and local logs may be written.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, released 2026-09-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
