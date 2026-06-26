## Description: <br>
A privacy-first, local-first search assistant and MCP server for your Zotero library, enabling AI agents to search and analyze your research papers securely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[papersgpt](https://clawhub.ai/user/papersgpt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and agents use this skill to search, analyze, and synthesize information from a local Zotero library during literature reviews and paper-focused research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to install and run an external tool that indexes a private local Zotero library. <br>
Mitigation: Install only from a trusted package source and verify indexing scope, storage locations, log retention, deletion steps, and access boundaries before use. <br>
Risk: Research results may expose sensitive collections, notes, or PDF contents to connected agents. <br>
Mitigation: Limit agent access to trusted clients, exclude sensitive collections where possible, and review retrieved snippets before sharing or citing them. <br>


## Reference(s): <br>
- [PapersGPT for Zotero project repository](https://github.com/papersgpt/papersgpt-for-zotero) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and research workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and synthesis guidance should be verified against the user's Zotero library before citation or reuse.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; skill frontmatter says 0.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
