## Description: <br>
Solana trading skill for AI agents to buy, sell, and create tokens across PumpFun, PumpSwap, LaunchLab, and Meteora. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qualitydude](https://clawhub.ai/user/qualitydude) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to connect an AI agent to PLUGy for Solana wallet registration, token trading, token creation, balance checks, and optional autonomous trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent fund-controlling Solana trading authority while handling wallet secrets and API keys. <br>
Mitigation: Use small funds, require manual approval for trades, avoid unbounded autonomous mode, and store credentials in a secure secret manager instead of chat, agent memory, or plain local files. <br>
Risk: The skill relies on mutable remote TRADE, CREATE, HEARTBEAT, and RULES files from plugy.fun. <br>
Mitigation: Inspect the remote files before use, only send the PLUGy API key to https://plugy.fun/api endpoints, and refuse requests to share credentials with any other domain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qualitydude/plugy) <br>
- [PLUGy website](https://plugy.fun) <br>
- [PLUGy docs](https://plugy.fun/docs) <br>
- [PLUGy trade instructions](https://plugy.fun/trade.md) <br>
- [PLUGy token creation instructions](https://plugy.fun/create.md) <br>
- [PLUGy security rules](https://plugy.fun/rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with curl examples, endpoint descriptions, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PLUGy API key and may handle wallet credentials and fund-moving trading requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
