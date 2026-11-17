## Description:

Shop autonomously on Amazon via Moltpho - search products, manage credit, and purchase items using mUSD on Base mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unifiedh](https://clawhub.ai/user/unifiedh)

### License/Terms of Use:


## Use Case:

External users and their agents use Moltpho to search Amazon products, manage credit-backed purchasing, update shipping profiles, and place orders through a Moltpho account using mUSD on Base mainnet.

### Deployment Geography for Use:

United States (US shipping addresses only)

## Known Risks and Mitigations:

Risk: The skill can spend funds and place real-world orders using stored Moltpho credentials.

Mitigation: Enable order confirmations, review totals before purchase, and set tight per-order and daily caps in the portal.

Risk: Proactive purchasing can act on inferred needs without a direct purchase request.

Mitigation: Turn off proactive purchasing unless this behavior is explicitly desired, and restrict categories and caps before enabling it.

Risk: Local credentials can authorize purchases if the machine or credentials file is exposed.

Mitigation: Protect the credentials file, avoid shared-machine installs, and rotate or delete credentials after suspected compromise.

Risk: Shipping-profile updates and payment setup involve sensitive personal or financial information.

Mitigation: Prefer the Moltpho portal for sensitive setup, and do not provide card numbers, passwords, or unnecessary personal data in chat.

## Reference(s):

- [Moltpho Skill Page](https://clawhub.ai/unifiedh/skills/moltpho)
- [Moltpho API Reference](references/API.md)
- [Moltpho Purchasing Policies](references/POLICIES.md)
- [Moltpho API](https://api.moltpho.com/v1)
- [Moltpho Portal](https://portal.moltpho.com)

## Skill Output:

**Output Type(s):** [Text, API Calls, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON API payloads and Python helper calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open a browser portal and make authenticated HTTPS requests for registration, account setup, catalog search, shipping profile updates, quotes, x402 signing, orders, and support tickets.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
