## Description: <br>
Open Ontologies helps agents build, validate, query, and govern RDF/OWL ontologies and knowledge graphs with 39+ MCP tools backed by an in-memory Oxigraph triple store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabio-rovai](https://clawhub.ai/user/fabio-rovai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, ontology engineers, and knowledge-graph practitioners use this skill to generate, validate, query, evolve, align, and persist RDF/OWL ontologies through the Open Ontologies MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Open Ontologies MCP server binary. <br>
Mitigation: Install the server only from the intended cargo package or GitHub release, and review the binary before using it with sensitive data. <br>
Risk: User-directed pull and push actions can contact remote ontology URLs or SPARQL endpoints. <br>
Mitigation: Require explicit confirmation before fetching from remote sources or pushing triples to a SPARQL endpoint. <br>
Risk: Ontology lifecycle actions can save datasets, create versions, or apply production ontology changes. <br>
Mitigation: Review planned changes and avoid saving, versioning, or applying sensitive or production datasets without approval. <br>


## Reference(s): <br>
- [Open Ontologies ClawHub page](https://clawhub.ai/fabio-rovai/open-ontologies) <br>
- [Open Ontologies releases](https://github.com/fabio-rovai/open-ontologies/releases) <br>
- [W3C OWL Wine ontology example](https://www.w3.org/TR/owl-guide/wine.rdf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code, ontology, SPARQL, shell, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local MCP server; ontology files or versions are persisted only when the user requests save or version actions.] <br>

## Skill Version(s): <br>
0.5.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
