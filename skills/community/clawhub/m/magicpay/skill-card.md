## Description: <br>
Handle approved login, identity, checkout, donation, subscription, payment pages, and typed action approvals through the magicpay CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xor777](https://clawhub.ai/user/xor777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use MagicPay to guide approved login, identity, checkout, donation, subscription, payment, wallet, and other sensitive browser workflows while keeping stored Memory values out of the agent prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MagicPay supports high-impact payment, wallet, login, browser-session, and saved-profile workflows. <br>
Mitigation: Use it only on trusted machines and require matching typed approval before protected actions such as payment, login, identity submission, wallet signing, account changes, or final form submission. <br>
Risk: API keys, OTPs, CDP endpoints, saved profile data, and Memory references can expose sensitive authority if shared in prompts, logs, or reports. <br>
Mitigation: Keep MAGICPAY_API_KEY, local config, OTP digits, CDP endpoints, Memory refs, payment card data, wallet private keys, and passwords out of chat, logs, summaries, and external tools. <br>
Risk: Stored Memory or payment values could be exposed or misused if the agent bypasses the value-free planning flow. <br>
Mitigation: Use plan-fill and apply-fill for Memory work, do not pass raw Memory values or materializers through the agent, and collect payment authorization before provider-backed card handles are revealed. <br>
Risk: A stale or unapproved browser/session can cause fills or approvals to target the wrong page or authority boundary. <br>
Mitigation: Start a MagicPay workflow session before launch or attach, use only an approved private browser or CDP endpoint, rerun planning after page changes, and observe the result page before claiming success. <br>


## Reference(s): <br>
- [MagicPay on ClawHub](https://clawhub.ai/xor777/magicpay) <br>
- [MagicPay CLI package](https://www.npmjs.com/package/@mercuryo-ai/magicpay-cli) <br>
- [MagicPay OpenClaw marketplace README](https://github.com/MercuryoAI/skills/blob/main/docs/magicpay/openclaw/marketplace/README.md) <br>
- [MagicPay workflow guide](https://github.com/MercuryoAI/skills/blob/main/docs/magicpay/references/workflow.md) <br>
- [MagicPay command guide](https://github.com/MercuryoAI/skills/blob/main/docs/magicpay/references/commands.md) <br>
- [MagicPay result states](https://github.com/MercuryoAI/skills/blob/main/docs/magicpay/references/statuses.md) <br>
- [MagicPay guardrails](https://github.com/MercuryoAI/skills/blob/main/docs/magicpay/references/guardrails.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the magicpay CLI, MAGICPAY_API_KEY, and an approved browser or private CDP session for browser-dependent workflows.] <br>

## Skill Version(s): <br>
0.1.41 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
