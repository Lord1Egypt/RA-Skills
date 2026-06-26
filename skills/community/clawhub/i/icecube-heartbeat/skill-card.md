## Description: <br>
IceCube Heartbeat guides an agent to use scheduled heartbeat polls for proactive health checks, memory governance, improvement detection, and optional outreach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ares521521-design](https://clawhub.ai/user/ares521521-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use IceCube Heartbeat to turn scheduled heartbeat polls into maintenance cycles that check pending work, memory files, agent health, and improvement opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring heartbeat tasks can trigger autonomous repository, memory, and skill-installation changes without clear user approval. <br>
Mitigation: Run heartbeat checks read-only by default and require explicit approval before commits, pushes, memory promotion, skill installation, or self-improvement routines. <br>
Risk: Optional email, calendar, weather, or API checks may access personal or external account data. <br>
Mitigation: Enable each integration separately, use narrow scopes, and keep those checks disabled unless the user explicitly opts in. <br>
Risk: Proactive outreach can interrupt users or surface low-value findings during quiet periods. <br>
Mitigation: Honor quiet hours, rate-limit notifications, and send only actionable findings that match the user's stated preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ares521521-design/icecube-heartbeat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt an agent to read local state files, update memory or documentation, and propose or perform maintenance actions depending on user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
