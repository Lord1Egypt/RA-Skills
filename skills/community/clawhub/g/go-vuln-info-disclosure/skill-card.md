## Description:

Guides agents through audits of Go code for information disclosure in logs, errors, HTTP responses, Kubernetes Secret handling, and credential storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhy0](https://clawhub.ai/user/yhy0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit Go services for credential leaks and sensitive data exposure across logs, API serialization, Kubernetes resources, and error paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad security review examples, including auth-bypass and RCE-adjacent cases, could be misapplied outside an authorized assessment.

Mitigation: Use the skill only for authorized defensive review and keep analysis scoped to systems the reviewer is permitted to assess.

Risk: Pattern-based grep checks can produce false positives or miss source-to-sink context.

Mitigation: Trace candidate findings manually and confirm missing sanitization before reporting a vulnerability.

Risk: Audit work may surface real credentials or sensitive strings in code, logs, or API responses.

Mitigation: Redact secrets in notes and reports, and avoid copying raw credentials into prompts or shared artifacts.

## Reference(s):

- [Go Information Disclosure -- Real-World Cases](references/cases.md)
- [ClawHub Skill Page](https://clawhub.ai/yhy0/skills/go-vuln-info-disclosure)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown guidance with grep command examples and audit checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language audit guidance with real-world vulnerability examples.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
