## Description: <br>
Optimizes context window via MECW principles and memory tiering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill during long or multi-step work to monitor context pressure, choose conservation strategies, route work across parent context, subagents, or dedicated sessions, and preserve summaries or findings without overloading the active conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may encourage agents to create local coordination, checkpoint, findings, or memory files during long tasks. <br>
Mitigation: Review workspace write behavior before use in sensitive repositories and keep generated files in approved project or temporary locations. <br>
Risk: Context-management and delegation advice can introduce misleading summaries or unnecessary subagent workflows if applied without review. <br>
Mitigation: Use the guidance when context pressure or task complexity warrants it, and review generated summaries or findings before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-context-optimization) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with tables, decision rules, and inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend local summaries, checkpoint files, memory tiers, and optional subagent coordination patterns; no executable installer is included.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter: 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
