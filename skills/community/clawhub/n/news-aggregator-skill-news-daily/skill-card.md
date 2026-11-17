## Description:

每日综合新闻简报可自动抓取并生成包含科技、财经和热点内容的综合报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[arsoooo](https://clawhub.ai/user/arsoooo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent collect daily news from configured sources, organize it into four sections, save a Markdown report, and optionally create a Feishu document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a referenced news-aggregator-skill and its scripts, which are not included in this artifact.

Mitigation: Install only after separately auditing the referenced skill and scripts.

Risk: The artifact suggests a hard-coded network proxy.

Mitigation: Use only an approved proxy that belongs to the deployment environment.

Risk: Generated reports may be saved locally or published to Feishu.

Mitigation: Confirm the report content and destination before saving or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arsoooo/skills/news-aggregator-skill-news-daily)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown report with inline shell commands and local file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports under reports/YYYY-MM-DD/ and optionally create a Feishu document.]

## Skill Version(s):

1.0.0 (source: release metadata, artifact version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
