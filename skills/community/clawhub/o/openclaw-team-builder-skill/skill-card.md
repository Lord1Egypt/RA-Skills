## Description: <br>
Discovers, composes, and activates OpenClaw specialist teams from core, agency, and research rosters, with Planner and Reviewer workflows for coordinated delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoeSzeles](https://clawhub.ai/user/JoeSzeles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan multi-agent teams for engineering, trading, creative, research, marketing, and operations work, then route handoffs and review deliverables through Planner and Reviewer workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes high-impact live trading and autonomous configuration-change guidance without clear approval limits. <br>
Mitigation: Treat it as planning-only by default and do not connect it to live trading, session control, or write APIs unless explicit approvals, dry-run defaults, risk limits, audit logging, and rollback controls are added. <br>
Risk: Specialist activation can reference paid generation or other high-trust agent capabilities. <br>
Mitigation: Review referenced agent files before activation and require spending limits, human approval, and audit logs before enabling paid or high-impact operations. <br>


## Reference(s): <br>
- [Openclaw Team Builder on ClawHub](https://clawhub.ai/JoeSzeles/openclaw-team-builder-skill) <br>
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured tables, checklists, handoff templates, and occasional TSV experiment ledgers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Planning-only by default; review specialist activations and high-impact actions before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
