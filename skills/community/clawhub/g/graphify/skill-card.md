## Description:

AI coding assistant skill for building and querying knowledge graphs from codebases, docs, and media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantox](https://clawhub.ai/user/fantox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Graphify to generate and query knowledge graphs for unfamiliar codebases, architecture analysis, impact tracing, and context sharing with AI coding assistants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Semantic extraction can send selected documents, PDFs, or images to an external LLM provider when an API key is configured.

Mitigation: Use only intended API keys and review inputs before semantic extraction; AST code extraction and Whisper transcription can run without those API keys.

Risk: Generated knowledge graphs may include sensitive files if the project is indexed without exclusions.

Mitigation: Create a .graphifyignore that excludes secrets, credentials, caches, build output, dependency directories, and other high-noise or sensitive paths before indexing.

Risk: URL ingestion and assistant or git hook installation can add external content or project-local automation.

Mitigation: Run URL ingestion and assistant or git hook setup only when those project-scoped changes are intended.

Risk: The installed graphify package is external to the skill artifact.

Mitigation: Install in a virtual environment and review the graphify package provenance and version before use.

## Reference(s):

- [Graphify API Reference](artifact/references/api_reference.md)
- [ClawHub skill page](https://clawhub.ai/fantox/skills/graphify)
- [Graphify project homepage](https://github.com/safishamsi/graphify)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and references to generated graph artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference graphify-out/GRAPH_REPORT.md, graphify-out/graph.json, graph.html, and optional export files produced by the graphify CLI.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
