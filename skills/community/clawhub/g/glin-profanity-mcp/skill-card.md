## Description: <br>
MCP server providing profanity detection tools for AI assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegdsks](https://clawhub.ai/user/thegdsks) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, moderators, and content teams use this MCP server to review batches of user content, audit comments, validate content before publishing, and support human-in-the-loop moderation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User tracking tools can build moderation profiles without documented storage, deletion, or access controls. <br>
Mitigation: Before enabling tracking tools, confirm data storage location, retention period, access permissions, and deletion or correction workflows for moderation history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thegdsks/glin-profanity-mcp) <br>
- [npm package: glin-profanity-mcp](https://www.npmjs.com/package/glin-profanity-mcp) <br>
- [GitHub package source](https://github.com/GLINCKER/glin-profanity/tree/release/packages/mcp) <br>
- [npm package: glin-profanity](https://www.npmjs.com/package/glin-profanity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration snippets, shell commands, and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce moderation findings, censored text, safety scores, corpus summaries, language lists, regex patterns, and user-tracking summaries depending on the selected MCP tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
