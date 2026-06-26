## Description: <br>
Quant Trade helps an agent analyze OKX market candles with RSI, EMA, Bias, and Bollinger Bands, then prepare or execute OKX spot, swap, and futures orders through the OKX CLI when credentials are configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[long778899](https://clawhub.ai/user/long778899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and developers use this skill to give an agent OKX technical-analysis workflows and guarded order-management commands. It is intended for users who deliberately want agent-assisted trading and can choose demo or live profiles before any authenticated action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated OKX commands can affect real funds when the live profile is used. <br>
Mitigation: Start in demo mode, require an explicit live-or-demo profile choice, and review order details before execution. <br>
Risk: Trading credentials may be exposed if pasted into chat or stored too broadly. <br>
Mitigation: Configure credentials locally with the OKX CLI or environment variables, avoid sharing secrets in chat, and use API keys with only the permissions needed. <br>
Risk: Scheduled monitoring or trading workflows can continue running after the user stops actively supervising them. <br>
Mitigation: Avoid leaving the scheduler running unattended with live credentials and stop the process when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/long778899/okx-quant-trade) <br>
- [OKX](https://www.okx.com) <br>
- [OKX market candles API](https://www.okx.com/api/v5/market/candles) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON indicator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OKX CLI commands, credential/profile checks, trading-mode prompts, technical indicator summaries, and scheduler guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
