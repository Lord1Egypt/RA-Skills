## Description: <br>
Audits Skill() references to detect hubs, isolates, and dangling targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit Skill() reference graphs before documentation passes, renames, retirements, quarterly audits, and composition reviews. It helps identify heavily referenced hubs, orchestrator skills, isolates, and dangling references that may need repair or documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented audit command scans the plugins tree selected by the user and can write reports to a chosen output path. <br>
Mitigation: Run it against the intended plugins root and review the output path before execution. <br>
Risk: Installing the broader source plugin may include external Claude Code plugin components beyond this skill card evidence. <br>
Mitigation: Review those external plugin components separately before using them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-skill-graph-audit) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Usage reference](modules/usage.md) <br>
- [Interpretation guide](modules/interpretation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with CLI examples and optional JSON report output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to inspect Skill() references and classify hubs, orchestrators, isolates, and dangling targets.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
