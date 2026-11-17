## Description:

DACHSER (dachser.com). Use this skill for ANY DACHSER request — searching and reading data. Whenever a task involves DACHSER, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Logistics and support teams can use this skill to look up delivery-order status, current shipment status, and shipment event history through a connected DACHSER account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the setup fallback can run an unverified remote installer that may affect other installed agent skills.

Mitigation: Review and explicitly approve the CLI installation before allowing the fallback, check its effects on other installed agent skills, and note that OOMOL mediates access to the DACHSER account.

## Reference(s):

- [DACHSER](https://www.dachser.com/)
- [DACHSER API documentation](https://api-portal.dachser.com/bi.b2b.portal/api/information)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured JSON results with shipment or delivery-order status and history, presented as text when summarized.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookup results; requires the oo CLI and a connected DACHSER account.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
