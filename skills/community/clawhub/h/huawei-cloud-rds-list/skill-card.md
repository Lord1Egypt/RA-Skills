## Description:

Lists Huawei Cloud RDS instances in a selected region and presents filtered inventory as a table, JSON, Markdown, or CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use it to inspect regional RDS inventories, support operations patrols and handovers, and retrieve instance IDs for follow-on tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment-controlled settings may bypass the claimed read-only command limits and run an arbitrary executable with the agent's privileges, potentially exposing cloud credentials.

Mitigation: Follow the scanner guidance not to install until reviewing how inherited environment variables and tool permissions are controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-rds-list)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [IAM policies](references/iam-policies.md)
- [KooCLI installation guide](references/cli-installation-guide.md)
- [Verification method](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, CSV]

**Output Format:** [Terminal table, JSON array, Markdown table, or CSV file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Regional inventory with optional instance filters; Markdown and CSV exports use Chinese headers.]

## Skill Version(s):

1.0.8 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
