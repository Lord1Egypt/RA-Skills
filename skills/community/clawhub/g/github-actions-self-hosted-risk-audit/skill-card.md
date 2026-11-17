## Description:

Audit GitHub Actions workflows that use self-hosted runners for untrusted trigger and credential-hardening risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to review GitHub Actions workflow files for risky self-hosted runner patterns, including untrusted triggers, broad runner selection, write-capable permissions, and checkout credential persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit uses lightweight heuristic checks and may miss unsafe workflow behavior.

Mitigation: Review the script and workflow findings before using the result as a CI enforcement gate.

Risk: A clean result could be mistaken for proof that self-hosted runner workflows are safe.

Mitigation: Treat a clean report as one security signal and pair it with stronger YAML parsing and checkout-input review where CI decisions depend on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-self-hosted-risk-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Text report or JSON summary of flagged workflow files, scores, severities, and critical findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and one or more workflows meet the configured critical threshold.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
