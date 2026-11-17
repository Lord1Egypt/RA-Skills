## Description:

Audit deployment workflow risk from GitHub Actions runs by scoring failure rate, unresolved failure streaks, and time since last successful deploy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to rank deployment workflows that may be risky to trust for production releases, using exported GitHub Actions run data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit reads selected GitHub Actions JSON exports that may contain repository names, branches, workflow names, run timing, and sample run URLs.

Mitigation: Keep RUN_GLOB narrow and review JSON output before sharing it outside the intended audience.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, shell commands]

**Output Format:** [Text report or JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit 1 when FAIL_ON_CRITICAL=1 and one or more groups are critical.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
