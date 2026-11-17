## Description:

Checks Chinese text for advertising-law issues, major platform policy risks, and AI-writing patterns, then produces a structured report and a platform-adapted rewrite suitable for user review before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeshenyue12345](https://clawhub.ai/user/yeshenyue12345)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to review Chinese copy for advertising-law, platform-policy, and AI-style risks, then obtain a concise compliance report and a rewritten draft. It is drafting support and does not replace legal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for legal approval because it reviews advertising-law and platform-compliance issues.

Mitigation: Treat the report and rewritten copy as drafting support, and route high-risk or regulated content through qualified legal review before publication.

Risk: The artifact states that it does not read local files, while also allowing file reading after explicit user confirmation.

Mitigation: Only confirm local-file reads when the exact file is intended as the text to check, and avoid providing unrelated or sensitive files.

Risk: The skill relies on web search for current policy and enforcement updates, so search quality and source freshness can affect recommendations.

Mitigation: Review cited policy sources and platform rules before acting on the rewritten content, especially for regulated categories.

## Reference(s):

- [广告法合规检查清单](references/ad-law-checklist.md)
- [各主流平台内容规范](references/platform-rules.md)
- [去AI化写作检查清单](references/anti-ai-checklist.md)
- [各平台发布格式指南](references/platform-format-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables and copy-ready rewritten text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes compliance findings, platform-format recommendations, and a publish-ready rewritten draft for user review.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and manifest state 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
