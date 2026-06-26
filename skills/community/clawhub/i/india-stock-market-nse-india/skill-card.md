## Description: <br>
Get India NSE stock market data via FinanceAgent on OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query India NSE stock symbols through the FinanceAgent on OneKey Gateway and receive quote data from the upstream source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a OneKey Gateway API key and uses it in CLI and HTTP requests. <br>
Mitigation: Store DEEPNLP_ONEKEY_ROUTER_ACCESS as a secret, prefer a scoped or low-privilege key when available, and avoid exposing it in logs or shared shell history. <br>
Risk: The connector depends on a third-party gateway and npm package. <br>
Mitigation: Install and run it only in environments where the OneKey/DeepNLP gateway and @aiagenta2z/onekey-gateway package are trusted. <br>
Risk: The curl example uses verbose mode, which can reveal request details in captured logs. <br>
Mitigation: Remove -v when running the HTTP example in environments with retained or shared logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/india-stock-market-nse-india) <br>
- [DeepNLP OneKey Agent Router endpoint](https://agent.deepnlp.org/agent_router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and a symbol_list array; returned quote fields depend on the upstream data source.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
