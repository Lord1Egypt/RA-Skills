## Description: <br>
Guides users through creating, validating, and integrating custom OpenClaw plugins, tools, and commands using templates, scripts, examples, and reference material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcusy2k](https://clawhub.ai/user/marcusy2k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold OpenClaw plugins, understand the expected manifest and lifecycle structure, validate plugin metadata, and prepare plugins for installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or custom plugin code can persist and run inside OpenClaw after restart. <br>
Mitigation: Review plugin code, manifests, permissions, and behavior before installing; install only plugins whose permissions and behavior are understood. <br>
Risk: Local scaffolding commands create files in the selected output directory. <br>
Mitigation: Run scaffolding in an intended development directory and inspect generated files before integrating the plugin. <br>


## Reference(s): <br>
- [OpenClaw Plugin API Reference](references/api-reference.md) <br>
- [OpenClaw CLI Reference for Plugin Management](references/cli-reference.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash, JSON, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local plugin scaffold files when the initialization script is run by the agent or user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
