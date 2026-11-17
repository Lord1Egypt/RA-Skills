## Description:

Make Claude, Cursor, Cline, Continue, and Zed remember every AI conversation forever by guiding installation of memex, a local-first MCP memory server backed by a shared SQLite corpus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedelev](https://clawhub.ai/user/sedelev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MCP-compatible agent users use this skill to install and configure memex so AI conversation history, selected chat exports, and related local data can be indexed and searched across supported clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fast install path executes a remote installer and can modify local tool configuration.

Mitigation: Inspect the installer or use the documented manual path, review each command before execution, and confirm config changes before writing them.

Risk: The installed memory service can index sensitive AI conversations, chat exports, and local files selected through supported capture flows.

Mitigation: Confirm which sources will be watched, import sensitive chats only with explicit consent, and skip sources that should not be available to future agents.

Risk: Automatic context injection can surface prior conversation content to future agent sessions.

Mitigation: Decline or disable auto-context unless automatic memory injection is desired, and verify the installed hook or client behavior after setup.

Risk: Using sudo for global npm installation can expand the impact of a bad or compromised package install.

Mitigation: Prefer a user-level npm prefix or another non-sudo Node package management setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sedelev/skills/install-memex)
- [memex homepage](https://memex.parallelclaw.ai)
- [memex npm package](https://www.npmjs.com/package/memex-mvp)
- [memex source repository](https://github.com/parallelclaw/memex-mvp)
- [memex installer script](https://github.com/parallelclaw/memex-mvp/blob/main/docs/install.sh)
- [npm EACCES guidance](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing installation steps, consent prompts, verification commands, and MCP configuration guidance.]

## Skill Version(s):

1.5.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
