## Description: <br>
Orchard is an OpenClaw project and task management plugin with a persistent task board, agent tools, REST API access, a web dashboard, and an autonomous queue runner that dispatches ready tasks as subagents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derp42](https://clawhub.ai/user/derp42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use Orchard to organize projects, create and track agent tasks, and let configured subagents execute ready work while preserving run history and comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously spawn OpenClaw subagents and persist project data under ~/.openclaw. <br>
Mitigation: Install only where autonomous task execution is acceptable, and use the documented debug or log-only modes to suppress or limit spawning during review. <br>
Risk: The local dashboard and API can expose operational controls and bearer-token-mediated access if bound or proxied too broadly. <br>
Mitigation: Keep the UI bound to 127.0.0.1, use SSH tunneling for remote access, avoid non-local HTTP with bearer tokens, and treat watchdog or queue-control endpoints as administrative capabilities. <br>
Risk: Context injection and external configuration sources may process sensitive project text. <br>
Mitigation: Disable or carefully scope context injection and GEMINI_API_KEY usage when project content may be sensitive, and review any config-safety documentation URLs before use. <br>


## Reference(s): <br>
- [Orchard ClawHub listing](https://clawhub.ai/derp42/orchard) <br>
- [README.md](README.md) <br>
- [Orchard local debugging](docs/local-debugging.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and REST API route tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent project, task, run, comment, and knowledge-base records through OpenClaw tools, API routes, and dashboard interactions.] <br>

## Skill Version(s): <br>
0.2.5-rc.5 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
