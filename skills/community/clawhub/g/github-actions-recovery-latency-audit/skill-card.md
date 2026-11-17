## Description:

Measure GitHub Actions failure recovery latency and unresolved incident age by workflow group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to audit GitHub Actions run exports, find slow recovery patterns, and identify workflow groups with unresolved failures for triage or CI gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads every file matched by RUN_GLOB, so an overly broad glob can process unintended local JSON exports.

Mitigation: Review RUN_GLOB before running the skill and point it only at the intended GitHub Actions export files.

Risk: The documented data collection command can rely on existing GitHub CLI authentication when the user manually exports run data.

Mitigation: Use a GitHub CLI session and permissions appropriate for the repositories being audited.

Risk: Using FAIL_ON_CRITICAL=1 can fail a CI job when configured thresholds classify groups as critical.

Mitigation: Tune the warning and critical thresholds before enabling FAIL_ON_CRITICAL in an automated gate.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text report or JSON summary with ranked recovery-risk groups and optional shell commands for data collection and execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local GitHub Actions run JSON exports and can exit nonzero when FAIL_ON_CRITICAL=1 and critical groups are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
