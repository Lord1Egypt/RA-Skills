## Description:

Audit GitHub Actions queue wait hotspots from run/job JSON so CI bottlenecks are visible before they stall merges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI maintainers use this skill to analyze exported GitHub Actions run/job JSON, rank queue wait hotspots, and decide where queue delays are slowing merges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can expose CI metadata such as repository names, branches, job names, run IDs, and GitHub URLs.

Mitigation: Set RUN_GLOB only to the intended GitHub Actions export files and review generated reports before sharing them outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-queue-latency-audit)
- [ClawHub publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Human-readable text report or machine-readable JSON report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return a non-zero exit status when configured to fail on critical queue waits.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
