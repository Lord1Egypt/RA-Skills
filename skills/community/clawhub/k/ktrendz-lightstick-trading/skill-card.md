## Description: <br>
Trade K-pop artist lightstick tokens using bonding curve prices, real-time signals, and news to buy or sell with a $100 daily limit and fee structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hans1329](https://clawhub.ai/user/hans1329) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents with a K-Trendz API key use this skill to configure access, check token prices and signals, and execute one-token buy or sell actions on the K-Trendz bonding curve market. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute live buy and sell transactions without a built-in confirmation step. <br>
Mitigation: Confirm the artist, action, estimated cost or refund, fees, and slippage before running any buy or sell command. <br>
Risk: The skill stores or uses a K-Trendz API key for trading access. <br>
Mitigation: Use only if you trust K-Trendz with the API key, protect the saved configuration file, and remove it when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hans1329/ktrendz-lightstick-trading) <br>
- [K-Trendz bot API](https://k-trendz.com/api/bot/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a K-Trendz API key; buy and sell commands execute live token trades.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
