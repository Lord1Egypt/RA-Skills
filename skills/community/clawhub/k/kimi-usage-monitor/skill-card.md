## Description: <br>
Monitor Kimi K2.5 API usage and quota from the Kimi console so agents can check remaining quota, reset timers, rate-limit status, and usage patterns for resource planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xD4O](https://clawhub.ai/user/xD4O) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and autonomous coding agents use this skill to inspect Kimi K2.5 quota and rate-limit information before intensive work, subagent spawning, or long-running planning. It supports console checks, JSON automation output, and capacity-aware task decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can inspect broader authenticated browser content than the Kimi console. <br>
Mitigation: Keep the attached browser context limited to the Kimi console and select the exact Kimi console tab before taking snapshots. <br>
Risk: The subagent guard allows spawning when quota checks fail. <br>
Mitigation: For autonomous use, change quota checks and subagent spawning controls to fail closed when usage cannot be verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xD4O/kimi-usage-monitor) <br>
- [Kimi console](https://www.kimi.com/code/console) <br>
- [Platform compatibility](PLATFORM_SUPPORT.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Console text and JSON, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes usage percentages, reset timing, rate-limit information, timestamps, and subagent/preflight decisions when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
