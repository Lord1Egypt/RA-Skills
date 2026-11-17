## Description:

Audit GitHub Actions workflow cache usage for poisoning, keying, and secret-path risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to statically review GitHub Actions workflows for risky cache usage, including untrusted trigger combinations, weak cache keys, broad restore prefixes, sensitive cache paths, and floating cache action refs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may not be complete for every workflow shape, especially where multiline YAML parsing limitations affect detection.

Mitigation: Use it as a lightweight local checker, keep WORKFLOW_GLOB scoped to workflow files, and independently review results before treating them as a complete security gate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-cache-hardening-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Text report or JSON audit report from a Bash/Python command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally exit nonzero when FAIL_ON_CRITICAL=1 and a critical workflow is detected.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
