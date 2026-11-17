## Description:

Calculate literature growth velocity and acceleration to assess research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research analysts use this skill to calculate publication growth velocity and acceleration for keywords, classify research-field lifecycle stage, and produce trend estimates from time-series literature counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene issues may affect broad deployment.

Mitigation: Install in an isolated virtual environment, remove unnecessary dataclasses and enum dependencies for Python 3.8+, and pin NumPy to a reviewed version.

Risk: Input and output file handling can read from or write to unintended locations if paths are chosen carelessly.

Mitigation: Keep input and output paths inside the intended workspace and review generated files before sharing.

Risk: Forecasts and lifecycle labels can be mistaken for authoritative research conclusions.

Mitigation: Treat generated forecasts as analytical estimates and confirm conclusions against source literature and domain expertise.

## Reference(s):

- [Audit Reference](artifact/references/audit-reference.md)
- [Keyword Velocity Tracker on ClawHub](https://clawhub.ai/aipoch-ai/skills/keyword-velocity-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON analysis outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a keyword and year/count time-series data; generated forecasts are analytical estimates that should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
