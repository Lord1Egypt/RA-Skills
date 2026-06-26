## Description: <br>
Opinion Skill provides Bun-based tools for querying Opinion prediction markets, inspecting market data, and preparing wallet-backed trading actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yuandiaodiaodiao](https://clawhub.ai/user/Yuandiaodiaodiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to help users search Opinion prediction markets, inspect prices, order books, balances, positions, orders, and trade history, and run guided buy, sell, cancel, or enable-trading commands when wallet credentials are intentionally configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live wallet-backed financial actions, including buying, selling, cancelling orders, and enabling trading. <br>
Mitigation: Use a dedicated low-balance wallet and require manual confirmation before every buy, sell, cancel-all, or enable-trading action. <br>
Risk: Trading scripts require sensitive wallet and API credentials in environment configuration. <br>
Mitigation: Avoid main-wallet private keys, protect the .env file, and inspect or pin the skill code and dependencies before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Yuandiaodiaodiao/opinion-skill) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/Yuandiaodiaodiao) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON-capable script outputs for market data, balances, orders, positions, and trade history.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
