## Description:

Audit GitHub Actions job runtime risk against timeout thresholds so near-timeout jobs get fixed before they fail CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI maintainers use this skill to review GitHub Actions run exports, identify jobs that are near configured timeout thresholds or already timed out, and decide where to tune timeouts or reduce runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted workflow, repository, or job names may make plain text logs misleading.

Mitigation: Prefer OUTPUT_FORMAT=json or trusted input data when report data may contain untrusted names.

Risk: Auditing unintended files can produce irrelevant or confusing timeout findings.

Mitigation: Run the skill only against intended GitHub Actions export files and set RUN_GLOB and filters deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-timeout-risk-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Text report or JSON containing summary, ranked groups, and critical_instances.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and critical timeout-risk instances are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
