## Description: <br>
Cleans up accumulated OpenClaw subagent and cron child sessions to improve slow subagent startup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrddrl](https://clawhub.ai/user/lrddrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw use this skill to reduce slow subagent startup caused by accumulated child session records. It guides stopping the gateway, running a cleanup script or dry run, and restarting the gateway while preserving main and channel sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced cleanup.ps1 script is not included in the artifact evidence and may modify session records. <br>
Mitigation: Obtain and inspect the exact cleanup script before use, confirm which sessions.json and history files it will touch, and run a dry run first. <br>
Risk: Using the CleanJsonl option can delete conversation history files. <br>
Mitigation: Back up session data before cleanup and require explicit confirmation before deleting any .jsonl history files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrddrl/openclaw-subagent-session-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with PowerShell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run and history-file deletion cautions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
