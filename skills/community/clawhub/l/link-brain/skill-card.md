## Description: <br>
Local knowledge base for links. Save URLs with summaries and tags, search later using natural language, build collections, and review your backlog with spaced repetition. Includes a standalone HTML graph view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jakes420](https://clawhub.ai/user/jakes420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to turn saved URLs, browser bookmarks, and exported reading history into a local searchable knowledge base with summaries, tags, collections, review queues, and standalone HTML views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quickstart can read and import local browser bookmarks into a local database. <br>
Mitigation: Use setup or individual scan commands first when the user wants to review detected sources before importing. <br>
Risk: Auto-save fetches URL content from the user's machine to summarize and tag pages locally. <br>
Mitigation: Use auto-save only for URLs the user is comfortable having the local tool fetch; use manual save with provided title, summary, and tags otherwise. <br>


## Reference(s): <br>
- [Link Brain usage examples](references/examples.md) <br>
- [Link Brain v4.0.0 release notes](references/v4.0.0-release-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON command output, and generated local Markdown or HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data locally under ~/.link-brain/ by default; LINK_BRAIN_DIR can override the data directory.] <br>

## Skill Version(s): <br>
4.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
