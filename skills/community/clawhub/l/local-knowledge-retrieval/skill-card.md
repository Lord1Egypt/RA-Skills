## Description:

A local-first document search skill with PPT/PDF support, dual-channel retrieval through keyword and AI semantic search, and progressive description evolution for large local file collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kittitys](https://clawhub.ai/user/kittitys)

### License/Terms of Use:

MIT-0

## Use Case:

External users, consultants, knowledge workers, and agents use this skill to create a local knowledge base from user-approved folders and answer questions with cited retrieval from PDFs, PPTX, DOCX, spreadsheets, images, and text files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local files and stores extracted text caches and source paths for approved folders.

Mitigation: Use it only on folders the user is authorized to process, and review or clear generated caches when documents are sensitive.

Risk: Selected file contents may be sent to the model provider chosen by the user during semantic analysis or answer generation.

Mitigation: Use an approved model provider for sensitive material and avoid indexing folders whose contents cannot be shared with that provider.

Risk: Dependency installation changes the local Python environment.

Mitigation: Install only the listed pinned packages after explicit user approval.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kittitys/skills/local-knowledge-retrieval)
- [Project homepage](https://github.com/kittitys/knowledge-retrieval)
- [Environment setup](artifact/references/environment-setup.md)
- [Knowledge base conventions](artifact/references/knowledge-base-conventions.md)
- [Phase execution](artifact/references/phase-execution.md)
- [File handling](artifact/references/file-handling.md)
- [Degradation and cleanup](artifact/references/degradation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance and answers with cited sources, plus JSON output from helper search scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local manifests, BM25 indexes, shortcut links, and extracted-text caches under knowledge-base after user approval.]

## Skill Version(s):

3.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
