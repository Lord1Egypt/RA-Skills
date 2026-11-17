## Description:

AI-driven Chinese content lifecycle skill for topic research, content generation, fact checking, visual formatting, GEO checks, WeChat draft publishing, Toutiao publishing preparation, and analytics review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikogeyu-cell](https://clawhub.ai/user/mikogeyu-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams and individual publishers use this skill to manage Chinese-language article workflows across WeChat Official Accounts and Toutiao, from topic selection and draft preparation through review, publishing, and performance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real WeChat and Toutiao publishing credentials and account actions.

Mitigation: Keep config.yaml out of version control, avoid passing secrets on the command line, and require explicit human confirmation before publishing or deleting drafts.

Risk: Security review notes a token fragment leak and under-documented side effects.

Mitigation: Remove the token-printing behavior before use and review publishing side effects, especially draft deletion and Playwright-driven account actions.

Risk: Generated footers, calls to action, QR codes, and outbound links can publish incorrect or unwanted content.

Mitigation: Inspect all generated footer blocks, CTA text, QR images, and links before approving publication.

Risk: Automated content and data claims can be inaccurate or unsupported.

Mitigation: Use the included fact-checking workflow, require traceable sources for quantitative claims, and remove claims that cannot be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikogeyu-cell/skills/omnipub-content-engine)
- [Topic research workflow](artifact/references/01-topic-research.md)
- [Content generation workflow](artifact/references/02-content-generation.md)
- [Fact-checking workflow](artifact/references/03-fact-checking.md)
- [Charts and infographics workflow](artifact/references/04-charts-infographics.md)
- [Footer style workflow](artifact/references/05-footer-styles.md)
- [GEO optimization workflow](artifact/references/06-geo-optimization.md)
- [Publishing workflow](artifact/references/07-publishing.md)
- [Analytics workflow](artifact/references/08-analytics.md)
- [WeChat CSS constraints](artifact/references/wechat-css-constraints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and HTML content guidance with CLI commands, generated scripts, configuration examples, and analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeChat-compatible HTML, Toutiao publishing preparation scripts, fact-check reports, GEO reports, infographic prompts, footer templates, and analytics reports.]

## Skill Version(s):

2.0.0 (source: server release metadata, artifact manifest, and SkillHub metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
