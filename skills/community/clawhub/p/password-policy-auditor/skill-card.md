## Description:

Audit password policies and authentication configurations for security compliance. Check password complexity, storage (hashing algorithms), rotation policies, MFA coverage, account lockout, and compliance with NIST 800-63, OWASP, and PCI-DSS guidelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, application security reviewers, and compliance teams use this skill to audit authentication systems, identify password policy gaps, and produce remediation plans aligned to common security standards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The breach-check example contacts an external service with a password hash prefix.

Mitigation: Use it only in user-approved test or policy-review workflows, and avoid entering live user passwords into ad hoc scripts.

Risk: Generated audit findings and remediation plans can be incomplete without system-specific review.

Mitigation: Have qualified reviewers verify the results against the target application, deployed controls, and applicable compliance requirements before production changes.

## Reference(s):

- [Have I Been Pwned Pwned Passwords range API](https://api.pwnedpasswords.com/range/{prefix})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit checklists, command examples, compliance mappings, and remediation planning guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
