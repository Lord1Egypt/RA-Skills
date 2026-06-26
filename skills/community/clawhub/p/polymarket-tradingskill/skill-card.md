## Description: <br>
Use when an OpenClaw user needs fast NBA opportunity scanning, NBA-only /fair pricing, or deep analysis of one specific Polymarket market or event in any domain, including politics, via prompts like /analyze, analyze this market, or direct PM URLs, without making the final trading decision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a1594834522-coder](https://clawhub.ai/user/a1594834522-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to scan NBA and basic soccer markets, analyze specific Polymarket events or markets, and organize pricing signals for human review. It provides decision support only and does not execute trades, manage wallets, or make final buy/sell decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be routed to the skill automatically when market-analysis intent is detected. <br>
Mitigation: Review routed requests and confirm the intended market or scan scope before relying on the output. <br>
Risk: The skill requires a configured OpenClaw agent API base URL and bearer token. <br>
Mitigation: Use a trusted API endpoint and a least-privilege read-only API key managed outside prompts and responses. <br>
Risk: Pricing and priority labels can be mistaken for trading instructions. <br>
Mitigation: Treat outputs as decision support and keep final trading decisions with the user or a separate execution layer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a1594834522-coder/polymarket-tradingskill) <br>
- [OpenClaw Decision-Support API Quick Reference](references/agent-api.md) <br>
- [Decision-Support Contract](references/decision-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON-like analysis blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are compact decision-support summaries, opportunity shortlists, pricing views, and risk notes; they are not trading instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
