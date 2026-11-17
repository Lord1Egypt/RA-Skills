## Description:

Apply semantic ontology rules to knowledge graphs to infer new relationships, class memberships, and properties from explicit ontology definitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to reason over RDF/OWL-style ontology definitions, expand knowledge graphs with inferred class memberships and relationships, and validate semantic consistency while designing ontology-based applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment says the skill is a local ontology-reasoning helper with some overstated or incorrect reasoning examples.

Mitigation: Validate outputs against a trusted RDF/OWL reasoner before using results for production, compliance, medical, access-control, or policy decisions.

Risk: The bundled Python engine is a simplified helper rather than a complete RDF/OWL reasoner.

Mitigation: Use it for conceptual guidance or prototyping, and replace or cross-check it with established reasoning libraries for complete ontology semantics.

## Reference(s):

- [Ontology-Based Inference Helper Skill Page](https://clawhub.ai/fisa712/skills/ontology-based-inference-helper)
- [ClawHub Homepage](https://clawhub.com)
- [Ontology-Based Inference - Design Patterns & Strategies](references/ontology-patterns.md)
- [Ontology-Based Inference - Real-World Examples](examples/ontology-examples.md)
- [OntologyInferenceEngine implementation](scripts/ontology_inference_engine.py)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with Python code examples and configuration patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can describe inferred class memberships, derived relationships, materialized triples, semantic consistency results, and local Python helper usage.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
