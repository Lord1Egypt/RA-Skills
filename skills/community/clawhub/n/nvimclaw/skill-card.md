## Description:

Bridge to live Neovim over OpenClaw's node plugin. Use for reading or editing named and unnamed buffers, discovering open buffers, running surgical Ex substitutions, inspecting cursor/selection/diagnostics, and Neovim chat-to-session messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utrumsit](https://clawhub.ai/user/utrumsit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use nvimclaw to let an agent inspect and edit live Neovim buffers, read diagnostics, cursor, and selection state, and coordinate chat turns from inside Neovim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent controlled access to inspect and potentially edit live Neovim buffers, including sensitive editor content.

Mitigation: Install only when this editor access is intended, avoid sending chat turns from sensitive buffers, and disable or limit automatic context attachment when sensitive content should not be shared.

Risk: Privileged tools can mutate buffers or run destructive Ex commands.

Mitigation: Keep privileged tools disabled unless needed, require confirmation for destructive Ex commands, and use dry runs plus optimistic locks for buffer edits.

Risk: Broad command allowlists on shared gateways can expose newly added privileged Neovim tools before they are reviewed.

Mitigation: Prefer explicit command allowlists on shared gateways and approve node pairings only for trusted Neovim instances.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utrumsit/skills/nvimclaw)
- [nvimclaw plugin repository](https://github.com/utrumsit/nvimclaw)
- [vscode.openclaw reference implementation](https://github.com/xiaoyaner-home/openclaw-vscode/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, Vim, Lua, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON command parameters for OpenClaw node invocation.]

## Skill Version(s):

0.1.10 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
