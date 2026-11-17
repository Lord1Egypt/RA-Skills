## Description:

Summarize GitHub Actions matrix job failures across runs so you can spot unstable OS/runtime axes fast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to analyze exported GitHub Actions run JSON and identify recurring CI failures by workflow, job, matrix axis, branch, failed step, repository, and conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads every local JSON file matched by RUN_GLOB and may print repository names, branches, SHAs, job URLs, and failed step names from those files.

Mitigation: Point RUN_GLOB only at intended GitHub Actions exports and review generated reports before sharing them outside the project.

Risk: Broad or incorrect filters can omit relevant failures from the report.

Mitigation: Start with a small export set or the bundled fixtures, then add workflow, branch, job, axis, conclusion, step, run, SHA, or repository filters deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-failure-matrix)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Text report or JSON summary with grouped failure records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit non-zero when FAIL_ON_FAILURES=1 and grouped failures are found.]

## Skill Version(s):

1.7.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
