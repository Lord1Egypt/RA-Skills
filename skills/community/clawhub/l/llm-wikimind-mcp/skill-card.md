## Description: <br>
Install and configure LLM-WikiMind MCP, a local Markdown knowledge-base server with BM25 search and MCP tools for search, reading, listing, ingestion, and domain discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hal-9909](https://clawhub.ai/user/hal-9909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this skill to set up a local MCP-backed personal wiki, register it with an MCP-compatible client, and keep Markdown knowledge indexed for retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup installs external code and the qmd dependency. <br>
Mitigation: Install only after reviewing and trusting the linked repository and dependency. <br>
Risk: Adopting a broad notes directory can expose more local Markdown content than intended to the MCP server. <br>
Mitigation: Choose a narrow wiki folder and avoid adopting sensitive note directories unless that access is intentional. <br>
Risk: Adding the watcher to ~/.zshrc starts background syncing in future shell sessions. <br>
Mitigation: Enable shell autostart only when persistent watcher behavior is desired. <br>


## Reference(s): <br>
- [LLM-WikiMind repository](https://github.com/HAL-9909/llm-wikimind) <br>
- [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [ClawHub skill page](https://clawhub.ai/hal-9909/llm-wikimind-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides setup steps, MCP client registration examples, verification commands, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
