## Description: <br>
Semantic knowledge base allowing ingest, search, and retrieval of saved texts, URLs, and files using embeddings and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OdinBot33](https://clawhub.ai/user/OdinBot33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to save notes, URLs, files, and text into a local semantic knowledge base and retrieve relevant context for questions or workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved content may persist locally and be processed by configured external AI providers. <br>
Mitigation: Do not save secrets, credentials, regulated data, or confidential documents unless local persistence and provider processing are acceptable. <br>
Risk: The security review notes a local PDF path code-execution issue. <br>
Mitigation: Avoid ingesting untrusted local PDF paths and review the skill before installation or execution. <br>
Risk: Sensitive local retrieval may expose more stored context than intended. <br>
Mitigation: Use search-only mode for sensitive retrieval and review returned context before using it in an answer. <br>


## Reference(s): <br>
- [OEE Knowledge Base RAG on ClawHub](https://clawhub.ai/OdinBot33/oee-knowledge-base) <br>
- [OdinBot33 publisher profile](https://clawhub.ai/user/OdinBot33) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search-only mode can return retrieved context without generating an LLM answer.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
