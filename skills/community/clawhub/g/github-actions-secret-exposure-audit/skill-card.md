## Description:

Audit GitHub Actions workflow files for secret exposure risks like pull_request_target secret usage, secret echo commands, and unpinned action secret passing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to audit GitHub Actions workflow YAML for secret exposure patterns before credentials leak or unsafe token use reaches CI. It helps prioritize risky workflows and optionally fail CI on critical findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON reports may include full workflow lines containing suspected hardcoded credentials.

Mitigation: Prefer text output for shared logs. If JSON output is required, redact sensitive fields before publishing CI artifacts or logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daniellummis/skills/github-actions-secret-exposure-audit)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Text or JSON audit report with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and python3. JSON reports may include matched workflow lines.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
