## Description:

Wires the local-first memex MCP memory server into an OpenClaw gateway, installs or reuses the memex-mvp daemon, back-fills OpenClaw sessions into a local SQLite and FTS5 corpus, and exposes memex search and retrieval tools to the OpenClaw LLM toolset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedelev](https://clawhub.ai/user/sedelev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running OpenClaw use this skill to add persistent local memory: captured sessions, back-filled history, and MCP search tools backed by memex. It is intended for Linux or macOS OpenClaw deployments, including workstations, VPS hosts, self-hosted OpenClaw, and Moonshot Kimi-Claw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent user-level service continuously indexes OpenClaw conversations into a local memex database.

Mitigation: Install only when continuous local session capture is intended; review the generated systemd user service or LaunchAgent before enabling it, and document disable, uninstall, and data-deletion steps.

Risk: The skill installs memex-mvp from npm using a mutable latest package reference when memex is not already present or needs upgrade.

Mitigation: Prefer a pinned, verified memex-mvp version for controlled deployments and review the package source and checksum before installation.

Risk: PATH changes and OpenClaw MCP configuration edits could affect future shell sessions or gateway behavior.

Mitigation: Confirm shell rc changes before relying on them, verify that OpenClaw configuration is merged rather than overwritten, and run the skill's MCP listing and fresh-session checks after restart.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sedelev/skills/install-memex-claw)
- [memex homepage](https://memex.parallelclaw.ai)
- [memex-mvp npm package](https://www.npmjs.com/package/memex-mvp)
- [Related install-memex skill](https://clawhub.ai/sedelev/install-memex)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks the agent to run discovery, installation, configuration, migration, and verification steps with concise human-facing status output.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
