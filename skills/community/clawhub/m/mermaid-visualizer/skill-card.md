## Description:

Transform text content into professional Mermaid diagrams for presentations and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axtonliu](https://clawhub.ai/user/axtonliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation teams use this skill to turn processes, architectures, comparisons, mind maps, sequences, and state transitions into Mermaid diagrams. The skill is suited for presentation and documentation workflows where Markdown-renderable diagrams are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger language can cause the agent to choose Mermaid output when another visual format was intended.

Mitigation: Explicitly name the desired output format when requesting Mermaid, Excalidraw, Canvas, or another visualization type.

Risk: Generated diagrams may be inaccurate or misleading if the source text is ambiguous or the model misreads relationships.

Mitigation: Review generated diagrams before using them in documentation or presentations.

## Reference(s):

- [Mermaid Syntax Rules Reference](references/syntax-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/axtonliu/skills/mermaid-visualizer)
- [Publisher Profile](https://clawhub.ai/user/axtonliu)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Mermaid code fences and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagram source intended for Mermaid-compatible renderers such as Obsidian and GitHub.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
