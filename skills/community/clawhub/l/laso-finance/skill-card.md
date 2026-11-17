## Description:

Order prepaid cards, gift cards, and send money to USD/EUR/GBP debit cards or US bank accounts using USDC on Base or Solana via the x402 protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huntermonk](https://clawhub.ai/user/huntermonk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to spend USDC through Laso Finance for online checkout, gift card and prepaid card purchases, debit or bank payouts, balance checks, and x402 payment-required flows.

### Deployment Geography for Use:

Global, with rail-specific restrictions described by the skill: U.S. cards and USD push-to-card are U.S.-oriented, EUR push-to-card is Eurozone-oriented, GBP push-to-card is U.K.-oriented, and some payout flows may require account-owner verification.

## Known Risks and Mitigations:

Risk: The skill enables real purchases, payouts, transfers, withdrawals, banking changes, webhook registration, and external x402 payments.

Mitigation: Require explicit user confirmation before each money movement, account change, webhook registration, or external x402 payment.

Risk: The skill asks agents to keep durable financial-account credentials across sessions.

Mitigation: Store secrets only in an approved secret manager or an owner-protected local credentials file, never in repositories, prompts, logs, or shared instruction files.

Risk: The skill recommends installing or refreshing live skill text from Laso Finance URLs.

Mitigation: Verify the downloaded skill and docs version before installing or updating a persistent local copy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huntermonk/skills/laso-finance)
- [Laso Finance homepage](https://laso.finance)
- [Laso Finance docs version beacon](https://laso.finance/.well-known/docs-version.json)
- [Laso Finance skill discovery index](https://laso.finance/.well-known/skills/index.json)
- [Laso Finance agent skills discovery index](https://laso.finance/.well-known/agent-skills/index.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, HTTP examples, JSON examples, and workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to call external payment, banking, wallet, authentication, webhook, and account-management endpoints when the user authorizes those actions.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
