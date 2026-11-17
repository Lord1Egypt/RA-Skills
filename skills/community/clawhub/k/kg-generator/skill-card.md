## Description:

Generates knowledge graphs from user-provided local file or web URLs, producing RDF-Turtle by default and JSON-LD or other RDF serializations on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kidehen](https://clawhub.ai/user/kidehen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-graph practitioners use this skill to convert web pages, documents, articles, reports, and business analysis content into structured semantic data. It is suited for generating RDF-Turtle, JSON-LD, schema.org descriptions, identifier patterns, FAQ sections, glossary terms, and HowTo structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to fetch arbitrary user-supplied web URLs and local file paths, which may expose sensitive files, credential-bearing pages, or internal services.

Mitigation: Require user confirmation before fetching or saving content, prefer trusted public URLs or non-sensitive local files, and avoid internal services and credential-bearing pages.

Risk: Generated RDF-Turtle or JSON-LD may contain syntax errors or misleading semantic assertions if source extraction or entity modeling is wrong.

Mitigation: Validate the requested serialization before delivery and review generated entities, identifiers, and cross-references before relying on the graph.

## Reference(s):

- [Publisher Profile](https://clawhub.ai/user/kidehen)
- [Skill Page](https://clawhub.ai/kidehen/skills/kg-generator)
- [schema.org](http://schema.org)
- [US Census Bureau NAICS Lookup Pattern](https://www.census.gov/naics/?input={code}&year=2022&details={code})
- [SPARQL 1.1 Overview](https://www.w3.org/TR/sparql11-overview/)
- [Identifier Patterns](references/identifier-patterns.md)
- [NAICS Identifier Pattern Reference](references/naics-identifier-pattern.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown with RDF-Turtle, JSON-LD, or other RDF serialization code blocks; optional saved .ttl or .jsonld files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to be syntax-validated for the requested RDF serialization before delivery.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
