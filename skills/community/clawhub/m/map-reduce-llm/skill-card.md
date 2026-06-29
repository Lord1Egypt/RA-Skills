## Description: <br>
Structured Map-Reduce workflow for analyzing large documents with LLMs when the content exceeds the model's context window, covering intelligent chunking strategies, prompt templates, hierarchical and agentic variants, and quality control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-ht](https://clawhub.ai/user/alex-ht) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and engineers use this skill to analyze documents that exceed an LLM context window by chunking source material, processing chunks independently, and reducing the results into a traceable final synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive document chunks or intermediate outputs may be copied into LLM prompts, optional sub-agents, external lookups, or local files. <br>
Mitigation: Use only approved models, tools, storage locations, and sub-agent workflows for the data being analyzed. <br>
Risk: Final syntheses may contain unsupported cross-chunk connections or incorrect claims. <br>
Mitigation: Require chunk IDs or traceability for major claims and spot-check important conclusions against the original chunks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alex-ht/map-reduce-llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with prompt templates, command examples, and structured deliverable expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends saving chunks, map outputs, partial reductions, and traceability metadata for auditability.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
