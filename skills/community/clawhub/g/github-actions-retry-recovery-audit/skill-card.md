## Description:

Audit GitHub Actions runs for fail-then-success retry recovery patterns to quantify flaky rerun waste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to audit exported GitHub Actions workflow runs, identify flaky retry recovery patterns, and prioritize wasted CI minutes for triage or CI enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may include private repository metadata if the input GitHub Actions JSON exports contain it.

Mitigation: Limit RUN_GLOB to intended exports and handle generated reports according to the repository metadata sensitivity.

Risk: The optional critical fail gate can cause a nonzero CI exit.

Mitigation: Enable FAIL_ON_CRITICAL only when CI enforcement is intended and threshold values have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-retry-recovery-audit)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration, JSON, Text]

**Output Format:** [Text report or JSON summary with ranked retry recoveries and critical recovery entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code is 0 in report mode, or 1 when FAIL_ON_CRITICAL=1 and critical recoveries are present.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
