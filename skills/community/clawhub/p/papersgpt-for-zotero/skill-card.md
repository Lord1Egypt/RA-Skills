## Description:

A privacy-first, local-first search assistant and MCP server for your Zotero library, enabling AI agents to search and analyze your research papers securely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[papersgpt](https://clawhub.ai/user/papersgpt)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and AI-agent users use this skill to search and synthesize information from their local Zotero papers, PDFs, and academic notes. It supports literature reviews and targeted lookups within the user's own document collection, not public web search or general knowledge answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned external npm package that indexes private local Zotero documents in a background process.

Mitigation: Review and trust the npm package before installing, prefer a pinned version from a verified source, and limit access to the intended Zotero directory.

Risk: Indexed papers or notes may contain sensitive research material.

Mitigation: Check where indexes are stored, whether the package uses the network, and how indexed data can be deleted before pointing it at private content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/papersgpt/skills/papersgpt-for-zotero)
- [PapersGPT for Zotero repository](https://github.com/papersgpt/papersgpt-for-zotero)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search queries, local command suggestions, retrieved context snippets, and synthesized research guidance.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
