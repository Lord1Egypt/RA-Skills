## Description:

Detect flaky GitHub Actions job steps by finding mixed success/failure conclusions across runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to analyze exported GitHub Actions run JSON and identify CI steps that alternate between successful and failed conclusions. It supports local reporting and optional CI enforcement for critical flaky step groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads files matched by RUN_GLOB, which could unintentionally include private or unrelated GitHub Actions exports if scoped too broadly.

Mitigation: Keep RUN_GLOB pointed at the intended exported CI run JSON directory and avoid broad private directories.

Risk: The optional CI fail gate can fail a pipeline when critical flaky step groups are detected.

Mitigation: Review WARN_FAILURE_RATE, CRITICAL_FAILURE_RATE, MIN_OCCURRENCES, and FAIL_ON_CRITICAL before enabling enforcement in CI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-step-flake-audit)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Text report or JSON summary with ranked flaky step groups and critical groups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May exit with status 1 when FAIL_ON_CRITICAL=1 and critical flaky step groups are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
