## Description: <br>
Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonnenberglauramarie-afk](https://clawhub.ai/user/sonnenberglauramarie-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate qmd for indexing local project or documentation folders and searching them with BM25, vector, hybrid, and MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing broad local directories can expose secrets or private data to the local qmd index. <br>
Mitigation: Index only specific project or documentation folders and avoid paths that contain credentials or private data. <br>
Risk: Ollama embedding and rerank requests could be sent to an untrusted endpoint if OLLAMA_URL is changed. <br>
Mitigation: Keep OLLAMA_URL pointed at a trusted local or managed endpoint. <br>
Risk: MCP mode can expose local search capabilities to connected clients. <br>
Mitigation: Run MCP mode only with trusted clients. <br>


## Reference(s): <br>
- [Max QMD Search on ClawHub](https://clawhub.ai/sonnenberglauramarie-afk/max-qmd) <br>
- [qmd package repository](https://github.com/tobi/qmd) <br>
- [qmd homepage](https://tobi.lutke.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
