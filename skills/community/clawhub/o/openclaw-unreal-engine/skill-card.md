## Description: <br>
Integrates OpenClaw with Unreal Engine 5.x projects, editors, and plugins for automation scaffolding, UE5 C++ plugin work, Blueprint-callable nodes, editor or runtime connections, Remote Control workflows, and version-adapted UE 5.0+ guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droidhackzor](https://clawhub.ai/user/droidhackzor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design and scaffold OpenClaw integrations for Unreal Engine 5.x projects, including editor automation, Blueprint-facing workflows, runtime task transport, and plugin deployment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can overwrite an existing Plugins/OpenClawUnrealPlugin folder. <br>
Mitigation: Review the installer before use and back up any existing plugin directory before copying the scaffold into a project. <br>
Risk: The integration handles API keys or tokens for OpenClaw communication. <br>
Mitigation: Use HTTPS or strictly localhost-only non-production tokens, and do not commit API keys in Unreal project assets or configuration. <br>
Risk: Remote editor actions and telemetry can mutate or expose project state. <br>
Mitigation: Define explicit limits for remote editor actions, telemetry, and destructive operations before using the skill in a real project. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/droidhackzor/openclaw-unreal-engine) <br>
- [architecture.md](references/architecture.md) <br>
- [blueprints.md](references/blueprints.md) <br>
- [install-strategy.md](references/install-strategy.md) <br>
- [openclaw-api-contract.md](references/openclaw-api-contract.md) <br>
- [remote-control-notes.md](references/remote-control-notes.md) <br>
- [repo-evaluation-notes.md](references/repo-evaluation-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, JSON examples, shell commands, and generated Unreal Engine plugin files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce project plugin scaffolds, reference documentation, installation commands, and Unreal/OpenClaw task protocol examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
