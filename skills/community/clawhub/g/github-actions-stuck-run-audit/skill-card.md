## Description: <br>
Detect stale queued/in-progress GitHub Actions runs before they quietly block delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to audit exported GitHub Actions run data, identify stale queued or in-progress workflow runs, and decide when a CI gate should warn or fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output can include repository, workflow, run, or branch details from GitHub Actions exports. <br>
Mitigation: Review text or JSON output before sharing it outside the intended team or system. <br>
Risk: A broad RUN_GLOB can include unintended GitHub Actions export files in the audit. <br>
Mitigation: Set RUN_GLOB to the intended export directory or file pattern before running the skill. <br>
Risk: Enabling FAIL_ON_CRITICAL can intentionally block CI when critical stuck-run groups are detected. <br>
Mitigation: Use FAIL_ON_CRITICAL=1 only in workflows where blocking delivery on critical findings is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-stuck-run-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples; runtime audit output is text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally return a non-zero exit code when FAIL_ON_CRITICAL=1 and critical stuck-run groups are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
