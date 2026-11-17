## Description:

MoneybigA helps agents perform multi-framework stock analysis for A-share, Hong Kong, and U.S. equities, combining technical, fundamental, valuation, and quantitative-factor methods into research reports with scores, signals, risk notes, and HTML dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, active traders, investment researchers, and value investors can use this skill to request public-web stock research, financial analysis, valuation review, and technical signal summaries. The skill is intended to produce non-personalized research artifacts and does not execute trades or provide guaranteed investment outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock reports can include buy or sell labels, stop-losses, targets, and confidence scores that may be mistaken for personalized financial advice.

Mitigation: Present outputs as research only, require user review before acting, and make clear that the skill does not replace licensed financial advice.

Risk: Public web data may be delayed, incomplete, stale, or unavailable for suspended securities or during source outages.

Mitigation: Require the agent to disclose missing or uncertain data and base conclusions only on available public information.

Risk: The skill has no trading authority but may generate trading-style recommendations that users could apply directly.

Mitigation: Do not connect the skill to broker APIs or automated execution paths, and require independent verification before any trade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosmofang/skills/moneybiga)
- [ClawHub publisher profile](https://clawhub.ai/user/cosmofang)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown analysis and single-file interactive HTML dashboard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public web research, produces non-personalized financial research, and does not place trades, access credentials, or persist user data.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/package.json, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
