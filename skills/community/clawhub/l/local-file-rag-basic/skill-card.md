## Description: <br>
High-performance local File RAG suite for searching code and documents in a local workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjreliable](https://clawhub.ai/user/wjreliable) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to search local workspaces for relevant code and document snippets by query, optional target file, or selected root directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, extract, and cache contents from broad local directories selected by the user. <br>
Mitigation: Point rootDir only at intended project folders, avoid home directories or folders with secrets, and delete .storage/code-rag.db when the index is no longer needed. <br>
Risk: The skill can silently install npm packages for document parsing. <br>
Mitigation: Review and preinstall the npm dependencies before use where possible, and run the skill only in environments where package installation is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjreliable/local-file-rag-basic) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Metadata] <br>
**Output Format:** [Structured Markdown-style search results with skeletons, metadata, and clustered snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Indexes supported files under 20MB and caches a local SQLite index under the selected root.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
