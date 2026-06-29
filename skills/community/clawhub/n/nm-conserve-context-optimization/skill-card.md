## Description: <br>
Optimizes context window via MECW principles and memory tiering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor context pressure, apply MECW guidance, route work to subagents or dedicated sessions, and manage memory tiers during long or multi-file workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes workflows that can create local checkpoints and coordination files, which may capture sensitive project state if used without boundaries. <br>
Mitigation: Decide allowed checkpoint and coordination paths before use, and avoid storing secrets or credentials in those files. <br>
Risk: Subagent and cross-plugin workflows can change shared resources if delegated too broadly. <br>
Mitigation: Require explicit approval before multi-agent or cross-plugin workflows modify shared resources. <br>
Risk: Context optimization advice may lead an agent to skip relevant evidence or over-compress important history. <br>
Mitigation: Review summaries and retained evidence before relying on synthesized results for consequential decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conserve-context-optimization) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>
- [MECW principles module](artifact/modules/mecw-principles.md) <br>
- [Subagent coordination module](artifact/modules/subagent-coordination.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with examples, checklists, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes context thresholds, routing rules, memory-tier conventions, and coordination-file patterns.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
