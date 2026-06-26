## Description: <br>
Use this skill when the user wants to audit a Binance trading prompt, decide whether an AI trader should get Binance account permissions, return Pass/Warn/Block with guardrails, identify allowed/watch-only/blocked symbols, rewrite the prompt into a safer operating mode, or generate a share card URL for the probation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to audit Binance or crypto trading prompts before granting account permissions. It returns a Pass/Warn/Block style assessment with findings, guardrails, a permission plan, a probation profile, and a safer prompt rewrite when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading prompts are sent to Miraix's public API. <br>
Mitigation: Remove API keys, balances, personal information, proprietary strategy details, and private account data before using the skill. <br>
Risk: Permission recommendations could be mistaken for authorization to enable risky Binance permissions. <br>
Mitigation: Treat permission plans as advisory and require human review before enabling spot, futures, margin, transfer, or withdraw permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richard7463/miraix-binance-agent-firewall) <br>
- [Miraix Binance Agent Firewall audit API](https://app.miraix.fun/api/binance-agent-firewall) <br>
- [Miraix Binance Agent Firewall share image API](https://app.miraix.fun/api/binance-agent-firewall/share-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance derived from API JSON, with optional inline shell command examples and share-card URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include status, safetyScore, verdict, summary, findings, guardrails, permissionPlan, probationProfile, safePrompt, and shareText.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
