## Description:

Audit GitHub Actions mainline branch reliability by scoring failure rate, consecutive failures, and stale-success risk for critical workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to audit GitHub Actions reliability on protected branches and identify workflows with high failure rates, consecutive failures, or stale successful runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may include private repository names, workflow names, commit SHAs, and run URLs from user-provided GitHub Actions exports.

Mitigation: Use a narrow RUN_GLOB and review generated text or JSON before sharing it outside the organization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daniellummis/skills/github-actions-mainline-health-audit)
- [Publisher Profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text report or JSON summary with scored workflow groups and critical group details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and critical groups are present.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
