## Description: <br>
Openclaw Safety Guard scans an OpenClaw workspace across security, memory, heartbeat, cron, shared-file, communications, and code-standard checks, then generates health scores, a local dashboard, JSON logs, and Feishu summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonzhangshuo](https://clawhub.ai/user/jasonzhangshuo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run recurring or manual workspace health checks, review dashboard and JSON outputs, and receive Feishu notifications about local safety and configuration issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a recurring weekday local scan that reads OpenClaw workspace state and stores local history. <br>
Mitigation: Confirm the cron job scope and disable path before enabling the skill in a workspace. <br>
Risk: The skill sends local security summaries to a bound Feishu open_id. <br>
Mitigation: Use least-privileged Feishu credentials and verify the notification recipient binding during setup. <br>
Risk: The skill runs Node build tooling and automatically applies a local Gateway LaunchAgent plist permission change. <br>
Mitigation: Review local build execution requirements and confirm automatic GREEN fixes are acceptable before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonzhangshuo/openclaw-safety-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, local dashboard files, and JSON scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces health summaries, per-dimension findings, local dashboard HTML, archived JSON logs, and Feishu notification content.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
