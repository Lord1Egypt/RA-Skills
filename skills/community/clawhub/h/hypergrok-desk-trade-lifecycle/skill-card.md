## Description:

The end-to-end procedure for one trade on the HyperGrok desk - from an idea to a reviewed, journaled result - with the ticket format, who owns each stage, and what "done" looks like. Use whenever the user wants to open, adjust or close a position, or whenever any Bot is about to touch the exchange write path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Desk Leads, analysts, risk managers, execution traders, and reviewers use this skill to coordinate and document a trade from proposal through risk sign-off, user approval, execution, reconciliation, and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags guidance that may allow some high-impact trading adjustments without fresh confirmation, and the review was partly incomplete.

Mitigation: Before any adjustment, verify that a written, in-force mandate or pre-authorized protective action covers the exact change; otherwise require the lifecycle's exact user approval phrase. Review unresolved references and authorization exceptions before enabling the skill.

## Reference(s):

- [HyperGrok Desk Trade Lifecycle on ClawHub](https://clawhub.ai/galleonlabs/skills/hypergrok-desk-trade-lifecycle)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Text]

**Output Format:** [Markdown trade proposals, tickets, and lifecycle records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organized into proposal, evidence, risk, approval, execution, reconciliation, and review sections]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
