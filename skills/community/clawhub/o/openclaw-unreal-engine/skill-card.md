## Description:

Integrate OpenClaw with Unreal Engine 5.x projects, editors, and plugins so an agent can inspect or scaffold Unreal automation, create UE5 C++ plugin surfaces, expose Blueprint-callable nodes, connect to editor or runtime sessions, and design version-adapted workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[droidhackzor](https://clawhub.ai/user/droidhackzor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical artists use this skill to plan and scaffold OpenClaw integrations for Unreal Engine 5.x projects, including editor automation through Remote Control and runtime or Blueprint-facing task flows through a lightweight plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled plugin can send bearer tokens and task data to arbitrary or plaintext OpenClaw endpoints.

Mitigation: Use HTTPS or WSS with trusted hosts, avoid production tokens in Blueprint-readable settings or config files, and rotate any token that may have been exposed.

Risk: The installer removes an existing OpenClawUnrealPlugin directory before copying the scaffold.

Mitigation: Run the installer only in a test or version-controlled Unreal project first, and review or back up the target plugin directory before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/droidhackzor/skills/openclaw-unreal-engine)
- [Unreal Engine + OpenClaw architecture](references/architecture.md)
- [Blueprint integration patterns](references/blueprints.md)
- [OpenClaw /api/unreal/task contract](references/openclaw-api-contract.md)
- [Install strategy: engine source vs project plugin](references/install-strategy.md)
- [Remote Control notes](references/remote-control-notes.md)
- [OpenClaw Unreal Plugin composition notes](assets/OpenClawUnrealPlugin/REFERENCES.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with C++, Unreal plugin files, JSON contract examples, and bash install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a drop-in Unreal plugin scaffold and project-plugin installation helper.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
