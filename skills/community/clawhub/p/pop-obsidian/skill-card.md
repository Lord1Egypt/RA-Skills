## Description: <br>
Plugin Orchestration Protocol (POP) for Obsidian integration that helps an agent discover plugin capabilities and orchestrate multi-step workflows through JSON-RPC over WebSocket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toolate28](https://clawhub.ai/user/toolate28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to coordinate Obsidian vault workflows, plugin actions, progress updates, and coherence checks from an agent. It is suited for multi-step note, research, drafting, export, and automation pipelines where the user controls the local Obsidian and bridge environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger broad Obsidian vault changes such as creating, updating, deleting, tagging, merging, and exporting notes through connected plugins. <br>
Mitigation: Use a test vault first, keep destructive actions disabled or approval-gated, and review each pipeline before execution. <br>
Risk: Pipeline steps may access environment variables or send vault content to external AI or host tools through separate integrations. <br>
Mitigation: Restrict environment-variable access, require explicit opt-in before external content sharing, and run only trusted bridge and plugin components. <br>
Risk: The release depends on separate Obsidian, Rust bridge, community plugin, and host tool behavior outside the skill package. <br>
Mitigation: Install only trusted companion components, pin expected versions where possible, and verify bridge/plugin behavior in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/toolate28/pop-obsidian) <br>
- [Pipeline Templates](references/pipeline-templates.md) <br>
- [POP Plugin Catalog](references/plugin-catalog.md) <br>
- [POP Protocol Specification](references/protocol-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, shell commands, markdown] <br>
**Output Format:** [Markdown with JSON-RPC examples, pipeline definitions, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce pipeline plans and action payloads that affect local Obsidian vault content when executed through the required bridge and plugins.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
