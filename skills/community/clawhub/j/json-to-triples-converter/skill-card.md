## Description:

Convert JSON documents into RDF triples or graph-ready subject-predicate-object statements for knowledge graphs and semantic databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to convert JSON datasets and API payloads into RDF triples, JSON-LD, or graph-ready node and edge structures for semantic web, linked data, and knowledge graph ingestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Turtle or N-Triples from crafted or untrusted JSON can be unsafe for a production RDF store.

Mitigation: Add standards-compliant literal escaping, URI encoding, datatype and language validation, and parser validation before RDF ingestion.

Risk: The bundled converter is suitable only as a prototype or internal-data utility until reviewed.

Mitigation: Review converter behavior before production deployment and limit use to trusted or internal JSON data until hardening is complete.

## Reference(s):

- [Conversion Patterns](artifact/references/conversion-patterns.md)
- [Example Conversions](artifact/examples/example-conversions.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/json-to-triples-converter)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with RDF Turtle, N-Triples, JSON-LD, Graph JSON, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces graph-ready subject-predicate-object outputs; parser validation is recommended before RDF store ingestion.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
