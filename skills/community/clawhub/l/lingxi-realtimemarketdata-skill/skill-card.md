## Description: <br>
国泰海通证券-灵犀实时行情 helps agents retrieve authenticated real-time market data for A-shares, Hong Kong stocks, U.S. stocks, ETFs, and indices, including latest price, price change, volume, turnover, turnover rate, capital inflow, and volume ratio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtht-tech](https://clawhub.ai/user/gtht-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer securities market-data questions with authenticated real-time quotes. It is suited for stock price, movement, comparison, and capital-flow queries where the agent must use the configured market-data tool and avoid fabricating unavailable data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials for authenticated market-data calls and stores an API key locally in a shared JSON file. <br>
Mitigation: Install only after verifying the publisher and GTJA/GTHT relationship; prefer the QR authorization flow and limit access to the local credential file. <br>
Risk: Financial market-data responses may be mistaken for investment advice. <br>
Mitigation: Use the skill for objective quote data only and preserve the required disclaimer that generated content is not investment advice. <br>
Risk: Unavailable or failed market-data calls could lead to unsupported answers if the agent improvises. <br>
Mitigation: Follow the documented fallback path and use the fixed no-data response when the configured skills cannot provide valid data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gtht-tech/lingxi-realtimemarketdata-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gtht-tech) <br>
- [GTHT API key authorization activity](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1) <br>
- [Market data gateway](https://zx.app.gtja.com:8443/mcp/marketdata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline node commands and structured market-data fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QR or API-key authorization before market-data calls; stores the API key locally for later authenticated requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
