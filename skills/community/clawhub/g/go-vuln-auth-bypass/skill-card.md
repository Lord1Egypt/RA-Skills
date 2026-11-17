## Description:

Guides audits of Go authentication and authorization flows, RBAC policies, Kubernetes admission webhooks, JWT/OAuth validation, and privilege-escalation paths in cloud-native infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhy0](https://clawhub.ai/user/yhy0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to review Go and Kubernetes/cloud-native code for authentication bypass, authorization bypass, RBAC leakage, middleware ordering, impersonation, and token-validation weaknesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes exploit-path examples and grep searches for authentication and authorization weaknesses.

Mitigation: Use it only for authorized code review and treat the examples as audit guidance, not operational attack instructions.

Risk: Static audit guidance can produce incomplete findings or false positives when applied without project context.

Mitigation: Confirm candidate issues against the target application's authentication, authorization, RBAC, and deployment design before acting.

## Reference(s):

- [Go Auth Bypass - Real-World Cases](references/cases.md)
- [ClawHub skill page](https://clawhub.ai/yhy0/skills/go-vuln-auth-bypass)
- [Publisher profile](https://clawhub.ai/user/yhy0)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with checklist items and inline grep commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces static review guidance; it does not execute code or call external services.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
