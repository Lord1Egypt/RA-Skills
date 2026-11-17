## Description:

Audit GitHub Actions workflow conclusion volatility to surface unstable pipelines before they become chronic failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to audit exported GitHub Actions workflow run history, identify workflows that frequently change conclusions, and decide whether unstable pipelines should block CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Bash/Python reporting script over GitHub Actions JSON exports.

Mitigation: Keep RUN_GLOB pointed only at intended run-export files before execution.

Risk: FAIL_ON_CRITICAL can turn audit findings into a CI failure gate.

Mitigation: Review text or JSON output before enabling FAIL_ON_CRITICAL in automated pipelines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-conclusion-volatility-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Text report or JSON object with summary, ranked groups, and critical groups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and critical groups are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
