## Description:

Compare baseline vs current GitHub Actions run exports to catch workflow/job runtime regressions before CI costs and lead time spike.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and DevOps engineers use this skill to compare baseline and current GitHub Actions run exports, identify workflow or job runtime regressions, and optionally gate CI on critical regressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad BASELINE_GLOB or CURRENT_GLOB patterns can cause unrelated local JSON files to be parsed.

Mitigation: Use narrow glob paths that point to dedicated GitHub Actions artifact directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-runtime-regression-audit)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text report or JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit 1 when FAIL_ON_CRITICAL=1 and at least one job crosses critical regression thresholds.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
