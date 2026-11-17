## Description:

Audit GitHub Actions run health by trigger event and workflow so flaky or noisy automation sources are easy to prioritize.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and DevOps engineers use this skill to analyze exported GitHub Actions runs, identify failure-prone trigger, repository, and workflow combinations, and prioritize automation reliability work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may expose repository names, branches, commit SHAs, run URLs, and workflow outcomes from matched GitHub Actions exports.

Mitigation: Keep RUN_GLOB scoped to intended export files and avoid running reports over private or sensitive repositories unless that disclosure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-trigger-health-audit)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Text report or JSON summary of GitHub Actions trigger health metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May exit nonzero when FAIL_ON_CRITICAL=1 and a critical trigger group is found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
