## Description: <br>
Audit pull-request and merge-queue GitHub Actions reliability by scoring failure rate, queue latency, and stale-success risk for merge gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit exported GitHub Actions pull-request and merge-queue run data, identify unreliable merge gates, and optionally fail CI when critical gate-health risks are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fail a pipeline when FAIL_ON_CRITICAL=1 and critical gate-health results are found. <br>
Mitigation: Enable FAIL_ON_CRITICAL only in jobs where critical audit results should intentionally fail the pipeline. <br>
Risk: The analysis depends on the GitHub Actions run JSON files selected by RUN_GLOB. <br>
Mitigation: Keep RUN_GLOB pointed at the intended GitHub Actions export JSON files before running the audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-pr-gate-health-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Shell commands] <br>
**Output Format:** [Text report or JSON object emitted by a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit 1 when FAIL_ON_CRITICAL=1 and one or more groups are critical.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
