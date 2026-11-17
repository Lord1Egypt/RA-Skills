## Description:

Provides AI agents with paid API calls for sanctions screening, KYB/KYC, AML, OFAC and PEP watchlist checks, PASS/WARN/BLOCK verdicts, and entity risk scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to screen customers, vendors, counterparties, wallets, domains, or legal names before onboarding, payments, contracting, or transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive person, company, domain, or wallet identifiers are sent to a third-party API.

Mitigation: Use the skill only with a lawful basis and privacy review, and avoid confidential or regulated data unless third-party processing is approved.

Risk: The skill describes automatic USDC payments per request without clear in-skill consent or spending controls.

Mitigation: Require explicit approval for each screening run and set wallet spending limits or budgets outside the skill before use.

Risk: Periodic monitoring can create repeated paid requests.

Mitigation: Enable monitoring only with a defined cadence, budget, and stop condition.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinhughes2121/skills/gocreative-compliance)
- [Publisher profile](https://clawhub.ai/user/colinhughes2121)
- [GoCreative API](https://api.gocreativeai.com)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, JSON]

**Output Format:** [JSON responses with concise compliance decisions and supporting screening details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PASS/WARN/BLOCK verdicts, sanctions or PEP matches, KYB dossiers, vendor risk data, and 0-100 entity risk scores.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
