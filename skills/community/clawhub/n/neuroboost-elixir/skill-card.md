## Description: <br>
NeuroBoost Elixir provides autonomous agents with guidance and utilities for resource-aware model routing, persistent memory, self-diagnosis, health scoring, self-healing, context engineering, knowledge graph memory, and multi-agent collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidadong2359](https://clawhub.ai/user/weidadong2359) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent builders use this skill to guide autonomous agents toward lower-cost execution, persistent cross-session memory, health monitoring, repair workflows, and coordinated multi-agent operation. The bundled JavaScript package also provides local diagnostic and optimization utilities for agent experiments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad autonomous memory, repair, restart, persistence, and trading-style workflows. <br>
Mitigation: Use it only in a dedicated workspace, review files it writes, and require explicit approval before restarts, configuration changes, external messages, purchases, posts, or trades. <br>
Risk: Persistent memory and diagnostic files can capture sensitive operational context if used in a shared or production workspace. <br>
Mitigation: Do not store secrets or private keys in the skill's memory files, and review generated memory, dashboard, and coordination records before sharing or deploying them. <br>
Risk: The skill is configured for broad auto-activation in artifact evidence. <br>
Mitigation: Disable broad auto-activation where possible and invoke the skill intentionally for agent optimization, memory, diagnosis, or coordination tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidadong2359/neuroboost-elixir) <br>
- [Publisher profile](https://clawhub.ai/user/weidadong2359) <br>
- [Failure Gallery](https://github.com/Davdong2/lobster-backup/blob/main/docs/neuroboost-failure-gallery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples; the package also exposes JavaScript modules and CLI text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent behavior may include persistent memory files, diagnostic reports, health dashboards, and coordination records when the user adopts the documented workflows.] <br>

## Skill Version(s): <br>
5.1.1 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
