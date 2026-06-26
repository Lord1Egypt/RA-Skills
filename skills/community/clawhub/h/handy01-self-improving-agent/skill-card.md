## Description: <br>
Self-improving agent system that analyzes conversation quality, identifies improvement opportunities, and continuously optimizes response strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[handy01](https://clawhub.ai/user/handy01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze conversation quality, log improvement notes, generate weekly improvement reports, and suggest updates to an OpenClaw agent's working style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local improvement notes may be written to improvement_log.md in the OpenClaw workspace. <br>
Mitigation: Install only when local logging is acceptable, and avoid enabling automatic post-session analysis for sensitive chats unless the host provides clear opt-in, scoping, and deletion controls. <br>
Risk: Automatic conversation analysis could capture sensitive chat context if enabled broadly. <br>
Mitigation: Scope use to appropriate workspaces and review host controls for opt-in behavior and retention before enabling automatic analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/handy01/handy01-self-improving-agent) <br>
- [Publisher profile](https://clawhub.ai/user/handy01) <br>
- [Project homepage](https://github.com/xiucheng/self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Text guidance, Markdown reports and logs, JSON statistics, and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local improvement notes to improvement_log.md in the OpenClaw workspace when logging is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
