## Description: <br>
Real-time dashboard for task status and polo score tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor Pilot Protocol task queues, submitted task status, completion counts, and polo score changes from a local terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a local Pilot Protocol daemon and external pilotctl binary that expose task, requester, target, queue, and score information. <br>
Mitigation: Install and run it only in environments where you trust the Pilot Protocol daemon and pilotctl binary, and avoid exposing terminal output that contains sensitive task metadata. <br>
Risk: The monitoring examples poll local command output through jq and watch, so missing dependencies or an unavailable daemon can produce incomplete or stale status views. <br>
Mitigation: Confirm pilotctl, jq, and watch are installed and verify the daemon is running before relying on dashboard results. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub listing](https://clawhub.ai/teoslayer/pilot-task-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local pilotctl JSON output with jq and optional watch-based polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
