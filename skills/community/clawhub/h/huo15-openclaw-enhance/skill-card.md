## Description:

Huo15 Openclaw Enhance is a third-party OpenClaw plugin that adds non-invasive agent-harness features such as structured memory, safety observations, task and workflow helpers, statusline and dashboard views, file upload and sharing bridges, and session search without replacing native OpenClaw behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this plugin to add persistent context, task organization, safety observations, file-transfer helpers, session lifecycle cues, and operational diagnostics to OpenClaw agents while keeping native OpenClaw behavior authoritative.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin is broad and always-on, and server security evidence says it can persistently change agent behavior and force replies.

Mitigation: Install it only when those enhancements are wanted, review enabled modules before deployment, and disable behavior-changing modules that are not needed.

Risk: Local upload and share routes can expose files through generated URLs.

Mitigation: Review large-file upload and sharing settings, require an appropriate public base URL only when needed, use short expirations, and revoke shared files when the transfer is complete.

Risk: Memory capture, transcript search, and history surfacing can reveal local agent context.

Mitigation: Disable automatic memory and transcript/history features for sensitive workspaces or limit use to agents where persistent context is acceptable.

Risk: LaunchAgent, archiver, or curl-to-bash setup paths can create unwanted background behavior or install unreviewed code.

Mitigation: Prefer the package-manager install path, pin and inspect any setup script before execution, and avoid optional background-task setup unless operations require it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-enhance)
- [Source repository](https://cnb.cool/huo15/ai/huo15-openclaw-enhance)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [npm package](https://www.npmjs.com/package/@huo15/openclaw-enhance)
- [Architecture documentation](docs/architecture.md)
- [Product requirements](docs/PRD.md)
- [Non-invasive enhancement decision](docs/decisions/0001-non-invasive-enhancement.md)
- [Remove model router decision](docs/decisions/0002-remove-model-router.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON-like tool results, inline shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include temporary local file-sharing or upload URLs, memory and transcript search summaries, dashboard/status information, and proposed OpenClaw CLI commands.]

## Skill Version(s):

6.7.21 (source: server release and package.json; SKILL.md frontmatter reports 6.7.13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
