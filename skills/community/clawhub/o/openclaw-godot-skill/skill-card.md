## Description:

Controls the Godot Editor via OpenClaw for scene management, node manipulation, input simulation, debugging, screenshots, and editor control in trusted local projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomleelive](https://clawhub.ai/user/tomleelive)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game engineers use this skill to operate a local Godot 4.x editor through OpenClaw for scene inspection, node creation and editing, gameplay input simulation, logs, screenshots, and editor state checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed gateway extension can mutate Godot projects through scene saves, node deletion, input simulation, and script or project inspection.

Mitigation: Install only on trusted local machines and projects, keep version control or backups available, and confirm state-changing editor operations before running them.

Risk: The security summary flags an under-protected HTTP control channel in some configurations.

Mitigation: Keep the bridge bound to localhost and do not expose the gateway or bridge port on shared or public networks.

Risk: The installer writes into the local OpenClaw extension directory and may overwrite an existing Godot extension.

Mitigation: Review the existing ~/.openclaw/extensions/godot contents before running the installer.

Risk: The skill can expose project names, engine version, scene structure, script contents, and screenshots to the connected agent.

Mitigation: Use only with projects whose contents may be shared with the active agent session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomleelive/skills/openclaw-godot-skill)
- [Project homepage](https://github.com/TomLeeLive/openclaw-godot-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands, code snippets, and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose editor actions that modify scenes, nodes, saved files, or gameplay state; state-changing actions should be confirmed before execution.]

## Skill Version(s):

1.2.10 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
