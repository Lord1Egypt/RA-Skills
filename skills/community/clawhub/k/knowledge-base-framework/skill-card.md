## Description:

KB Framework builds a local hybrid knowledge base for Markdown, PDF, OCR, and Obsidian content with SQLite, ChromaDB, line-level source pointers, and optional local LLM generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minenclown](https://clawhub.ai/user/minenclown)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to index local Markdown, PDF, and Obsidian content, run hybrid search with line-level source pointers, and generate LLM essences or reports from indexed material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and update flows can change the local environment or install host-wide OCR dependencies.

Mitigation: Review installer and updater behavior first, use a virtual environment with locked dependencies, and avoid sudo-level OCR installation unless host-wide packages are intended.

Risk: LLM processing and remote Ollama configuration can expose indexed content to an unintended model endpoint.

Mitigation: Keep Ollama bound to localhost unless a remote endpoint is explicitly trusted, and restrict indexed source paths to non-sensitive directories.

Risk: Obsidian writer and cleanup commands can modify or delete notes in a vault.

Mitigation: Back up the vault before using writer or cleanup commands and review target paths before running write operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minenclown/skills/knowledge-base-framework)
- [README](artifact/README.md)
- [Installation guide](artifact/INSTALL.md)
- [KB usage guide](artifact/HOW_TO_KB.md)
- [Transformers engine reference](artifact/kb/biblio/TRANSFORMERS_ENGINE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, search results, and JSON-like audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local file paths, line references, model or engine status, and generated knowledge summaries or reports.]

## Skill Version(s):

1.2.0 (source: server release metadata, SKILL.md, README.md, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
