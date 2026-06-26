## Description: <br>
Generate comprehensive Knowledge Graphs from file: or http(s): URLs as RDF-Turtle by default, or JSON-LD and other RDF serializations on request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kidehen](https://clawhub.ai/user/kidehen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and semantic web practitioners use this skill to convert web pages or local documents into standards-oriented knowledge graph outputs. It is suited for generating RDF-Turtle, JSON-LD, schema.org descriptions, identifier patterns, FAQs, glossaries, and structured analysis from user-provided URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read user-provided local file URLs, which can expose confidential document contents to the agent session. <br>
Mitigation: Use local file URLs only for documents intended for analysis, and avoid confidential files unless that access is deliberate. <br>
Risk: The skill can save generated RDF or JSON-LD files, creating persistent outputs in a user-selected or default directory. <br>
Mitigation: Confirm the output path before saving and review generated files before sharing or using them downstream. <br>


## Reference(s): <br>
- [Identifier Patterns](references/identifier-patterns.md) <br>
- [NAICS Identifier Pattern Reference](references/naics-identifier-pattern.md) <br>
- [Generic Knowledge Graph Prompt](prompts/generic-jsonld.md) <br>
- [Business & Market Analysis Prompt](prompts/business-market-analysis-turtle.md) <br>
- [Skill Page](https://clawhub.ai/kidehen/kg-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown containing RDF-Turtle, JSON-LD, or another requested RDF serialization in a single code block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally save generated .ttl or .jsonld files when the user requests a path or accepts the default save behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
