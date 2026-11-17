## Description:

End-to-end stablecoin payments for links, invoices, receipts, and dashboards across Telegram, WhatsApp, and Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofuzorchukwuemeke](https://clawhub.ai/user/ofuzorchukwuemeke)

### License/Terms of Use:

MIT

## Use Case:

External users, merchants, developers, and agents use this skill to create and track USDC payment links, invoices, fundraising campaigns, customer data collection, and payment dashboards through Obverse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests payment API authority through OBVERSE_API_KEY.

Mitigation: Use a narrowly scoped Obverse API key and rotate it if it is exposed.

Risk: Dashboard passwords may appear in normal agent output.

Mitigation: Do not share generated dashboard credentials in group chats or logs; treat them as short-lived secrets.

Risk: Payment links can collect customer or contributor data.

Mitigation: Collect personal data only with clear consent, purpose, and retention expectations.

Risk: OBVERSE_API_URL can be overridden.

Mitigation: Override OBVERSE_API_URL only for trusted HTTPS endpoints or controlled local development.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ofuzorchukwuemeke/skills/obverse-payments)
- [Obverse Homepage](https://www.obverse.cc)
- [Obverse API Key Registration](https://obverse.onrender.com/api-keys/register)
- [Obverse API Documentation](https://obverse.onrender.com/api-docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown and JSON-style payment or status summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OBVERSE_API_KEY; outputs can include payment URLs, dashboard credentials, customer or contributor data, wallet balances, and transaction status.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact manifests list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
