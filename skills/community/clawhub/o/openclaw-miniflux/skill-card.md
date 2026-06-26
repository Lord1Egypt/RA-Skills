## Description: <br>
Manage RSS feeds and entries on a Miniflux instance, including browsing feeds, reading articles, updating categories, subscribing or unsubscribing feeds, importing OPML, marking entries as read, and bookmarking articles through openclaw-miniflux-mcp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinhong2011](https://clawhub.ai/user/sinhong2011) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Miniflux users use this skill to connect an agent to a Miniflux RSS reader instance for feed browsing, article triage, subscription management, category management, and OPML import or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration is write-capable and can change RSS account state, including feeds, categories, entry read status, bookmarks, and OPML imports. <br>
Mitigation: Run the MCP server with --read-only for browsing-only workflows and confirm user intent before destructive or bulk write actions. <br>
Risk: Miniflux credentials or API tokens are required in local MCP configuration. <br>
Mitigation: Use a dedicated Miniflux API token when possible and store credentials only in the local MCP configuration. <br>
Risk: Users may install a helper binary before confirming its source. <br>
Mitigation: Verify the openclaw-miniflux-mcp binary source before installing, or prefer Cargo installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sinhong2011/openclaw-miniflux) <br>
- [openclaw-miniflux-mcp GitHub Releases](https://github.com/sinhong2011/openclaw-skill-miniflux/releases) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown instructions with JSON configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of configured MCP tools to read and, unless read-only mode is enabled, modify Miniflux feeds, categories, entries, bookmarks, and OPML data.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
