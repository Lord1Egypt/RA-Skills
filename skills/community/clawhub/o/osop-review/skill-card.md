## Description: <br>
Review .osop/.osoplog for security risks, permission gaps, and destructive commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archie0125](https://clawhub.ai/user/archie0125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review OSOP workflow or execution-log files before execution, focusing on security risks, permission scope, destructive commands, missing approval gates, cost exposure, and operational safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow or log files may contain real credentials or sensitive operational details. <br>
Mitigation: Use the skill only on files the agent is allowed to read, and redact real credentials first when exact secret values are not needed. <br>
Risk: The review is advisory and may miss context-specific execution risks. <br>
Mitigation: Review the generated findings before acting on them and confirm approval gates, permissions, and destructive commands against the actual workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/archie0125/osop-review) <br>
- [OSOP homepage](https://osop.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown risk review table and summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a risk score, verdict, findings, permissions, secrets, cost, approval-gate status, and safety recommendation.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
