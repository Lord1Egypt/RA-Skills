## Description:

Guide human release testing on an isolated OCM copy or approved in-place gateway, collect feedback, or refresh the release campaign.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw maintainers and release testers use this skill to validate a release against a selected Gateway, collect human-reviewed feedback, or refresh a release campaign. The tester judges quality while the skill guides preparation, reporting, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads a mutable latest-release script and runs it without verification, which ClawScan identifies as the main reported risk.

Mitigation: Review the installer and verify its source and integrity; use a pinned, reviewed version before execution.

Risk: Scanner coverage was partial, and one referenced file was only partially analyzed.

Mitigation: Review the partially analyzed file and obtain complete scan coverage before relying on the scan as a full assessment.

## Reference(s):

- [Gateway preparation](references/gateway-preparation.md)
- [Human testing guide](references/human-testing.md)
- [Report and closeout guidance](references/report-closeout.md)
- [OpenClaw maturity scorecard](https://docs.openclaw.ai/maturity/scorecard.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Markdown checklists, worksheets, and feedback drafts with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human-reviewed; may include sanitized validation feedback and setup guidance.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
