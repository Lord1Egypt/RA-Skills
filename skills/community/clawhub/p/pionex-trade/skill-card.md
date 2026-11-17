## Description:

Use when an agent needs to place or cancel Pionex spot orders and review open orders or fills through the `pionex-trade-cli` CLI with configured API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pibrandon](https://clawhub.ai/user/pibrandon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage Pionex spot trading workflows, including placing market or limit orders, cancelling orders, and checking order status or fills. It is not intended for market-data-only or portfolio-only requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an external Pionex CLI package and uses trading API credentials.

Mitigation: Install only if the Pionex npm package source is trusted, use a dedicated API key with only needed spot-trading permissions, disable withdrawals, and consider IP allowlisting.

Risk: Order placement and cancellation can affect real trading positions.

Mitigation: Use dry-runs where supported, confirm proposed writes with the user before live execution, and do not increase order size or submit additional orders without explicit agreement.

## Reference(s):

- [Pionex API Docs](https://pionex-doc.gitbook.io/apidocs/)
- [Pionex Homepage](https://www.pionex.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run trading commands, confirmation prompts, balance checks, and order-management guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
