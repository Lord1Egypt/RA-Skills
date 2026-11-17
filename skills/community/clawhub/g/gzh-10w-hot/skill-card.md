## Description:

全网持续收录每日超过1000+公众号10w+文章内容，向用户推送公众号达到10w+阅读的热门文章，并支持全领域、特定领域和每日订阅场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, editors, marketers, and researchers use this skill to retrieve WeChat Official Account articles that reached 10w+ reads, compare category rankings, analyze viral patterns, and generate shareable ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a REDFOX_API_KEY and may expose sensitive credential context through logs, prompts, or generated outputs if handled casually.

Mitigation: Use a dedicated, revocable API key; configure it only as an environment variable; avoid hard-coding it; and avoid sharing logs from runs of this skill.

Risk: Generated HTML reports include external article data and load a third-party PDF-export script, so the rendered page should be treated as untrusted content.

Mitigation: Review generated reports before sharing, open them in a constrained browser context when possible, and avoid using the HTML output with sensitive browsing sessions.

Risk: Server security evidence marks the release as suspicious, so deployment without review may miss credential-handling or report-rendering risks.

Mitigation: Review the skill before installing or enabling it for users, with particular attention to credential handling and generated report behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/gzh-10w-hot)
- [API interface specification](artifact/references/api-spec.md)
- [Category mapping reference](artifact/references/category-mapping.md)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown rankings and analysis, with optional generated HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured REDFOX_API_KEY and may create a temporary article data JSON file plus an HTML report when requested.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
