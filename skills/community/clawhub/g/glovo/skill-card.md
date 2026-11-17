## Description:

Navigate Glovo in a live browser session to compare stores, manage carts, and reach checkout safely before ordering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when a Glovo-specific task depends on a real signed-in session, saved address, current store availability, fees, promotions, cart state, or order issue. It helps compare delivery options, draft carts, verify checkout details, and recover from Glovo-specific order problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A signed-in browser session can expose live address, cart, payment, and ordering state, and checkout actions may create real purchases.

Mitigation: Require current-thread approval before browser control, cart changes, delivery address changes, or final order placement, and summarize checkout details before any live purchase action.

Risk: Optional persistent notes under ~/glovo/ may contain delivery preferences, address labels, store history, and issue patterns.

Mitigation: Store only durable operating preferences when the user allows local memory, and do not store passwords, payment card data, one-time verification codes, full receipts, or raw support transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/glovo)
- [Glovo skill homepage](https://clawic.com/skills/glovo)
- [Glovo web app](https://glovoapp.com)
- [Browser flow](artifact/browser-flow.md)
- [Checkout guardrails](artifact/checkout-guardrails.md)
- [Issue recovery](artifact/issue-recovery.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and local configuration file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser-control plans, checkout summaries, issue-recovery guidance, and optional local memory notes under ~/glovo/ when the user allows persistent storage.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
