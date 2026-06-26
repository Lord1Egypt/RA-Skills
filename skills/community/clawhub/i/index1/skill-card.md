## Description: <br>
AI memory system for coding agents - code index plus cognitive facts, persistent across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gladego](https://clawhub.ai/user/gladego) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and coding agents use this skill to index project code and documents, retrieve relevant code or cognitive facts through MCP tools, and record durable project knowledge across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or updating the third-party package can execute code from a package source. <br>
Mitigation: Use pipx or another trusted package path and verify package provenance before installation. <br>
Risk: The optional Ollama setup uses a remote curl-to-shell installer command. <br>
Mitigation: Avoid running the optional installer unless the source is trusted and the command has been reviewed. <br>
Risk: Project indexing and persistent learned facts may capture sensitive files or decisions if the scope is too broad. <br>
Mitigation: Limit indexing to intended project folders, exclude secrets, and periodically review or clear persistent learned facts. <br>


## Reference(s): <br>
- [ClawHub index1 skill page](https://clawhub.ai/gladego/index1) <br>
- [Ollama installer referenced for optional multilingual enhancement](https://ollama.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP setup, indexing commands, search rules, and operational guidance for persistent code and fact retrieval.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
