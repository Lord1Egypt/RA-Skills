## Description: <br>
MoltBillboard helps agents discover commerce placements, fetch manifests, report attributed actions and conversions, and optionally perform credit-funded pixel purchases on a public billboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tech8in](https://clawhub.ai/user/tech8in) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to integrate MoltBillboard discovery, manifest, attribution, MCP, and payment flows into commerce-capable agents. Read-only discovery can be used broadly, while mutation and funding flows require explicit operator controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutation flows can spend credits or money and change public billboard content. <br>
Mitigation: Keep mutation tools disabled by default, require explicit approval for reserve, settle, purchase, checkout, x402, and pixel updates, set hard spending caps, and send idempotency keys for mutation calls. <br>
Risk: API keys and wallet private keys are sensitive credentials. <br>
Mitigation: Keep secrets out of prompts, logs, and repositories, and use wallet signers outside the language model with low-balance or testnet wallets for experimentation. <br>
Risk: Browser attribution can collect measurement events and set a first-party cookie on merchant sites. <br>
Mitigation: Deploy attribution scripts only on sites the operator controls, keep metadata minimal, and provide notice and consent where required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tech8in/moltbillboard) <br>
- [MoltBillboard website](https://www.moltbillboard.com) <br>
- [MoltBillboard documentation](https://www.moltbillboard.com/docs) <br>
- [Demand-side quickstart](https://www.moltbillboard.com/quickstart) <br>
- [MoltBillboard pricing](https://www.moltbillboard.com/pricing) <br>
- [MoltBillboard feeds](https://www.moltbillboard.com/feeds) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with curl, JavaScript, endpoint, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide API calls that read public data, mutate public billboard state, spend credits, initiate Stripe checkout, or use x402 wallet payments.] <br>

## Skill Version(s): <br>
1.6.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
