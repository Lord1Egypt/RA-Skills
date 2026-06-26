## Description: <br>
Use when explaining Palantir Ontology concepts, guiding users to model a Foundry Ontology from scratch, parsing Feishu or local documents to extract business entities, or designing Object Types, Link Types, Action Types, Functions, and Interfaces for a Foundry implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theosunny](https://clawhub.ai/user/theosunny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and Foundry implementation teams use this skill to learn Palantir Ontology concepts, extract ontology candidates from business materials, and produce implementation-ready object, link, action, function, and interface designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive business documents and save full raw copies locally. <br>
Mitigation: Use only documents the user is allowed to process, scope file access to narrow files or folders, and delete generated raw_source files when finished. <br>
Risk: Generated HTML can include content derived from untrusted documents. <br>
Mitigation: Review generated HTML before opening it in a browser or sharing it with others. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theosunny/ontology-modeling) <br>
- [Object Type reference](reference/object-type.md) <br>
- [Link Type reference](reference/link-type.md) <br>
- [Action Type reference](reference/action-type.md) <br>
- [Function reference](reference/function.md) <br>
- [Interface reference](reference/interface.md) <br>
- [Project management ontology example](reference/example-project-mgmt.md) <br>
- [Visualization template](reference/visualization-template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated JSON, Markdown, OWL/Turtle, and HTML ontology artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create ontology files and raw-source notes under an ontology directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
