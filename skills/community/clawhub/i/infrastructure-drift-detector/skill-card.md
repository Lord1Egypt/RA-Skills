## Description:

Detect drift between Infrastructure-as-Code definitions (Terraform, Pulumi, CloudFormation, CDK) and actual deployed state. Identify untracked resources, manual changes, and configuration discrepancies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and infrastructure teams use this skill to compare IaC definitions with deployed cloud state, find manual changes or untracked resources, set up continuous drift detection, and draft remediation plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated remediation or monitoring commands could change infrastructure state or operational alerting if run without review.

Mitigation: Review generated CI schedules, cron jobs, terraform import commands, and terraform apply commands before enabling or executing them.

Risk: Cloud drift inspection can cover broad account scope when local IaC files and configured cloud credentials allow it.

Mitigation: Run the skill with credentials scoped to the intended accounts, projects, and read or change permissions needed for the audit.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown drift reports with inline shell commands and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Terraform import/apply commands, CI schedules, cron jobs, and cloud audit steps that require review before use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
