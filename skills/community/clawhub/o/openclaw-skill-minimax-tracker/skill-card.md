## Description: <br>
Tracks MiniMax API prompt usage for OpenClaw agents with progress bars, reset timing, persistent local storage, and reminder guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QiaoTuCodes](https://clawhub.ai/user/QiaoTuCodes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to record MiniMax prompt consumption after API calls, inspect remaining quota, and configure recurring reminders from local usage data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage counts and timestamps are stored on disk. <br>
Mitigation: Use the tracker only where local usage history is acceptable, protect the workspace directory, and remove the JSON data file when retention is no longer needed. <br>
Risk: The scheduled reminder example can create recurring agent activity. <br>
Mitigation: Enable the schedule only when recurring checks are desired, review the payload before use, and disable the reminder when monitoring is no longer needed. <br>
Risk: Usage totals can become inaccurate if API calls are not recorded or configuration values no longer match the active MiniMax plan. <br>
Mitigation: Call the tracker consistently after MiniMax API use and update the configured quota and reset window when the plan changes. <br>
Risk: Clone-based installation may fetch files that differ from the reviewed release artifact. <br>
Mitigation: When installing from a Git repository instead of the reviewed package, verify the files match the reviewed artifact before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QiaoTuCodes/openclaw-skill-minimax-tracker) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [MiniMax platform](https://platform.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; runtime output is plain text status and progress lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tracker commands write local JSON usage data under ~/.openclaw/workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
