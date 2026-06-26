## Description: <br>
Installs memex, a local-first MCP memory server, and guides CLI agents through discovery, installation, MCP configuration, history backfill, and optional Telegram import. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sedelev](https://clawhub.ai/user/sedelev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to install memex locally, connect MCP-compatible clients, and index AI conversations into a searchable SQLite memory. It is intended for users who want cross-client memory and are comfortable reviewing shell commands and local configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fast path runs an unpinned remote installer. <br>
Mitigation: Inspect the installer first or use the manual npm installation path before allowing execution. <br>
Risk: The skill creates a persistent local database of AI and optional chat histories. <br>
Mitigation: Install only when persistent local memory is desired, and review what sources are indexed before enabling backfill or imports. <br>
Risk: Auto-capture and auto-context can expose prior local conversations to future agents. <br>
Mitigation: Consider declining the daemon or auto-context hook, and use explicit per-chat consent for Telegram imports. <br>
Risk: MCP client configuration changes can affect existing agent tool setup. <br>
Mitigation: Review MCP configuration diffs and preserve existing server entries when adding memex. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sedelev/install-memex) <br>
- [memex homepage](https://memex.parallelclaw.ai) <br>
- [memex GitHub repository](https://github.com/parallelclaw/memex-mvp) <br>
- [memex npm package](https://www.npmjs.com/package/memex-mvp) <br>
- [memex installer source](https://github.com/parallelclaw/memex-mvp/blob/main/docs/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are shown before execution; MCP client configuration is described as a merge rather than an overwrite.] <br>

## Skill Version(s): <br>
1.5.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
