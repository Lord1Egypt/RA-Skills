## Description:

舆情监测智能体V2.0 helps an agent search daily technology news across AI, compute, collaboration tools, HarmonyOS, and 彩讯股份, score and filter the items, generate an H5 report, and push the report to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mia-liu842](https://clawhub.ai/user/mia-liu842)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operations teams can use this skill to monitor Chinese technology and company news, prioritize higher-signal items, and prepare a concise daily report for Feishu distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send generated reports to Feishu.

Mitigation: Use a fixed or approved Feishu destination and preview the report before sending.

Risk: The generated report may include financial or stock-related recommendations.

Mitigation: Treat financial recommendations as draft analysis that requires human review before business or investment use.

Risk: The HTML report generator handles untrusted news content unsafely.

Mitigation: Escape HTML content and validate output filenames before using the generator with untrusted news data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mia-liu842/skills/news-agent-v2-0)
- [Skill instructions](artifact/SKILL.md)
- [News source configuration](artifact/config.md)
- [Scoring rules](artifact/scoring.md)
- [Output rules](artifact/output_rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, HTML files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report text, generated HTML/H5 report file, and Feishu message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [News items are expected to include title, source link, summary, score, and source; displayed items are filtered at a 60-point threshold and sorted by score.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
