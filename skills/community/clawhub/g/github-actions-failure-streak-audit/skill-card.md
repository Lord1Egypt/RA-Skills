## Description:

Detect consecutive GitHub Actions failure streaks by repo/workflow/branch to prioritize unstable pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to analyze exported GitHub Actions run data, identify repeated CI failure streaks, and prioritize unstable workflows by severity and runtime impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local GitHub Actions JSON files matching RUN_GLOB and may print repository names, branches, SHAs, run URLs, and failure timing.

Mitigation: Keep RUN_GLOB scoped to the intended export directory and avoid sharing generated reports when they contain sensitive repository or CI details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-failure-streak-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; the bundled script produces text or JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report fields include grouped streak totals, ranked hotspots, summary data, streak records, and critical streak records.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
