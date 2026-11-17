## Description:

Provides natural-language A-share stock screening across market, financial, valuation, and technical indicators, and can run historical backtests for screening conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtht-tech](https://clawhub.ai/user/gtht-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to screen A-share stocks with natural-language criteria and request historical backtests of screening conditions. Outputs are informational and must not be treated as investment advice or a promise of future returns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable API key may be stored locally in plaintext.

Mitigation: Use the skill only on trusted machines and clear or revoke the API key when the workspace or machine is shared.

Risk: Mutable gateway configuration or GTHT_GATEWAY_CONFIG can redirect service requests.

Mitigation: Review gateway-config.json and the GTHT_GATEWAY_CONFIG environment variable before using the skill.

Risk: Stock-screening and backtest outputs may be mistaken for investment advice.

Mitigation: Keep the required disclaimers in user-facing responses and treat results as informational data, not trading recommendations or performance promises.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtht-tech/skills/lingxi-smartstockselection-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/gtht-tech)
- [Lingxi app API key page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1)
- [Junhong app API key page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=junhong&webEnv=web2&isyyzshare=1)
- [Financial screening gateway](https://zx.app.gtja.com:8443/mcp/lingxi/financial)
- [Backtest gateway](https://zx.app.gtja.com:8443/mcp/lingxi/backtest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline command examples and JSON tool results from MCP calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API key authorization; stock-screening and backtest outputs must include the skill's non-investment-advice disclaimers.]

## Skill Version(s):

1.11.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
