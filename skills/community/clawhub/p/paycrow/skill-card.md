## Description: <br>
PayCrow helps agents query PayCrow's hosted Trust API for Ethereum wallet trust scores before payments and describes separate escrow protection available through a PayCrow MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michu5696](https://clawhub.ai/user/michu5696) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use PayCrow to check a counterparty wallet's trust score before paying for an API or service and to decide whether to proceed, reduce the amount, or avoid payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses queried through the trust check are sent to PayCrow's hosted API. <br>
Mitigation: Only query wallet addresses you are comfortable sending to PayCrow, and avoid treating the score as private local analysis. <br>
Risk: Trust scores and recommendations are advisory and do not prove that a payment or escrow interaction is safe. <br>
Mitigation: Review the counterparty, MCP server installation, wallet permissions, spending limits, and contract behavior before enabling escrow or payment tools. <br>


## Reference(s): <br>
- [PayCrow ClawHub listing](https://clawhub.ai/michu5696/paycrow) <br>
- [PayCrow Trust API](https://paycrow-app.fly.dev) <br>
- [PayCrow npm package](https://www.npmjs.com/package/paycrow) <br>
- [PayCrow Base contract](https://basescan.org/address/0xDcA5E5Dd1E969A4b824adDE41569a5d80A965aDe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with a curl command and trust-score interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides advisory trust-check guidance and does not embed credentials, persist data, or directly authorize payments.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
