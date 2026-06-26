## Description: <br>
Helps agents audit Go authentication and authorization flows for bypass patterns in RBAC, Kubernetes admission webhooks, JWT/OAuth validation, middleware chains, and cloud-native privilege paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhy0](https://clawhub.ai/user/yhy0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and code reviewers use this skill to inspect Go and Kubernetes/cloud-native projects for authentication bypass, authorization bypass, privilege escalation, and related access-control weaknesses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit searches may surface sensitive security logic, token handling, or credential-related code paths. <br>
Mitigation: Use the skill only on repositories you are authorized to review and handle discovered security-sensitive details according to the repository owner's disclosure process. <br>
Risk: Pattern matches and checklist findings may be incomplete or may flag benign code as a candidate vulnerability. <br>
Mitigation: Validate each finding against the full authentication flow, authorization checks, tests, and deployment context before relying on or reporting it. <br>


## Reference(s): <br>
- [Go Auth Bypass - Real-World Cases](references/cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with grep commands, detection checklists, and Go code-pattern examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit guidance; no executables, credentials, or API keys are required.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
