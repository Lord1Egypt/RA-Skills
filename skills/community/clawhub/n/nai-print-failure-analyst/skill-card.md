## Description:

Diagnoses 3D print failures from symptoms or images, recommends slicer setting fixes, logs failures, analyzes recurring patterns, and generates failure reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External makers, print-farm operators, and 3D printing support staff use this skill to diagnose common print failures, choose slicer adjustments, keep a local failure history, and summarize recurring issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged failures may include sensitive project, customer, printer, material, or troubleshooting details in free-form fields.

Mitigation: Avoid entering sensitive details unless local retention is acceptable, and review or delete artifact/assets/failure-log.json when the history is no longer needed.

Risk: Diagnosis and slicer settings are advisory and may not match a specific printer, filament, environment, or safety requirement.

Mitigation: Treat recommendations as starting points, change settings incrementally, and verify results on test prints before using them on important jobs.

## Reference(s):

- [3D Print Failure Types](references/failure-types.md)
- [Slicer Setting Fixes by Failure Type](references/slicer-fixes.md)
- [ClawHub Skill Release](https://clawhub.ai/newageinvestments25-byte/skills/nai-print-failure-analyst)
- [ClawHub Publisher Profile](https://clawhub.ai/user/newageinvestments25-byte)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON from diagnostic commands and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read a local failure history file at artifact/assets/failure-log.json when the user logs or reviews failures.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
