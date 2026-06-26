## Description: <br>
Wires the local-first memex MCP memory server into an OpenClaw gateway so OpenClaw sessions are captured, back-filled, and searchable by future agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sedelev](https://clawhub.ai/user/sedelev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run OpenClaw use this skill to install or reuse memex, configure local session capture, back-fill existing OpenClaw history, and expose memex search tools through the OpenClaw MCP configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent searchable records of OpenClaw conversations, including historical sessions, in a local memex SQLite database. <br>
Mitigation: Review before installing, back up memex.db if needed, and skip or manually approve back-fill and re-import steps when sensitive history should not be indexed. <br>
Risk: The skill changes local runtime state by installing or reusing memex, registering a daemon or LaunchAgent, and editing the OpenClaw MCP server configuration. <br>
Mitigation: Inspect the created service, LaunchAgent, OpenClaw config merge, and shell profile edits after installation; the skill's own guidance says it should not use sudo. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sedelev/install-memex) <br>
- [memex homepage](https://memex.parallelclaw.ai) <br>
- [memex-mvp npm package](https://www.npmjs.com/package/memex-mvp) <br>
- [memex-mvp source link](https://github.com/parallelclaw/memex-mvp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through local discovery, installation, daemon setup, OpenClaw MCP configuration, back-fill, restart, and verification steps.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
