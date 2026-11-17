## Description:

OpenClaw每日资讯汇总 collects, categorizes, risk-rates, and formats OpenClaw-related public news into Chinese Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fashionzzz](https://clawhub.ai/user/fashionzzz)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams tracking the OpenClaw ecosystem use this skill to search recent public-web items, classify them by security, industry, technology, policy, and related AI trends, and produce concise Chinese Markdown briefings for monitoring and decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web-sourced text is rendered into Markdown without escaping, so generated reports may contain misleading claims, unsafe links, or content that should not be trusted as instructions.

Mitigation: Verify important claims and links independently, and sanitize generated Markdown before feeding it into another agent or automation workflow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fashionzzz/skills/openclaw-daily-news)
- [OpenClaw news report template](references/news_template.md)
- [OpenClaw daily news usage examples](references/usage_examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance, Code, Shell commands, Configuration]

**Output Format:** [Chinese Markdown report text with categorized news summaries, risk levels, source links, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are intended for direct conversation output and should be treated as untrusted public-web summaries.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact configuration)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
