## Description: <br>
Build, review, and debug OpenClaw plugins with the official plugin SDK, including plugin manifests, shipped skills, tools, hooks, slash commands, tests, and runtime availability issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pazyork](https://clawhub.ai/user/pazyork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, modify, review, test, package, and debug OpenClaw plugins. It helps choose the right plugin boundary, structure plugin files, register capabilities, validate manifests and runtime behavior, and diagnose why a plugin capability is present but unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or modified plugin code can change runtime behavior, manifests, tool exposure, hooks, commands, and shipped skills. <br>
Mitigation: Review generated code and configuration before installation, then validate manifest, registration, runtime reachability, and user-facing surface behavior. <br>
Risk: The bundled observability example can log session data if copied and installed, including prompts, model outputs, tool details, and telemetry records. <br>
Mitigation: Treat telemetry and session logs as sensitive, limit access to them, and disable or remove observability behavior when it is not required. <br>
Risk: Registered plugin tools may still be unavailable because runtime tool policy, allowlists, gateway state, or session snapshots can filter them. <br>
Mitigation: Inspect tool policy and plugin diagnostics, restart the gateway when required, and verify behavior in a real conversation surface after installation. <br>


## Reference(s): <br>
- [Official Documentation Entry Points](references/official-docs.md) <br>
- [Plugin Layout and Registration](references/plugin-layout-and-registration.md) <br>
- [Hooks and Event Types](references/hooks-and-events.md) <br>
- [Development, Testing, and Validation Workflow](references/testing-and-workflow.md) <br>
- [Pitfalls and Debugging Guide](references/pitfalls-and-debugging.md) <br>
- [In-Repo Example Map](references/example-map.md) <br>
- [Observability Lab Example](references/observability-lab-source/README.md) <br>
- [OpenClaw Building Plugins](https://docs.openclaw.ai/plugins/building-plugins) <br>
- [OpenClaw Plugin SDK Overview](https://docs.openclaw.ai/plugins/sdk-overview) <br>
- [OpenClaw Plugin Manifest](https://docs.openclaw.ai/plugins/manifest) <br>
- [OpenClaw Hooks Documentation](https://docs.openclaw.ai/automation/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and file-change recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include validation steps, packaging instructions, residual risk notes, and references to relevant OpenClaw documentation or artifact files.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
