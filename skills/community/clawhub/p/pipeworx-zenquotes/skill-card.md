## Description: <br>
Inspirational quotes - random, daily quote of the day, or batch 50 at once from ZenQuotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to fetch inspirational quotes for meetings, newsletters, quote-of-the-day widgets, notifications, motivational feeds, and journaling applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a remote Pipeworx MCP gateway through an unpinned npm helper. <br>
Mitigation: Install only if you trust Pipeworx, review outbound network access, and pin mcp-remote to a specific version when tighter supply-chain control is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-zenquotes) <br>
- [Pipeworx ZenQuotes homepage](https://pipeworx.io/packs/zenquotes) <br>
- [Pipeworx ZenQuotes MCP gateway](https://gateway.pipeworx.io/zenquotes/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and bash examples; runtime tool calls return quote text with author metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented example and uses a remote MCP gateway for quote retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
