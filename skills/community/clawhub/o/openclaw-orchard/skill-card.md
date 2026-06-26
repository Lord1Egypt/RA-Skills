## Description: <br>
Agentic project and task management plugin for OpenClaw. Persistent SQLite-backed task board with a queue runner that auto-dispatches ready tasks as subagents, REST API, native agent tools, and a web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derp42](https://clawhub.ai/user/derp42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use OrchardOS to manage agent projects, persist tasks and run history, and dispatch ready work to subagents through tools, API routes, and a web dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes admin-level controls and can dispatch subagents automatically. <br>
Mitigation: Review before installing in sensitive workspaces, use scoped or non-production gateway tokens, and treat debug and watchdog controls as administrator-only. <br>
Risk: The standalone UI proxy forwards browser bearer-token authorization to the gateway and can expose access if bound too broadly. <br>
Mitigation: Keep the UI bound to 127.0.0.1 and do not enable unsafe LAN binding unless intentional. <br>
Risk: Context injection and external model configuration can move project data outside the local workspace. <br>
Mitigation: Disable context injection or remove GEMINI_API_KEY when project data must remain local. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/derp42/openclaw-orchard) <br>
- [README](README.md) <br>
- [Orchard local debugging](docs/local-debugging.md) <br>
- [OrchardOS Dashboard UX/UI Design Brief](docs/ux-brief.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline commands, configuration examples, REST API descriptions, and generated OpenClaw task-management behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent SQLite-backed project, task, run, comment, and dashboard state inside OpenClaw.] <br>

## Skill Version(s): <br>
0.2.5-rc.5 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
