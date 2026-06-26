## Description: <br>
Flexible multi-agent development team wizard for OpenClaw that configures 2-10 agent teams, named teams, role templates, workflows, model assignment, and production guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to create and manage OpenClaw multi-agent development teams with configurable roles, workflows, model mappings, and post-setup governance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup wizard can make broad persistent changes to OpenClaw agent configuration. <br>
Mitigation: Install only when a persistent multi-agent OpenClaw team is intended; use named teams and back up and inspect ~/.openclaw/openclaw.json before and after setup. <br>
Risk: Logging, weekly optimization, and cron behavior may collect or retain operational context without a defined governance model. <br>
Mitigation: Do not enable skill learning telemetry, context logging, or the weekly optimizer until collection, storage, access, retention, deletion, and disable procedures are defined. <br>
Risk: Subagent fan-out can fail through spawn rejection, timeouts, missing channels, or rate limits. <br>
Mitigation: Use the documented timeout governance wrapper with graded timeouts, retries, circuit breaker behavior, explicit failure classes, and health-check reporting before production fan-out. <br>
Risk: Allowlist changes can affect which agents are visible or callable. <br>
Mitigation: Merge and deduplicate allowAgents under main.subagents.allowAgents, review the resulting allowlist, and verify agent visibility before spawning agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halfmoon82/multi-agent-team-by-halfmoon82) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Migration guide v2.1 to v2.2](artifact/MIGRATION_v2.1_to_v2.2.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JavaScript setup workflow, shell commands, and generated OpenClaw configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the setup wizard is run, it may update ~/.openclaw/openclaw.json and create team workspace files and manifests.] <br>

## Skill Version(s): <br>
2.2.2 (source: server release metadata and artifact/clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
