## Description:

Inspects JF camera snapshots for overflowing garbage bins and produces a graded inspection report for single, batch, or scheduled checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Facilities and sanitation teams use camera snapshots to check garbage bins for overflow, review severity-ranked reports, and schedule recurring inspections.

### Deployment Geography for Use:

China, Asia, Europe, and North America (supported JF API regions)

## Known Risks and Mitigations:

Risk: Scheduled inspection messages may expose JF API credentials.

Mitigation: Bind credentials through a secure secret store or runtime environment; never put live values in scheduled task messages.

Risk: Downloaded camera captures may reveal sensitive surveillance imagery or reach unintended IM recipients.

Mitigation: Restrict capture access, confirm report recipients before enabling pushes, and clean up stored images.

Risk: Camera-provided download URLs and image content may be unsafe in a shared workspace.

Mitigation: Validate download URLs and content before use and install only when the JF API endpoint is trusted.

## Reference(s):

- [JF Open Platform documentation](https://docs.jftech.com)
- [ClawHub skill listing](https://clawhub.ai/jftech/skills/jf-open-pro-garbage-inspection)

## Skill Output:

**Output Type(s):** [Markdown, Image files]

**Output Format:** [Severity-ranked Markdown inspection report with downloaded camera snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports severe overflow, mild overflow, normal, or undetermined results; supports scheduled reports to a selected IM recipient.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; embedded metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
