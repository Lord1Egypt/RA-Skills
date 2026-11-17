## Description:

Analyzes news and event-driven signals for Chinese equity markets, including policy, company, industry, and sentiment events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and financial research workflows use this skill to structure event-driven market commentary around policy changes, company announcements, industry events, market sentiment, related securities, historical analogs, and risk controls. Outputs should be treated as educational analysis, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate buy, sell, timing, position-size, target-price, and stop-loss suggestions that users may mistake for personalized financial advice.

Mitigation: Present outputs as educational market commentary, require independent verification, and avoid using the skill as the sole basis for trading decisions.

Risk: Event-driven analysis can become stale if current news or announcements are not retrieved successfully.

Mitigation: State whether current news was searched and included; when search fails, label the report as based on historical patterns or framework analysis.

Risk: The bundled report template contains a hard-coded analyst attribution.

Mitigation: Remove or replace the attribution before publishing reports unless the attribution has been verified.

## Reference(s):

- [Event Analysis Template](artifact/references/event-analysis-template.md)
- [Event Classification](artifact/references/event-classification.md)
- [Historical Cases](artifact/references/historical-cases.md)
- [Quick Start](artifact/references/quick-start.md)
- [ClawHub Skill Page](https://clawhub.ai/wang-junjian/skills/news-event-driven-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis reports with tables, ratings, risk notes, and action-oriented commentary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market impact ratings, affected securities, timing, position sizing, stop-loss guidance, and source freshness notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
