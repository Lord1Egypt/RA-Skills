## Description:

Audit pull-request and merge-queue GitHub Actions reliability by scoring failure rate, queue latency, and stale-success risk for merge gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to audit exported GitHub Actions run data for unreliable pull-request and merge-queue gates before they block merges or mask degraded CI health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad RUN_GLOB can cause the report to read more local JSON files than intended.

Mitigation: Scope RUN_GLOB to the intended GitHub Actions artifacts directory before running the audit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daniellummis/skills/github-actions-pr-gate-health-audit)
- [Publisher Profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text or JSON reports, with shell commands and environment-variable configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and one or more scored gate groups are critical.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
