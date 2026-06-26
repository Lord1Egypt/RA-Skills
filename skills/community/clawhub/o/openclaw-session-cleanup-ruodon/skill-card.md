## Description: <br>
Cleans up accumulated OpenClaw subagent and cron-run child sessions to reduce slow subagent startup caused by an oversized sessions index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrddrl](https://clawhub.ai/user/lrddrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill when subagents start slowly or sessions.json has accumulated many child session records. It guides them through stopping the gateway, running a cleanup PowerShell script, and restarting the gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced cleanup script can change OpenClaw session state. <br>
Mitigation: Run it only from a trusted OpenClaw directory after inspecting the actual cleanup.ps1 script, and use -DryRun first. <br>
Risk: Using -CleanJsonl can delete conversation history. <br>
Mitigation: Back up sessions.json and any .jsonl history that should be retained, and use -CleanJsonl only when history deletion is intentional. <br>


## Reference(s): <br>
- [OpenClaw Session Cleanup skill instructions](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/lrddrl/openclaw-session-cleanup-ruodon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes a dry-run option and a separate option for deleting .jsonl history files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
