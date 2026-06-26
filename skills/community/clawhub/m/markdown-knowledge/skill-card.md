## Description: <br>
Integrates a local Markdown knowledge base with OpenClaw for semantic search and context injection, retrieving only when the user explicitly asks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronjager92](https://clawhub.ai/user/aaronjager92) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to index a local folder of Markdown notes, search it on demand, and inject relevant snippets into an AI conversation. It is intended for personal or team knowledge retrieval where the user controls the local knowledge directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled configuration and index files may expose private notes, local paths, or API credentials. <br>
Mitigation: Remove bundled config.json and index.json before release or installation, rotate any exposed credentials, and rebuild the index from an intentionally selected knowledge directory. <br>
Risk: Markdown notes indexed by the skill may contain secrets or sensitive personal information that can be surfaced in search results. <br>
Mitigation: Keep secrets out of the configured knowledge directory, review indexed content before use, and restrict knowledge_path to documents intended for AI retrieval. <br>
Risk: The init workflow can download and install ripgrep automatically when it is missing. <br>
Mitigation: Install ripgrep separately from a trusted source or review the download behavior before running initialization. <br>


## Reference(s): <br>
- [Markdown Knowledge Base README](references/README.md) <br>
- [Markdown Knowledge Base Project Guide](references/PROJECT.md) <br>
- [ClawHub skill page](https://clawhub.ai/aaronjager92/markdown-knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown search summaries, JSON action results, CLI command output, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result count is controlled by search_top_k; results may include local file paths and document excerpts from the configured knowledge directory.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and ClawHub metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
