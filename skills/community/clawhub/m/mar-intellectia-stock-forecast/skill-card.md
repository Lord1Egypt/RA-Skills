## Description:

Provides single-symbol stock and crypto forecasts and buy/sell/hold analysis through the SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request single-ticker stock or crypto forecasts and structured investment Q&A. It helps an agent call SkillBoss API Hub endpoints for forecast searches and buy/sell/hold analysis while presenting results as informational guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an API key and stock-analysis prompts to SkillBoss API Hub.

Mitigation: Install only if you trust SkillBoss with the submitted prompts and protect SKILLBOSS_API_KEY in a constrained environment.

Risk: Forecasts and buy/sell/hold analysis can be incorrect, stale, or unsuitable for financial decisions.

Mitigation: Treat results as informational only and verify important decisions with licensed market data and qualified financial advice.

Risk: The Python example depends on the requests package from the package ecosystem.

Mitigation: Use a constrained environment and pin dependencies when stricter supply-chain control is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-intellectia-stock-forecast)
- [Publisher profile](https://clawhub.ai/user/marjoriebroad)
- [SkillBoss skill information](https://skillboss.co/skills/intellectia-stock-forecast)
- [SkillBoss API Hub pilot endpoint](https://api.skillboss.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and Python examples; API responses may be JSON or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; results are informational and may not be real-time.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
