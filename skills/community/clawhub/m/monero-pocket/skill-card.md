## Description:

Ripley Pocket For Monero helps agents use the Ripley Pocket API to register accounts, check XMR balances, make Monero and XMR402 payments, withdraw XMR, and manage cross-chain swaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbtoshi](https://clawhub.ai/user/xbtoshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to integrate AI agents with Ripley Pocket for API-key authenticated crypto payments, Monero balance checks, transaction history, withdrawals, swaps, and XMR402 payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes broad activation language and payment helper examples that could cause an agent to spend funds without clear user approval or limits.

Mitigation: Require explicit manual approval before every payment, withdrawal, swap, or XMR402 payment, and enforce spend limits outside the skill.

Risk: Misuse or exposure of the Ripley Pocket API key could allow unauthorized balance access or payment actions.

Mitigation: Keep API_KEY scoped and protected, avoid exposing it in prompts or logs, and rotate it if compromise is suspected.

Risk: Crypto payments, withdrawals, and swaps may be irreversible after submission.

Mitigation: Verify destination addresses, currencies, networks, amounts, and trusted-domain allowlists before authorizing transactions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xbtoshi/skills/monero-pocket)
- [Ripley Pocket API gateway](https://pocket.ripley.run)
- [XMR402 protocol](https://xmr402.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl, Python, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API requests that require RIPLEY_URL and API_KEY configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
