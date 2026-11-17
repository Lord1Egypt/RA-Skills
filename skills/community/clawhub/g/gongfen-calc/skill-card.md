## Description:

Analyzes Excel and CSV task lists, normalizes fields and units, scores tasks across available dimensions, and produces traceable Excel, Markdown, and JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weikion](https://clawhub.ai/user/weikion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams can use it to turn Excel or CSV task lists into auditable task scores and reports. Results describe tasks rather than individual performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses --trusted-host, disabling certificate validation for dependency downloads.

Mitigation: Remove --trusted-host, install through a trusted package source with certificate validation enabled, and use an isolated environment.

Risk: Reruns overwrite reports and baseline data, which may contain business information; estimated task scores could also be mistaken for allocation decisions.

Mitigation: Use a dedicated output directory, protect generated reports, and review estimated scores with the team before any allocation decision.

## Reference(s):

- [Scoring anchors](artifact/references/scoring_anchors.md)
- [Field dictionary](artifact/references/field_dictionary.md)
- [ClawHub skill page](https://clawhub.ai/weikion/skills/gongfen-calc)

## Skill Output:

**Output Type(s):** [Files, Analysis]

**Output Format:** [Excel workbook, Markdown report, and JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-level scores with source-row traceability; estimated values are identified, and insufficient data reduces or suppresses scoring outputs.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
