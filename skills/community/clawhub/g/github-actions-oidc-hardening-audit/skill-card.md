## Description:

Audit GitHub Actions cloud auth workflows for OIDC hardening gaps like missing id-token write permissions, static cloud secrets, and floating auth action refs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers, DevOps engineers, and security teams use this skill to review GitHub Actions workflow YAML for cloud authentication patterns that may weaken OIDC-based federation or expose long-lived cloud credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regex-based workflow scanning can miss effective permissions or complex multi-job behavior.

Mitigation: Treat findings as advisory and pair them with human review of workflow structure, inherited permissions, and cloud identity configuration.

Risk: A clean result does not prove that cloud authentication is fully hardened.

Mitigation: Use the report as one signal in a broader security review before relying on the workflow in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-oidc-hardening-audit)
- [ClawHub publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Text report or JSON summary with flagged workflows and critical workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and critical workflows are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
