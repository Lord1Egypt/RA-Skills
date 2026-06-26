## Description: <br>
智能盯盘 helps an agent create market watch alerts for A-shares, Hong Kong stocks, and cryptocurrencies when user-defined price or percentage conditions are met. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingyv](https://clawhub.ai/user/lingyv) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to translate explicit market-monitoring requests into watch parameters, notification channels, and reminder behavior for supported A-share, Hong Kong stock, and cryptocurrency targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends watch requests, tokens, and optional email or phone alert details to an external WebSocket service. <br>
Mitigation: Use only after reviewing the backend destination, supplying a narrowly scoped token, and confirming the user wants any email or phone notification channel. <br>
Risk: The artifact uses an unencrypted ws:// bridge address for watch-monitoring traffic. <br>
Mitigation: Switch the bridge to encrypted wss:// before using real credentials, personal contact data, or sensitive watch requests. <br>
Risk: Market alerts can be misleading if required product codes, market types, conditions, or threshold variables are guessed. <br>
Mitigation: Confirm productCode, productType, condition, and variables with the user before creating a watch request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingyv/glance-watch) <br>
- [Publisher profile](https://clawhub.ai/user/lingyv) <br>
- [Market reference](references/markets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces watch setup guidance, required alert parameters, channel configuration, and failure-handling instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
