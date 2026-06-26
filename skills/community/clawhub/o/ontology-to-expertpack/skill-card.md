## Description: <br>
Convert an Ontology skill knowledge graph into a structured ExpertPack for migration from an entity/relation graph to a portable ExpertPack format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianhearn](https://clawhub.ai/user/brianhearn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert an OpenClaw Ontology graph.jsonl, and optionally schema.yaml, into an ExpertPack directory for review, refinement, and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ExpertPack files may include private or sensitive information from the input ontology graph. <br>
Mitigation: Review the generated Markdown and YAML before committing, publishing, or sharing the ExpertPack. <br>
Risk: Writing into an existing output directory can mix generated files with prior content. <br>
Mitigation: Choose a fresh or empty output directory for each conversion run. <br>
Risk: Documentation claims about Obsidian compatibility and YAML frontmatter may not match the generated output. <br>
Mitigation: Inspect the generated files and verify Obsidian/YAML behavior before relying on those features. <br>


## Reference(s): <br>
- [ExpertPack](https://expertpack.ai) <br>
- [ClawHub skill page](https://clawhub.ai/brianhearn/ontology-to-expertpack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown, YAML, and shell command guidance written into a local ExpertPack directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates manifest.yaml, overview.md, relations.yaml, glossary.md, category indexes, and content Markdown files from the supplied graph.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
