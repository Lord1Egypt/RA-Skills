## Description: <br>
A local-first knowledge-base maintenance and retrieval skill for knowledge workers, with PPT/PDF support, keyword plus AI semantic retrieval, and progressive description evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kittitys](https://clawhub.ai/user/kittitys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers, consultants, and developers use this skill to initialize and query local document collections, locate relevant files, and produce cited answers from supported local formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local indexes and extracted-text caches may contain sensitive document content or path metadata. <br>
Mitigation: Install only for folders you are comfortable indexing locally, keep the workspace in a trusted location, and inspect or clean caches when needed. <br>
Risk: Selected file content may be passed to the user's chosen LLM provider during semantic analysis. <br>
Mitigation: Use only trusted or approved model providers, and avoid sensitive client or regulated documents unless that provider is approved for the data. <br>
Risk: Dependency setup or repair can require package installation commands. <br>
Mitigation: Review any dependency-install prompt before approving it; ordinary search should not silently install dependencies. <br>
Risk: Indexing or searching files in cloud-synced folders may trigger local downloads of online-only files. <br>
Mitigation: Confirm the source and workspace paths before initialization and account for cloud-sync behavior before indexing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kittitys/local-knowledge-retrieval) <br>
- [Project homepage](https://github.com/kittitys/knowledge-retrieval) <br>
- [Knowledge base conventions](references/knowledge-base-conventions.md) <br>
- [Phase execution](references/phase-execution.md) <br>
- [File handling](references/file-handling.md) <br>
- [Environment setup](references/environment-setup.md) <br>
- [Degradation behavior](references/degradation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown responses with source citations, plus local index and cache files when initialized.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local knowledge-base metadata, BM25 indexes, extracted-text caches, and shortcuts after user confirmation.] <br>

## Skill Version(s): <br>
3.2.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
