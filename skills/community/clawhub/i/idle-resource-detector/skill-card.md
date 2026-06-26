## Description: <br>
Detect AWS idle and zombie resources consuming cost with zero meaningful utilization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Cloud engineers and AWS operators use this skill to find idle AWS resources, estimate monthly and annual waste, prioritize cleanup, and prepare runbooks with AWS CLI cleanup commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may rely on the agent's AWS CLI context and propose cleanup commands that affect cloud resources. <br>
Mitigation: Use read-only discovery first, verify the AWS account, region, and resource IDs, and review every generated deletion or cleanup command before execution. <br>
Risk: Resources that appear idle may still be important to production, critical, or compliance workflows. <br>
Mitigation: Require human confirmation for cleanup actions and manually review resources marked or named as production, critical, or otherwise sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/idle-resource-detector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with resource summaries, prioritized tables, runbooks, checklists, and AWS CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes estimated monthly waste, estimated annual savings, cleanup priorities, and confirmation flags for deletion-sensitive resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
