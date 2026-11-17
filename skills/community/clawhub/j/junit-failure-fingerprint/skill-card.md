## Description:

Cluster JUnit failures into stable fingerprints so CI triage focuses on root causes, not noisy one-off logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI maintainers use this skill to group noisy JUnit failure and error records into repeatable fingerprints for faster test triage. It supports local or CI workflows that need text summaries or machine-readable JSON for annotations and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JUnit failure messages and stack traces may contain secrets or sensitive test data.

Mitigation: Use a narrow JUNIT_GLOB such as an artifacts or test-results directory, and review text or JSON output before uploading or sharing it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/daniellummis/skills/junit-failure-fingerprint)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Text report or JSON output produced from JUnit XML inputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable with JUNIT_GLOB, TOP_N, OUTPUT_FORMAT, STACK_LINES, and FAIL_ON_FAILURES; requires bash and python3.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
