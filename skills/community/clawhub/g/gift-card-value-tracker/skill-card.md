## Description:

Use when managing a drawer of gift cards, deciding whether to spend or sell one, checking dormancy fees and expiry law (US CARD Act), or when a card's retailer files bankruptcy — balance registry, decay math, resale cash-out verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Individuals managing gift cards can record balances and dates, review dormancy and expiry concerns, compare resale offers they provide, and prioritize cards when a retailer shows signs of distress.

### Deployment Geography for Use:

United States (primary; brief notes for the EU, UK, and Canada)

## Known Risks and Mitigations:

Risk: A plaintext registry could expose balances or card identifiers.

Mitigation: Store only balances, dates, and last four digits; keep the registry in a dedicated, secured file and back it up.

Risk: Dormancy, expiry, bankruptcy, and resale estimates may not match issuer terms, current offers, or local rules.

Mitigation: Check issuer terms and current local rules before acting on estimates, and compare live resale offers.

Risk: Runtime host permissions have not been verified.

Mitigation: Review the execution environment's permissions before enabling the skill.

## Reference(s):

- [Gift Cards — Decay Law, Bankruptcy, and Resale Economics](references/decay-bankruptcy-resale.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON, Shell commands]

**Output Format:** [Text recommendations and summaries, optional shell commands, and a local JSON gift-card registry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses card details and resale offers supplied by the user; does not access accounts or move money.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
