## Description:

Generates Mermaid and ASCII diagrams of palace structure, knowledge topology, and synapse connectivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and memory-palace users use the skill to inspect or present knowledge-graph structure, entity relationships, and synapse strength as Mermaid or ASCII diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mermaid diagram content may be sent to Mermaid Chart without warning or approval; the security scan was incomplete and did not establish that all behavior was inspected.

Mitigation: Review the rendering flow before use and avoid sending sensitive knowledge-graph content to Mermaid Chart; use the ASCII output when external rendering is unsuitable.

## Reference(s):

- [Memory Palace project (metadata homepage)](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)
- [Palace Diagram release on ClawHub](https://clawhub.ai/athola/skills/nm-memory-palace-palace-diagram)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Mermaid flowchart syntax or ASCII text diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can describe a palace map, entity graph, synapse heatmap, or ASCII overview.]

## Skill Version(s):

1.10.3 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
