## Description:

Monitors live promotional traffic, conversion efficiency, inventory pressure, and funnel health to guide ad spend, restock, and traffic allocation decisions during major sales events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and promo operations teams use this skill during high-pressure sale windows to compare traffic, orders, CVR, spend, ROAS or MER, and inventory signals before changing ad budgets or routing traffic. It is intended for live or recent campaign decisions such as first-four-hour monitoring, breakeven checks, SKU sellouts, and landing-page or checkout triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend ad budget, inventory, or site changes based on incomplete, delayed, or incorrect promo metrics.

Mitigation: Provide current metrics deliberately, confirm assumptions such as margin and breakeven ROAS, and keep human approval on real budget, inventory, or site changes.

Risk: Operational recommendations can be misleading if checkout errors, stock status, or analytics lag are not verified.

Mitigation: Check dashboard freshness, checkout health, stock availability, and promotion setup before scaling spend or rerouting traffic.

## Reference(s):

- [Promo ops and traffic stress playbook](references/promo_ops_playbook.md)
- [ClawHub skill page](https://clawhub.ai/rijoyai/skills/promo-traffic-stress-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables, checklists, and concise operational recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include efficiency snapshots, action matrices, landing-page or checkout checks, restock guidance, and traffic allocation recommendations.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
