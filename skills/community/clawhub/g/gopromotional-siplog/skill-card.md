## Description:

Estimate a daily water goal and keep a simple hydration log (add drinks in ml, l, cl or oz; see progress, a 7-day history and streaks). Use when someone wants to track water intake, asks how much water to drink, or logs a drink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nbkdevs](https://clawhub.ai/user/nbkdevs)

### License/Terms of Use:

MIT-0

## Use Case:

People who want to track daily water intake can estimate a general hydration goal, log drinks, and review daily progress, recent history, and streaks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external package implementation was not independently verified, and running an unpinned third-party package may introduce risk.

Mitigation: Review the package and pin a reviewed version before running it.

Risk: Hydration history is saved in a local JSON file.

Mitigation: Use the documented file override when needed, and protect or remove the file according to the sensitivity of its contents.

## Reference(s):

- [GoPromotional SipLog on ClawHub](https://clawhub.ai/nbkdevs/skills/gopromotional-siplog)
- [GoPromotional branded water bottles](https://www.gopromotional.co.uk/branded-products/branded-water-bottles)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Hydration summaries or machine-readable JSON, with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hydration history is stored in a local JSON file.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
