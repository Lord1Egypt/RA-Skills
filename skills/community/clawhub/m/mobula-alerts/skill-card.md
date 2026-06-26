## Description: <br>
24/7 autonomous monitoring for crypto portfolios, whales, and market conditions. Multi-condition alerts via OpenClaw heartbeat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flotapponnier](https://clawhub.ai/user/flotapponnier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External crypto users, portfolio managers, and traders use this skill to configure an agent for continuous crypto portfolio, wallet, token, and market monitoring. It supports threshold alerts, whale watching, token discovery, and scheduled market briefs through heartbeat-driven checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, holdings, and portfolio alerts can reveal sensitive financial activity. <br>
Mitigation: Use private alert channels and avoid sending full wallet addresses or exact holdings unless they are necessary for the monitoring task. <br>
Risk: The skill requires a Mobula API key for monitoring workflows. <br>
Mitigation: Protect MOBULA_API_KEY as a secret and avoid exposing it in prompts, logs, screenshots, or shared alert output. <br>
Risk: Heartbeat monitoring can keep checking conditions and sending alerts after setup. <br>
Mitigation: Confirm how to disable heartbeat tasks before enabling 24/7 alerts, and tune monitoring frequency to the intended use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/flotapponnier/mobula-alerts) <br>
- [Mobula homepage](https://mobula.io) <br>
- [Mobula API documentation](https://docs.mobula.io) <br>
- [Mobula OpenClaw repository](https://github.com/Flotapponnier/Crypto-date-openclaw) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with alert templates, setup commands, and monitoring pattern examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOBULA_API_KEY and may describe heartbeat schedules, wallet or token monitoring criteria, and notification-channel setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
