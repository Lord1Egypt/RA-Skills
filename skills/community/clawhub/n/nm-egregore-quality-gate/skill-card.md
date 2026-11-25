## Description:

Orchestrates the QUALITY pipeline stage for egregore work items, running code review, unbloat, and test updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to run the egregore quality pipeline on their own work or to review a pull request. It coordinates convention checks, mapped review and maintenance skills, collects findings, and records a verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: In PR-review mode, the workflow may publish findings and submit a GitHub review under the authenticated account.

Mitigation: Review the findings and confirm the target pull request and authenticated account before enabling review submission.

Risk: The security scan was partial because two referenced local paths were absent from the scanned artifact, leaving evidence about them incomplete.

Mitigation: Ensure the referenced files are available and review them before relying on the scan.

## Reference(s):

- [The Coming Loop](https://lucumr.pocoo.org/2026/6/23/the-coming-loop/)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Quality findings and verdict in text; a manifest decision in JSON; optionally a GitHub review comment.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PR-review mode may submit a review using the authenticated GitHub account.]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
