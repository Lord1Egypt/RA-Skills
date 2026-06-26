## Description: <br>
Real-time Pump.fun token alerts for Solana traders, trading bots, Discord, Telegram, and AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NextFrontierBuilds](https://clawhub.ai/user/NextFrontierBuilds) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and trading automation builders use this skill to fetch and watch Pump.fun bonding and graduation token alerts from the PRISM API for chat bots, agent workflows, and alerting pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watch mode continuously polls an external cryptocurrency API. <br>
Mitigation: Use a trusted PRISM endpoint, keep polling intervals conservative, and review API behavior before using results in production workflows. <br>
Risk: Alert output can be connected to Telegram, Discord, trading, or public posting workflows. <br>
Mitigation: Scope bot tokens to the intended channel and require review before connecting alerts directly to trading or public posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NextFrontierBuilds/prism-alerts) <br>
- [Default PRISM API endpoint](https://strykr-prism.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text alert output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output depends on the configured PRISM API endpoint and live token data.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
