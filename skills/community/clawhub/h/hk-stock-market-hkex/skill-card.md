## Description: <br>
Get HKEX (Hong Kong Stock Exchange) market data via FinanceAgent on OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query HKEX stock symbols through the OneKey Gateway FinanceAgent and receive market quote data for integration into workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HKEX symbols and requests are sent to the external OneKey/DeepNLP gateway service. <br>
Mitigation: Use the skill only when that gateway is trusted for the data being queried. <br>
Risk: The skill requires a OneKey Gateway API key. <br>
Mitigation: Use a dedicated key where possible and avoid exposing it in logs, shared terminals, or shell history. <br>
Risk: Runtime behavior depends on the @aiagenta2z/onekey-gateway npm package and upstream market-data service. <br>
Mitigation: Review the package and gateway availability before relying on the skill in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/hk-stock-market-hkex) <br>
- [DeepNLP OneKey Agent Router endpoint](https://agent.deepnlp.org/agent_router) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a OneKey Gateway API key and returns JSON quote results from the external gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
