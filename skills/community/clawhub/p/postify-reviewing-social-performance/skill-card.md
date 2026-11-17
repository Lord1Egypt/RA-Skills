## Description:

Produces a read-only report of Postify delivery, failures, channel performance, and suggested posting times from workspace analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers and other Postify users review their workspace's delivery results, investigate failed posts, compare channels, and identify suggested posting times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Excess Postify permissions could allow changes beyond read-only reporting.

Mitigation: Confirm OAuth scopes allow read-only analytics and post access; avoid posting and deletion scopes unless needed for other skills.

Risk: Missing metrics or an unclear date range could make the report misleading.

Mitigation: Agree the reporting window, use only returned figures, and state when a metric is unavailable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with per-channel table and suggested posting times]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; defaults to the last 30 days and closes with up to three next steps.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
