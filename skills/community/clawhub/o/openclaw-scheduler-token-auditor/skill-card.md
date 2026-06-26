## Description: <br>
Audits OpenClaw scheduler token usage for cron jobs, scheduled tasks, and heartbeat sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yueeli](https://clawhub.ai/user/yueeli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and workspace administrators use this skill to audit scheduled OpenClaw jobs and heartbeat sessions for high token usage, threshold overruns, and unexpected scheduler token burn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output may reveal private operational details from scheduled jobs, run records, heartbeat sessions, or transcripts. <br>
Mitigation: Use the skill only in approved workspaces and share audit findings only with people authorized to see scheduler and transcript details. <br>
Risk: Missing token usage or heartbeat-only evidence could be overread as proof that a run is inexpensive. <br>
Mitigation: Keep the skill's Exact, Bounded, and Inconclusive evidence labels and avoid exact token claims unless authoritative usage fields are present. <br>


## Reference(s): <br>
- [OpenClaw Scheduler Token Auditor ClawHub release](https://clawhub.ai/yueeli/openclaw-scheduler-token-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit findings with evidence labels, threshold verdicts, concise cause analysis, and optional OpenClaw CLI fallback commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Exact, Bounded, and Inconclusive evidence classes and requires the active token threshold to be stated.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
