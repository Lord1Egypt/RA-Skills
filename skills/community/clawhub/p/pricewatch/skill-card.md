## Description: <br>
Monitors competitor prices across Amazon, Walmart, Shopify, and Etsy with AI-driven normalization, alerts, and historical trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juntinglu-229](https://clawhub.ai/user/juntinglu-229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and ecommerce teams use this skill to monitor competitor product URLs, track historical price changes, and receive configurable alerts or market reports for pricing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scrapes product URLs from user watchlists and may send product names, platforms, prices, percent changes, and recommendations to configured Slack or Telegram services. <br>
Mitigation: Use trusted watchlists, restrict monitored URLs in sensitive environments, and configure only approved notification services. <br>
Risk: Price extraction depends on third-party ecommerce page structure and can be inaccurate, blocked, or out of date. <br>
Mitigation: Review important alerts before pricing decisions, keep rate limits enabled, and manually verify high-impact price changes. <br>


## Reference(s): <br>
- [ClawHub PriceWatch listing](https://clawhub.ai/juntinglu-229/pricewatch) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Configuration example](artifact/scripts/config.example.yaml) <br>
- [PriceWatch monitoring script](artifact/scripts/price_watch.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration, shell commands, and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores price history locally in SQLite and can send configured Slack or Telegram alert payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
