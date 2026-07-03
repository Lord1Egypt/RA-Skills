## Description: <br>
Bridge to Neovim over OpenClaw's node plugin. nvim.*: buffer R/W, Ex commands (surgical :substitute), cursor/selection/diagnostics, chat-to-session messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utrumsit](https://clawhub.ai/user/utrumsit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent inspect and edit files inside a live Neovim session through OpenClaw, including buffer reads and writes, Ex substitutions, cursor and selection inspection, diagnostics, and in-editor chat handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent read and write access to files open within the configured Neovim workspace. <br>
Mitigation: Use a narrow workspace_root, install only when the Neovim plugin is trusted, and keep privileged tools disabled unless edits are required. <br>
Risk: Privileged Ex commands and mutating buffer operations can change the user's editor state or project files. <br>
Mitigation: Review destructive Ex commands before confirming them, use dry-run substitutions where available, and rely on changedtick or line-hash preconditions for mutating operations. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/utrumsit/nvimclaw/tree/main/skills/nvimclaw) <br>
- [Plugin repo](https://github.com/utrumsit/nvimclaw) <br>
- [vscode.openclaw extension](https://github.com/xiaoyaner-home/openclaw-vscode/) <br>
- [ClawHub skill page](https://clawhub.ai/utrumsit/skills/nvimclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell, JSON, Lua, and Vim command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to guide an agent's use of OpenClaw node commands against a live Neovim workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
