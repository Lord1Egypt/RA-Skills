## Description:

牛股王涨停全景 helps agents answer A-share limit-up and momentum-trading questions using disclosed public Niuguwang market-data endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maomaoxx779-cmd](https://clawhub.ai/user/maomaoxx779-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to summarize A-share limit-up conditions, seal rates, promotion success rates, prior-day limit-up performance, and multi-board matrices for short-term market sentiment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a fixed promotional footer and download link in every answer.

Mitigation: Review the skill before installation and apply the footer only when relevant market data is shown, if local policy permits modification.

Risk: Market-data summaries can be mistaken for investment advice.

Mitigation: Keep the investment-risk disclaimer visible and require human review before trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maomaoxx779-cmd/skills/limit-up-panorama)
- [Publisher profile](https://clawhub.ai/user/maomaoxx779-cmd)
- [Niuguwang app and PC download page](https://www.stockhn.com/#/appDownload)
- [Limit distribution API endpoint](https://stq.niuguwang.com/taoquant/FXB/LimitDistribution?type=0&s=_test&version=6.9.5&packtype=1&night=0)
- [Limit board time-series API endpoint](https://stq.niuguwang.com/taoquant/DBXF/GetLimitBoard)
- [Momentum board summary API endpoint](https://stq.niuguwang.com/taoquant/DBXF/GetDBXFShowData?s=_test&version=6.9.5&packtype=1&night=0)
- [Multi-board matrix API endpoint](https://stq.niuguwang.com/taoquant/DBXF/GetLBJZ?s=_test&version=6.7.6&packtype=1&night=0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with API request examples and market-data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to include source attribution and an AI-generated investment-risk disclaimer.]

## Skill Version(s):

1.0.0 (source: manifest.yaml, _meta.json, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
