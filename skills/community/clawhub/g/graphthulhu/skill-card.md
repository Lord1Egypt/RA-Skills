## Description: <br>
Knowledge graph MCP server for Logseq and Obsidian. 37 tools for reading, writing, searching, and analyzing your second brain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skridlevsky](https://clawhub.ai/user/skridlevsky) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to configure an MCP server that lets an agent read, write, search, and analyze a selected Logseq or Obsidian knowledge graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent read-write access to the configured Obsidian vault or Logseq graph. <br>
Mitigation: Use it only with graphs you intend the agent to access, keep backups or version control, and review destructive or bulk-edit requests before approval. <br>
Risk: The Logseq setup uses an API token for local graph access. <br>
Mitigation: Protect the Logseq token, keep the API bound to localhost, and avoid configuring vaults or graphs that contain unrelated secrets. <br>
Risk: The workflow depends on an external graphthulhu binary. <br>
Mitigation: Install only if you trust the binary and the configured graph access model. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skridlevsky/graphthulhu) <br>
- [graphthulhu GitHub repository](https://github.com/skridlevsky/graphthulhu) <br>
- [Full tool reference](https://github.com/skridlevsky/graphthulhu#tools) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown, Code] <br>
**Output Format:** [Markdown with JSON configuration snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external graphthulhu binary and access to a configured Obsidian vault or Logseq graph.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
