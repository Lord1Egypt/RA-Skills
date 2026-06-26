## Description: <br>
Layered memory orchestration for OpenClaw conversations that helps implement or maintain systems for domain classification, preference and decision capture, long-term knowledge objects, summary-first recall, and periodic memory reflection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jl1914](https://clawhub.ai/user/jl1914) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or maintain an inspectable local memory system for OpenClaw conversations, including memory gating, classification, capture, summary-first recall, and periodic reflection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived preferences, decisions, and background facts in local memory files. <br>
Mitigation: Use a dedicated MEMORY_ROOT, review the memory directory periodically, and avoid automatic capture of secrets or highly sensitive personal data without deletion, retention, and redaction controls. <br>
Risk: Memory files are read from and written to the workspace, so an incorrect storage path can mix project data with long-term memory state. <br>
Mitigation: Set MEMORY_ROOT explicitly to a scoped directory before enabling capture, recall, or reflection workflows. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Architecture](ARCHITECTURE.md) <br>
- [Examples](EXAMPLES.md) <br>
- [Roadmap](ROADMAP.md) <br>
- [File Layout](references/file-layout.md) <br>
- [Object Models](references/object-models.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Reflection](references/reflection.md) <br>
- [Retrieval Strategy](references/retrieval-strategy.md) <br>
- [ClawHub Release Page](https://clawhub.ai/jl1914/mem-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, Python scripts, YAML memory files, Markdown logs, and compact JSON recall payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local workspace files for memory state and supports MEMORY_ROOT to point storage at a dedicated directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
