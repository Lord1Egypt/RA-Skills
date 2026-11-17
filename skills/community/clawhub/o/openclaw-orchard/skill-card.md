## Description:

Agentic project and task management plugin for OpenClaw. Persistent SQLite-backed task board with a queue runner that auto-dispatches ready tasks as subagents, REST API, native agent tools, and a web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derp42](https://clawhub.ai/user/derp42)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use OrchardOS to manage agent work as persistent projects and tasks, then dispatch ready tasks through an automated queue runner. The skill also provides agent tools, REST API routes, and a dashboard for monitoring task state, run history, and project progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway tokens, task content, run output, and project knowledge may be sensitive persistent data.

Mitigation: Install only in trusted OpenClaw environments and protect the SQLite database, logs, task records, run records, and knowledge records as sensitive data.

Risk: Context injection can send project knowledge to an external embeddings provider.

Mitigation: Keep contextInjection disabled unless external embeddings are explicitly required and approved for the project data being processed.

Risk: The standalone dashboard and document-fetch behavior are flagged for XSS and SSRF concerns when used with privileged tokens or confidential projects.

Mitigation: Keep the standalone UI bound to loopback, avoid unsafe bind settings, and remediate the dashboard XSS and document-fetch SSRF issues before privileged or confidential use.

Risk: Automatic subagent dispatch can consume resources or continue work unexpectedly when a queue is misconfigured.

Mitigation: Use log-only or dry-run debugging modes, circuit breaker controls, conservative concurrency limits, and queue pause controls when evaluating or recovering the plugin.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/derp42/skills/openclaw-orchard)
- [README](README.md)
- [Local Debugging Guide](docs/local-debugging.md)
- [Dashboard UX Brief](docs/ux-brief.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, API route descriptions, and structured task/project data returned through tools or REST endpoints.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may persist in SQLite-backed project, task, run, comment, and knowledge records.]

## Skill Version(s):

0.2.5-rc.5 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
