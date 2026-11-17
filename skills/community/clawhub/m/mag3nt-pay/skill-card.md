## Description:

Pay for APIs and services, receive payments, and manage agent wallets using Mag3nt USDC virtual cards. Activate when the agent needs to pay for a resource, encounters an HTTP 402 response, a payment challenge header (x402, MPP, Pay Link), needs to issue or verify an AP2 payment mandate, check wallet balance, or set up payment credentials for autonomous transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mag3nt](https://clawhub.ai/user/mag3nt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous-agent operators use this skill to let an agent pay for protected APIs or services, settle payment challenges, issue or verify AP2 mandates, and check Mag3nt card balances before spending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend real funds through Mag3nt payment credentials and autonomous payment flows.

Mitigation: Use limited-balance cards, prefer test credentials where possible, and require explicit confirmation of recipient, amount, and merchant domain before payment or mandate creation.

Risk: Payment credentials or sensitive request data could be exposed if forwarded too broadly.

Mitigation: Keep Mag3nt credentials in the local environment and avoid forwarding Authorization headers, Cookie headers, or sensitive request bodies unless they are required for the specific payment flow.

Risk: The agent could settle the wrong payment challenge when multiple methods or protocols are offered.

Mitigation: Check balance first, inspect the challenge for supported methods, confirm the selected protocol and amount, and log transaction ID plus on-chain transaction hash as charge evidence.

## Reference(s):

- [Mag3nt Pay ClawHub Release](https://clawhub.ai/mag3nt/skills/mag3nt-pay)
- [Mag3nt Website](https://mag3nt.com)
- [Setup](references/setup.md)
- [Balance](references/balance.md)
- [Universal Pay](references/x402-pay.md)
- [MPP Pay](references/mpp-pay.md)
- [Pay Link Settlement](references/paylink-pay.md)
- [AP2 Pay](references/ap2-pay.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, HTTP request examples, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform API calls when the agent follows the skill with configured Mag3nt credentials.]

## Skill Version(s):

1.0.5 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
