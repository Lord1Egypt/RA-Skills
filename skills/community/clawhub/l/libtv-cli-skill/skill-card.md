## Description:

Guides an agent to install and use the LibTV CLI to operate LibTV canvases, workspaces, projects, nodes, groups, models, uploads, and generated media workflows from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgm327](https://clawhub.ai/user/kgm327)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need an agent to run LibTV CLI workflows instead of inventing HTTP requests or relying on web UI steps. It covers installing the CLI, logging in, selecting workspaces and canvases, creating and modifying nodes and groups, uploading assets, searching models, and running image, script, and media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and update steps can run unverified code downloaded from LibTV release endpoints and make persistent local PATH changes.

Mitigation: Prefer version-pinned installers with published checksums or signatures, and review installer commands before execution.

Risk: The CLI stores active credentials under LIBTV_CONFIG_DIR and can upload files or create, modify, run, and delete LibTV canvas content.

Mitigation: Keep the LibTV config directory private, use isolated config directories for testing, and review workspace, project, and group bindings before running mutating commands.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kgm327/skills/libtv-cli-skill)
- [LibTV web interface](https://www.liblib.art/tv/zh)
- [LibTV CLI installation guide](artifact/scripts/install.md)
- [LibTV CLI command map](artifact/SKILL.md)
- [Model schema reference](artifact/model-schema/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and command reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some guided CLI commands produce JSON or NDJSON; login and project selection write local LibTV state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
