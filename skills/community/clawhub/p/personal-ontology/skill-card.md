## Description:

Help users build and maintain a Personal Ontology: a graph of identity, beliefs, predictions, goals, projects, and relationships that supports aligned agent assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levineam](https://clawhub.ai/user/levineam)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to bootstrap and maintain a Markdown-based personal ontology from notes, goals, projects, and reflections. The skill helps agents surface candidate ontology objects, validate links, flag stale or contradictory entries, and produce reviewable updates before writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt an agent to scan highly personal notes, journals, tasks, and calendar context.

Mitigation: Limit access to selected folders and sources, exclude sensitive notes, and confirm consent before scanning.

Risk: Ontology updates could preserve inaccurate or overly revealing interpretations of private material.

Mitigation: Review all extracted candidates before writes, keep suggestions separate until confirmed, and avoid saving verbatim private quotes unless needed.

Risk: Generated Mermaid or SVG views may include imported or shared note content.

Mitigation: Treat rendered diagrams as untrusted when based on shared content and review them before opening or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/levineam/skills/personal-ontology)
- [README](artifact/README.md)
- [Setup guide](artifact/SETUP.md)
- [Bootstrap workflow](artifact/bootstrap.md)
- [Categorization and validation heuristics](artifact/heuristics.md)
- [Guided prompts](artifact/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, ontology files, Mermaid graph code, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update local ontology Markdown files after user confirmation and can emit Mermaid, ASCII, or SVG visualization output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
