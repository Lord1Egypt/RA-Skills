## Description: <br>
Installs UI plugin architecture into OpenClaw, enabling plugins to register custom views, navigation items, and settings panels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw developers and maintainers use this skill to manually add UI plugin registration support so plugins can expose dashboard views, navigation groups, and settings panels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual installation changes gateway and UI source files in the target OpenClaw checkout. <br>
Mitigation: Confirm the intended checkout before installation, review the git diff, and keep a rollback path. <br>
Risk: Incorrect edits could break plugin registry, navigation, or UI build behavior. <br>
Mitigation: Follow the installation steps in order, then run the documented build and UI build checks before restarting the gateway. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/plugin-architecture) <br>
- [Installation instructions](artifact/INSTALL_INSTRUCTIONS.md) <br>
- [UI plugin registry reference](artifact/reference/ui-plugin-registry.ts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown installation guidance with TypeScript snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual source-code patch guidance; review the resulting git diff before applying changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release metadata; artifact SKILL.md lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
