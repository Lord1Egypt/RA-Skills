## Description:

Fetches employee attendance data from the DingTalk Open Platform and saves local JSON and Excel reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renjicode](https://clawhub.ai/user/renjicode)

### License/Terms of Use:

MIT-0

## Use Case:

HR, operations, and internal automation teams use this skill to retrieve DingTalk department, employee, and attendance records for daily, weekly, or custom date-range reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Employee attendance data and DingTalk credentials may be exposed through local configuration or generated report files.

Mitigation: Protect the .env file, restrict output directories and file permissions, and install only after review by someone authorized to handle employee attendance data.

Risk: Unsafe command execution and automatic dependency installation can increase execution and supply-chain risk.

Mitigation: Patch Excel export to use argument-based process execution, remove automatic pip installs, and pin dependencies before deployment.

Risk: Scheduled attendance pulls can increase impact if run with excessive privileges.

Mitigation: Run scheduled jobs under a least-privilege account rather than a privileged account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renjicode/skills/keplerjai-dingtalk-attendance)
- [ClawHub publisher profile](https://clawhub.ai/user/renjicode)
- [DingTalk Open Platform](https://open.dingtalk.com)

## Skill Output:

**Output Type(s):** [text, JSON, Excel files, shell commands, configuration, guidance]

**Output Format:** [Terminal text plus local JSON and .xlsx report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DingTalk app credentials in a local .env or config.json and appropriate attendance/contact permissions.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
