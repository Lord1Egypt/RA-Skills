## Description:

Classify environmental and meteorological variables into driver categories for attribution analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and agents working on environmental attribution use this skill to group meteorological, hydrological, wind, and human variables into meaningful driver categories before analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Driver categories may not fit every dataset, location, or attribution method.

Mitigation: Review classifications for scientific fit with the dataset and validate that resulting groups make physical sense.

Risk: Derived variables such as net radiation can be misleading if source variables use incompatible definitions, units, or signs.

Mitigation: Check variable definitions and units before combining fields, and document each classification and derivation decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/lake-warming-attribution-meteorology-driver-classification)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown guidance with a short Python example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces category assignments and derived-variable suggestions; does not execute code or access data.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
