## Description: <br>
ontology-pro builds and updates knowledge graphs from text, supports multi-step causal reasoning, and produces actionable strategy recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract entities and relationships from text, maintain persistent JSON knowledge graphs, reason over causal paths and variables, and turn the results into prioritized strategy recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent knowledge graphs can retain and reuse user-derived content across sessions without clear consent or retention controls. <br>
Mitigation: Use explicit ontology or memory commands, avoid sensitive or regulated content unless retention and deletion are defined, and review stored graph files before reuse or sharing. <br>


## Reference(s): <br>
- [Cognitive Graph Protocol](references/cognitive-graph.md) <br>
- [Memory Protocol](references/memory-protocol.md) <br>
- [Reasoning Engine](references/reasoning-engine.md) <br>
- [Strategy Output](references/strategy-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON, with optional Mermaid diagrams and shell commands for bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist graph JSON under ~/.ontology-pro/graphs when the memory manager script is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
