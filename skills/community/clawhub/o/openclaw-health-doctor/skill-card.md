## Description: <br>
Checks OpenClaw system health across configuration, model connectivity, cron jobs, memory files, and skill loading, then reports issues and repair suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l6366616-lang](https://clawhub.ai/user/l6366616-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent to inspect an OpenClaw installation, summarize health status, and recommend concrete fixes without changing configuration by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic output may reveal local versions, configuration status, cron details, or memory-system metadata. <br>
Mitigation: Invoke the skill deliberately and avoid publishing or forwarding the report without review. <br>
Risk: Health checks may encounter sensitive values such as API keys while inspecting model and channel configuration. <br>
Mitigation: Redact sensitive values in the report and do not expose raw configuration contents. <br>
Risk: Repair suggestions could be mistaken for permission to change configuration automatically. <br>
Mitigation: Report findings first and make changes only when the user explicitly asks for remediation. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Doctor on ClawHub](https://clawhub.ai/l6366616-lang/openclaw-health-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown health report with status bullets, a health score, and repair suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sensitive values such as API keys are expected to be redacted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
