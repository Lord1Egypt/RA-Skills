## Description: <br>
Search and browse Hacker News, including top stories, keyword search via Algolia, and individual item lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Hacker News, inspect current top stories, and retrieve individual stories or comments for research, monitoring, digests, and follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls external Hacker News-related services through the Pipeworx MCP gateway, so returned content may change over time or include untrusted public user-generated text. <br>
Mitigation: Review retrieved items before using them in published summaries, decisions, or downstream automation. <br>
Risk: The artifact declares a curl dependency and includes command examples that make network requests. <br>
Mitigation: Run commands only in an environment where outbound requests to the documented Pipeworx endpoint are acceptable. <br>


## Reference(s): <br>
- [Pipeworx Hacker News pack homepage](https://pipeworx.io/packs/hackernews) <br>
- [Pipeworx Hacker News MCP endpoint](https://gateway.pipeworx.io/hackernews/mcp) <br>
- [ClawHub skill listing](https://clawhub.ai/brucegutman/pipeworx-hackernews) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks when showing connection or API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Hacker News search results, top-story summaries, item details, and MCP connection guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
