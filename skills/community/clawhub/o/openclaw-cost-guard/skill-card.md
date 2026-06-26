## Description: <br>
Tracks OpenClaw/Clawdbot token and cost usage from session JSONL logs, generates daily or weekly summaries and top expensive sessions, runs budget checks, and provides a token-saving playbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DasWeltall](https://clawhub.ai/user/DasWeltall) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor local OpenClaw/Clawdbot usage spend, identify expensive sessions, enforce budget thresholds, and apply concise token-saving practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cost reports can expose usage patterns, session IDs, and local file paths. <br>
Mitigation: Keep generated reports private unless reviewed and redact sensitive identifiers before sharing. <br>
Risk: Alert integrations can expose secrets if tokens are embedded in scripts. <br>
Mitigation: Store alert credentials outside scripts and pass them through the environment or a secret manager. <br>
Risk: Budget checks may fail scheduled jobs when the threshold is exceeded. <br>
Mitigation: Test thresholds with budget warn mode before enabling exit-on-breach automation. <br>


## Reference(s): <br>
- [OpenClaw Cost Guard release page](https://clawhub.ai/DasWeltall/openclaw-cost-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and optional JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return compact cost summaries, top-session rankings, budget status, and token-saving recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
