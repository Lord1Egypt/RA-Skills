## Description:

Hippocampus Memory Engine helps agents build and maintain an external memory store by vectorizing scattered memory sources, supporting retrieval, distillation, visualization, Obsidian sync, and optional GitHub publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzx11223344](https://clawhub.ai/user/wzx11223344)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain a persistent local memory system for conversation summaries, knowledge files, RAG retrieval, visual knowledge maps, and Obsidian synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic capture and long-term reuse of conversation and memory data can persist sensitive or unwanted content.

Mitigation: Before enabling daily sync or session-end capture, confirm what will be written, exclude sensitive content, and verify how stored memories can be reviewed and deleted.

Risk: Optional publishing or synchronization behavior could expose memory content outside the local workspace if enabled.

Mitigation: Review GitHub or Obsidian synchronization settings before use and confirm whether memory files are pushed, published, or shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzx11223344/skills/hippocampus-memory-engine)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown with PowerShell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or update of local memory files, HTML/SVG visualizations, Obsidian exports, and synchronization outputs.]

## Skill Version(s):

1.1.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
