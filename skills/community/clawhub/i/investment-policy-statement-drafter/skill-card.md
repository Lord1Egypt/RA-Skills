## Description:

Use this skill when an IAR, CFP practitioner, trust officer, or ERISA fiduciary needs to draft an Investment Policy Statement for an individual, trust, plan, or endowment client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External financial professionals use this skill to draft a review-ready Investment Policy Statement from client facts, objectives, constraints, fiduciary context, and source documents. It is intended to support professional compliance review, not to provide investment advice or make portfolio decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive financial planning facts or client context.

Mitigation: Use non-identifying client codes and redact Social Security numbers, full account numbers, taxpayer IDs, dates of birth, government IDs, custodian logins, and similar direct identifiers.

Risk: A draft IPS could be mistaken for final investment advice or an approved client document.

Mitigation: Keep outputs clearly labeled as drafts and require review, editing, and approval by the adviser, fiduciary, compliance function, and client or plan fiduciary before signature or use.

Risk: The document could include unsupported investment assumptions, product recommendations, or execution instructions.

Mitigation: Limit the output to policy-level drafting, avoid specific securities or managers, avoid orders and guarantees, and preserve unresolved information for professional follow-up.

Risk: Backdated or signed language could create compliance and recordkeeping risk.

Mitigation: Decline backdating, keep sign-off blocks unsigned, and require the responsible professional to complete records through approved firm procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/investment-policy-statement-drafter)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft document with structured intake, tables, self-checks, and sign-off blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a draft IPS for fiduciary and client review; requires redacted client identifiers and professional compliance review before use.]

## Skill Version(s):

0.1.1 (source: server release evidence and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
