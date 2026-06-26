## Description: <br>
Apply semantic ontology rules to knowledge graphs to infer new relationships, class memberships, and properties from explicit RDF/OWL ontology definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge graph engineers use this skill to apply RDF/OWL-style ontology rules, materialize inferred triples, validate semantic consistency, and choose inference strategies for semantic web and graph applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cyclic ontology relationships or transitive rules can cause repeated inference or excessive closure growth. <br>
Mitigation: Detect cycles, set depth and iteration limits, and validate ontology structure before materializing inferred facts. <br>
Risk: Large ontologies can produce too many inferred facts for available memory or query latency targets. <br>
Mitigation: Use selective materialization, caching, incremental updates, and an inference strategy that matches the workload. <br>
Risk: Domain, range, or hierarchy mismatches can produce misleading semantic classifications. <br>
Mitigation: Run semantic consistency checks, review inferred facts against expected domain constraints, and test with representative sample data. <br>


## Reference(s): <br>
- [Ontology Patterns](artifact/references/ontology-patterns.md) <br>
- [Ontology Examples](artifact/examples/ontology-examples.md) <br>
- [Ontology Inference Engine](artifact/scripts/ontology_inference_engine.py) <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/ontology-based-inference-helper) <br>
- [ClawHub Homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and structured inference outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce inferred class memberships, derived relationships, materialized triples, semantic consistency findings, and ontology reasoning implementation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
