## Description:

Run, tune, and troubleshoot local Ollama models with reliable API patterns, Modelfiles, embeddings, and hardware-aware deployment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, verify, integrate, tune, and troubleshoot local or self-hosted Ollama workflows. It is especially suited for API usage, structured JSON output, Modelfile customization, embeddings, local RAG checks, and hardware-aware operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional persistent notes under ~/ollama/ could capture sensitive operational context if used carelessly.

Mitigation: Keep secrets, API keys, private documents, prompts, transcripts, and sensitive network details out of saved notes.

Risk: Remote Ollama exposure or optional cloud execution can move data outside the local runtime.

Mitigation: Require explicit user approval before remote exposure or cloud use, and document the intended trust boundary.

Risk: Model tags, runtime state, GPU usage, and API feature support can drift across hosts and releases.

Mitigation: Verify exact model tags and runtime facts with live Ollama commands before making reproducible or production-adjacent recommendations.

## Reference(s):

- [ClawHub Ollama Skill](https://clawhub.ai/ivangdavila/skills/ollama)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)
- [Ollama Documentation](https://ollama.com/)
- [Ollama API](https://ollama.com/api)
- [API Patterns](api-patterns.md)
- [Embeddings and RAG](embeddings-and-rag.md)
- [Modelfile Workflows](modelfile-workflows.md)
- [Operations and Performance](operations-and-performance.md)
- [Troubleshooting](troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands, HTTP examples, configuration snippets, and troubleshooting steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local API examples, model-tag recommendations, Modelfile patterns, and operational checklists.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
