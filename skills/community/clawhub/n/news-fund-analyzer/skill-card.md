## Description:

Analyzes recent news, macroeconomic signals, market sentiment, fund holdings, and industry policy to explain fund movement and produce cautious fund research guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to generate fund diagnosis, price-movement explanations, portfolio-adjustment suggestions, and policy-impact analysis. The skill asks for fund details, holding status, investment horizon, and risk preference before producing a structured report with forecasts, risk notes, and a disclaimer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce model-generated investment actions that may be mistaken for professional financial advice.

Mitigation: Treat outputs as research support, require user review before acting, and preserve the disclaimer that fund investing carries risk.

Risk: Fund, market, portfolio, or risk-preference queries may be sent to external search engines through the bundled search helper.

Mitigation: Avoid submitting sensitive personal or account-level data, and review search queries before execution.

Risk: The bundled general search helper has broader scope than the fund-analysis task.

Mitigation: Use the search helper only for fund, market, macroeconomic, policy, and holdings research needed by this skill.

## Reference(s):

- [News Fund Analyzer ClawHub Listing](https://clawhub.ai/nidhov01/skills/news-fund-analyzer)
- [International Search Guide](artifact/multi-search-engine-2.0.1/references/international-search.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown fund analysis report with structured sections, probability estimates, action guidance, risk notes, and disclaimer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market and fund analysis, forecast scenarios, suggested position sizing, watch items, and risk warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
