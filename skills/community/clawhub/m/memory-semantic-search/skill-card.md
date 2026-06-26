## Description: <br>
Semantic search over workspace markdown files using an OpenAI-compatible embedding API and SQLite vector store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toller892](https://clawhub.ai/user/toller892) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to index workspace Markdown notes and retrieve semantically related snippets for recall of notes, decisions, and surrounding context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed Markdown content and search queries can be sent to the configured embedding provider. <br>
Mitigation: Index the narrowest directory possible, avoid secrets or regulated data, and prefer a trusted or local embedding endpoint. <br>
Risk: The SQLite database can retain raw note text from indexed Markdown files. <br>
Mitigation: Delete or force-rebuild the database after sensitive edits and store the database only in an approved local location. <br>
Risk: The skill requires an embedding API credential. <br>
Mitigation: Use a dedicated API key with the least privileges available and rotate or revoke it if the workspace content scope changes. <br>


## Reference(s): <br>
- [Memory Semantic Search on ClawHub](https://clawhub.ai/toller892/memory-semantic-search) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text search results or JSON arrays, with Markdown usage guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes file paths, line ranges, similarity scores, and snippets from indexed Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
