## Description: <br>
Detect drift between Infrastructure-as-Code definitions (Terraform, Pulumi, CloudFormation, CDK) and actual deployed state. Identify untracked resources, manual changes, and configuration discrepancies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, infrastructure engineers, and cloud platform teams use this skill to compare IaC definitions with deployed cloud state, detect manual changes or stale state, and prepare remediation plans before refactors or audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose Terraform import, Terraform apply, or CI scheduling commands that can affect real infrastructure if used without review. <br>
Mitigation: Review generated remediation and monitoring commands, confirm the target account and workspace, and run changes manually under normal change control with least-privilege credentials. <br>
Risk: Drift analysis requires the agent to inspect IaC files and cloud state through configured command-line tools. <br>
Mitigation: Install only in environments where this access is acceptable, and scope cloud credentials to the minimum read or change permissions required for the task. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes drift categories, risk levels, recommended actions, Terraform remediation commands, and CI scheduling examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
