## Description: <br>
Full-text search across structured Markdown documentation archives using SQLite FTS5 with BM25-ranked results and source URL extraction for citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carev01](https://clawhub.ai/user/carev01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and documentation-focused agents use this skill to index Markdown documentation archives and search them for technical facts, limitations, and source URLs for citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local search index can store and display the Markdown documents selected for indexing, including sensitive material if the wrong directory is indexed. <br>
Mitigation: Index only intended documentation directories, avoid secrets and mixed-sensitivity content, and use a dedicated database path. <br>


## Reference(s): <br>
- [Documentation Search Patterns](references/search-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and text, JSON, or Markdown search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results can include titles, source URLs, relevance scores, context snippets, and optional full content.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
