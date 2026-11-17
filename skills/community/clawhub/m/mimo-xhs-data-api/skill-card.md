## Description:

A social-media content data analysis skill for Xiaohongshu-centered strategy, creator collaboration, competitor monitoring, market insight, cross-platform comparison, and operational optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, operators, and developers use this skill to ask an agent for Chinese-language analysis of public Xiaohongshu and cross-platform content performance, creator fit, competitor strategy, market demand, titles, tags, publishing time, and 30-day optimization plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the provider's external XHS_API_KEY service for social-media analytics.

Mitigation: Use only approved API keys, avoid submitting confidential plans, secrets, or personal data without approval, and review provider terms before deployment.

Risk: Platform algorithm formulas, benchmark numbers, and public-data coverage may be incomplete or change over time.

Mitigation: Treat formulas and benchmarks as advisory, include API coverage notes and data gaps in outputs, and validate recommendations against current campaign data before acting.

## Reference(s):

- [聚合接口完整参考](references/aggregate-api.md)
- [xhs-data-api 详细参考](references/details.md)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Chinese Markdown analysis with structured recommendations, metric comparisons, API-backed findings, caveats, and action plans.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the provider's XHS_API_KEY service; outputs should cite coverage notes and data gaps when API responses provide them.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
