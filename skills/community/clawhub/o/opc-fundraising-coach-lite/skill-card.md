## Description:

A Chinese-first business canvas assistant that helps entrepreneurs and one-person or small teams turn a plain-language startup idea into a structured Business Model Canvas, investor-oriented BP outline, and concise diagnostic summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monsterdt](https://clawhub.ai/user/monsterdt)

### License/Terms of Use:

MIT-0

## Use Case:

External entrepreneurs, founders, and small teams use this skill to structure early business ideas into a Business Model Canvas, identify gaps, and produce a BP skeleton for pitch preparation. It is intended for general business-planning support, not legal, investment, or personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for non-public startup financial, valuation, runway, investor, or term-sheet information.

Mitigation: Avoid entering confidential details unless the host retention behavior is clear and the user intentionally wants that information used or stored.

Risk: The artifact gives inconsistent signals about whether founder profile information is session-only or may be retained as a workspace file.

Mitigation: Confirm storage expectations before writing or preserving session profiles, and omit sensitive fields when persistence is not required.

Risk: Business-plan and fundraising suggestions may be mistaken for legal, investment, or personalized financial advice.

Mitigation: Treat outputs as general educational planning support and seek qualified professional review before formal fundraising, legal, or investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monsterdt/skills/opc-fundraising-coach-lite)
- [BP coaching reference](references/bp-coaching.md)
- [Business Model Canvas template](assets/business-model-canvas-template.md)
- [BP framework template](assets/bp-framework-template.md)
- [Session profile template](assets/session-profile-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversation output with structured canvas sections, BP outline headings, checklists, and short diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session-profile details if the user provides startup, financial, fundraising, or investor information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
