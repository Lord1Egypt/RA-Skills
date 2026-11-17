## Description:

Find the cheapest way to send money between any two currencies. Compares 22+ crypto exchanges and 19 remittance providers in real-time. Free, open source, no affiliate fees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miguelvalenciav](https://clawhub.ai/user/miguelvalenciav)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use Money Router to compare cross-border money transfer routes by amount and currency pair. It returns ranked route guidance with costs, rates, provider paths, estimated timing, and verification-related actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification and quest features may send provider, currency pair, observed rate, and fee information to Coinnect.

Mitigation: Avoid submitting personal account details or transaction identifiers unless the service explicitly requests them and the user is comfortable sharing them.

Risk: Quoted rates, fees, provider availability, and transfer timing can change before a transfer is completed.

Mitigation: Verify the final rate, fee, recipient amount, and delivery estimate directly with the selected provider before initiating a transaction.

## Reference(s):

- [Money Router on ClawHub](https://clawhub.ai/miguelvalenciav/skills/money-router)
- [Coinnect homepage](https://coinnect.bot)
- [Coinnect API docs](https://coinnect.bot/docs)
- [Coinnect whitepaper](https://coinnect.bot/whitepaper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with API endpoint examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked route details, fee and exchange-rate summaries, provider paths, estimated delivery time, and step-by-step transfer guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
