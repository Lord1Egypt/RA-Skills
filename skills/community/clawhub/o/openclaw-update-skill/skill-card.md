## Description: <br>
Check for OpenClaw updates, perform updates, and manage version status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rothcold](https://clawhub.ai/user/rothcold) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check OpenClaw version status, apply pnpm-based OpenClaw updates, restart the gateway, and verify update results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Update commands can install a different OpenClaw package version than intended. <br>
Mitigation: Confirm the package source and target version before running pnpm or OpenClaw update commands. <br>
Risk: Restarting the OpenClaw gateway can interrupt active service. <br>
Mitigation: Schedule gateway restarts during an acceptable maintenance window and verify gateway status afterward. <br>
Risk: Cron-based update checks can run more often or at different times than intended. <br>
Mitigation: Configure any scheduled update checks deliberately and review the schedule before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rothcold/openclaw-update-skill) <br>
- [Publisher profile](https://clawhub.ai/user/rothcold) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw and pnpm commands plus version-check guidance.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
