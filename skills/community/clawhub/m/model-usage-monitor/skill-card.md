## Description: <br>
Monitors OpenClaw model usage from local logs, estimates model costs, calculates cache hit rate, and reports automated alert checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local model usage patterns, cost estimates, cache behavior, and threshold-based alerts from their OpenClaw environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags under-disclosed persistent scheduled execution and local agent session-file access. <br>
Mitigation: Review the cron behavior and local file access before installation; prefer manual or copy-only installation unless hourly monitoring is intended. <br>
Risk: The skill can copy monitoring code into ~/.openclaw/workspace/.lib and create an hourly OpenClaw cron job. <br>
Mitigation: Confirm how to list and remove the OpenClaw cron job before enabling automated checks. <br>
Risk: Monitoring reports are derived from local logs and session files, which can contain sensitive operational context. <br>
Mitigation: Run the skill only in environments where reading OpenClaw logs and local agent session files is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halfmoon82/model-usage-monitor) <br>
- [MIT-0 license](https://opensource.org/licenses/MIT-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON reports, markdown-style reports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit nonzero exit status during alert checks when thresholds are exceeded.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
