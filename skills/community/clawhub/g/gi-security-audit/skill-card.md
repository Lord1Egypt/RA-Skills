## Description:

Audits code for sensitive data exposure, dependency vulnerabilities, SQL injection, hardcoded secrets, XSS and injection issues, authorization gaps, and unsafe logging or error disclosure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laimiaohua](https://clawhub.ai/user/laimiaohua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code before deployment, during dependency changes, or when investigating sensitive data exposure, vulnerable dependencies, injection risks, authorization gaps, and unsafe logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad security-adjacent activation wording may lead to audits outside the user's intended scope.

Mitigation: Define the audit scope, target files, dependency manifests, and expected output before applying the checklist.

Risk: Optional pip install examples use unpinned scanner packages.

Mitigation: Run scanner installs in an isolated virtual environment or with pipx, avoid root execution, and prefer pinned versions from trusted package sources.

Risk: Checklist-style security reviews can miss project-specific vulnerabilities or produce incomplete remediation guidance.

Mitigation: Use the report as review guidance alongside code review, dependency scanning, tests, and project-specific security requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown security audit report with checklist items, code examples, and optional command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-grouped findings with locations, remediation guidance, passing checks, and optional local scanner commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
