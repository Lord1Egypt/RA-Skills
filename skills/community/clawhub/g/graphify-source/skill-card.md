## Description: <br>
Graphify Source helps agents build and query local knowledge graphs from code repositories, documents, images, video, and audio using a configured Llama.cpp-compatible workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peing111](https://clawhub.ai/user/peing111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn project source, documentation, and media into a queryable knowledge graph for architecture review, code exploration, semantic search, path tracing, and incremental updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says local-only claims conflict with instructions that require external LLM API keys for semantic extraction of code and documents. <br>
Mitigation: Review before installing and use only on projects and media you are comfortable exposing to the configured LLM provider unless a strict local-only mode is verified. <br>
Risk: The release is tagged as requiring sensitive credentials. <br>
Mitigation: Avoid proprietary code, secrets, regulated data, and private media until the provider, transmitted data, and opt-in controls are clearly documented. <br>


## Reference(s): <br>
- [Graphify Source ClawHub page](https://clawhub.ai/peing111/graphify-source) <br>
- [Graphify homepage](https://clawhub.ai/fantox/graphify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for graph build, update, watch, query, path, and explain workflows, plus expected graphify-out artifacts such as GRAPH_REPORT.md, graph.html, graph.json, and cache files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
