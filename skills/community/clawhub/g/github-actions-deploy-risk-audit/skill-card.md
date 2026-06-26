## Description: <br>
Audit deployment workflow risk from GitHub Actions runs by scoring failure rate, unresolved failure streaks, and time since last successful deploy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to rank GitHub Actions deployment workflows by production release risk, using exported run JSON and configurable thresholds for failure rate, trailing failure streaks, and stale successful runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Bash/Python script executes against files matched by RUN_GLOB. <br>
Mitigation: Install only if local script execution is acceptable and keep RUN_GLOB pointed at the intended GitHub Actions export directory. <br>
Risk: Reports can include repository, branch, workflow, and run URL details. <br>
Mitigation: Review generated text or JSON output before sharing it outside the intended audience. <br>
Risk: FAIL_ON_CRITICAL can fail release pipelines when critical groups are detected. <br>
Mitigation: Test report-only mode before enabling FAIL_ON_CRITICAL in release pipelines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-deploy-risk-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script emits text or JSON reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report mode exits 0 by default; fail-gate mode exits 1 when FAIL_ON_CRITICAL=1 and one or more groups are critical.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
