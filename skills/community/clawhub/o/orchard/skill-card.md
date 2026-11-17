## Description:

Agentic project and task management plugin for OpenClaw with a persistent SQLite-backed task board, queue runner that auto-dispatches ready tasks as subagents, REST API, native agent tools, and a web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derp42](https://clawhub.ai/user/derp42)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use Orchard to organize agent projects, add and track tasks, and let configured subagents work through ready tasks while preserving run history and comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous queue execution can spawn subagents and continue work without direct step-by-step operator involvement.

Mitigation: Review configuration before enabling the plugin, use debug.logOnly or disable spawn flags for initial testing, and set conservative concurrency and task-rate limits.

Risk: Stored project knowledge and task content may be reused in later prompts, including prompt-injection text.

Mitigation: Review stored knowledge before reuse and keep contextInjection disabled unless the operator explicitly wants embedding-backed context injection.

Risk: Provider API keys and gateway tokens can be exposed if placed directly in plugin configuration or sent through unsafe access paths.

Mitigation: Avoid putting provider API keys directly in plugin config until /orchard/config redacts them, do not pass gateway tokens on command lines or over plain HTTP, and restrict access to gateway-authenticated routes.

Risk: The standalone UI forwards bearer authorization to the local OpenClaw gateway and can become risky if exposed beyond loopback.

Mitigation: Keep the UI bound to 127.0.0.1 by default, use SSH tunneling for remote access, and only widen bindAddress with explicit intent and access controls.

## Reference(s):

- [Orchard ClawHub Skill Page](https://clawhub.ai/derp42/skills/orchard)
- [README](README.md)
- [Orchard local debugging](docs/local-debugging.md)
- [OrchardOS Dashboard UX/UI Design Brief](docs/ux-brief.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, structured tool and API responses, and task execution outputs from OpenClaw subagents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist project data, task state, knowledge entries, comments, and run history in SQLite.]

## Skill Version(s):

0.2.5-rc.5 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
