## Description: <br>
Audit AWS IAM policies and roles for over-privilege, wildcard permissions, and least-privilege violations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security engineers, cloud administrators, and developers use this skill to review AWS IAM policy documents, identify risky permissions, and draft least-privilege remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated IAM findings and replacement policies may be incomplete or unsuitable for a production AWS environment. <br>
Mitigation: Treat the output as advisory, share only the policy context needed for review, and verify recommendations before changing production IAM permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/iam-policy-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with findings tables and JSON policy snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk scoring, MITRE ATT&CK mapping, remediation recommendations, and IAM Access Analyzer guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
