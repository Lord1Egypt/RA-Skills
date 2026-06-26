## Description: <br>
Knowledge Rag turns local notes and documents into a searchable personal RAG knowledge base with natural-language search, indexing, and optional note saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54lynnn](https://clawhub.ai/user/54lynnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to index local .txt, .md, .pdf, and .docx documents, then search the resulting personal knowledge base through an agent, CLI, or local web interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The unauthenticated local web service can expose filesystem browsing and knowledge-index controls too broadly. <br>
Mitigation: Keep the service bound to localhost, avoid running it on untrusted networks, and stop it when not in use. <br>
Risk: Indexing personal documents can make sensitive or secret content searchable through the local knowledge base. <br>
Mitigation: Do not index secrets or highly sensitive files, and review save-to-knowledge-base actions before allowing persistence. <br>
Risk: Installation depends on local Ollama and package setup steps. <br>
Mitigation: Use verified Ollama and package installation steps rather than direct remote shell execution where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/54lynnn/knowledge-rag) <br>
- [54lynnn ClawHub profile](https://clawhub.ai/user/54lynnn) <br>
- [Ollama download](https://ollama.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local search result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local knowledge-base files and search indexes when the user asks to save or reindex content.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata; artifact frontmatter reports 1.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
