## Description:

US Stock AI Trading Assistant | SkillBoss API Hub Stock Forecast - smart analysis of stock entry and exit points, target price predictions, probability calculations, and technical ratings with support for "Should I Buy" investment decision Q&A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request single-symbol stock or crypto forecasts and buy, sell, or hold analysis through SkillBoss API Hub. It is intended for informational market analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker queries and analysis prompts are sent to SkillBoss API Hub as outbound API requests.

Mitigation: Install only if SkillBoss is trusted for the submitted queries, use a scoped API key, and avoid private portfolio or account details in prompts.

Risk: Forecasts and buy, sell, or hold analysis may be incomplete, delayed, or unsuitable for financial decision-making.

Mitigation: Treat outputs as informational only and verify material decisions with authoritative market data or a qualified financial professional.

Risk: The optional Python path depends on the requests package and local environment handling of API credentials.

Mitigation: Use curl or an isolated Python environment when reducing dependency risk, and keep SKILLBOSS_API_KEY out of shared logs and prompts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/intellectia-stock-forecast-2)
- [Publisher Profile](https://clawhub.ai/user/marjoriebroad)
- [SkillBoss Skill Information](https://skillboss.co/skills/intellectia-stock-forecast)
- [SkillBoss API Hub Endpoint](https://api.skillboss.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python examples; API responses may be JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends ticker queries or analysis prompts to SkillBoss API Hub.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
