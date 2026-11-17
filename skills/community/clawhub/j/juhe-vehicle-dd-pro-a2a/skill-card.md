## Description:

Generates a paid pre-purchase vehicle due diligence report from a VIN, vehicle type, and accident or illegal-modification status, covering vehicle configuration, registration details, transfer history, inspection estimate, and masked plate display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External vehicle buyers, vehicle-check agents, financial reviewers, and insurance reviewers use this skill to run a paid VIN-based quick check before purchase or review. It is intended for configuration, registration, transfer-history, and inspection-reference reporting, not valuation, full accident history, theft, lien, violation, insurance quote, or person-vehicle relationship checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to run an unpinned installer that can enable Alipay wallet and payment capabilities.

Mitigation: Review the installer step before use and prefer a pinned, reviewed package version or a trusted managed installation path.

Risk: Using the skill sends VIN and vehicle-type details to Juhe and uses Alipay for payment.

Mitigation: Proceed only after clear user consent to the paid query, data sharing with Juhe, and payment through Alipay.

Risk: Users may overread the report as a valuation, full accident check, theft/lien check, violation report, insurance quote, or buy/sell recommendation.

Mitigation: Keep output limited to returned facts and documented estimates, show the stated exclusions, and avoid deterministic purchase, lending, or insurance conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-vehicle-dd-pro-a2a)
- [Artifact README](artifact/README.md)
- [Product scope](artifact/PRODUCT.md)
- [Output format](artifact/OUT_FORMAT.md)
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with structured tables, concise payment guidance, and inline shell command examples for the agent workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masks returned license plates, blocks incomplete or invalid VIN/type/accident inputs before paid requests, and renders only returned service data.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
