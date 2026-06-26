## Description: <br>
Typed knowledge graph for structured agent memory and composable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create, query, link, and validate structured memory entities such as people, projects, tasks, events, documents, and credentials. It supports shared local state for composable skills through an append-only ontology graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain sensitive personal or project data across sessions and skills. <br>
Mitigation: Review stored entries under memory/ontology, avoid saving secrets or sensitive personal data, and keep delete or inspection workflows available. <br>
Risk: Broad activation can cause the skill to write shared memory during normal task or planning conversations. <br>
Mitigation: Prefer explicit user-directed write actions and confirm what will be stored before creating or linking ontology records. <br>


## Reference(s): <br>
- [Ontology Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, YAML, Python, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local ontology files under memory/ontology when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
