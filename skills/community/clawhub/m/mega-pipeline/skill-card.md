## Description: <br>
Runs a closed-loop OpenClaw automation pipeline that coordinates hunter scanning, gap checks, skill generation, dashboard refreshes, profit reporting, and resilience checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run and check a local OpenClaw workflow that chains market scanning, orchestration, dashboard status, profit reporting, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pipeline runs fixed downstream OpenClaw skill scripts, so its behavior depends on the trustworthiness of those installed components. <br>
Mitigation: Install and run it only in workspaces where the hunter, orchestrator, dashboard, profit, and resilience skills have been reviewed and trusted. <br>
Risk: Pipeline logs may include snippets of business or operational output. <br>
Mitigation: Review or clear the pipeline_logs directory when that output is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freeman88-tch/mega-pipeline) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/freeman88-tch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Console text and JSON log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local pipeline run logs under the OpenClaw workspace state directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
