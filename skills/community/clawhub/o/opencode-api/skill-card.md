## Description: <br>
Provides OpenClaw agents with Python and CLI wrappers for driving an OpenCode HTTP server to perform code review, code analysis, session management, structured-output tasks, and coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlin53882](https://clawhub.ai/user/jlin53882) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to send review, analysis, and coding tasks to a local OpenCode server through HTTP APIs or bundled Python wrappers. It is suited for workflows where OpenClaw delegates repository inspection, PR review, model selection, session control, or structured-output generation to OpenCode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive a powerful local OpenCode automation server, including workflows that may read code, run tools, or modify project state. <br>
Mitigation: Install only when that delegation is intended, review prompts and generated actions before use, and configure OpenCode permissions for least privilege. <br>
Risk: Binding the OpenCode server beyond localhost can expose code-execution capability or sensitive project context to a network. <br>
Mitigation: Keep the server bound to 127.0.0.1 by default; use strong authentication, firewalling, and a trusted network before binding to 0.0.0.0. <br>
Risk: Auto-start behavior may launch OpenCode when a wrapper first connects. <br>
Mitigation: Use the documented no-auto-start options or construct clients with auto_start disabled when server startup must remain under explicit operator control. <br>
Risk: Prompts, diffs, credentials, or repository content may be sent to external model providers through OpenCode sessions. <br>
Mitigation: Avoid submitting secrets or sensitive diffs, verify provider configuration, and use local or approved providers for confidential work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jlin53882/opencode-api) <br>
- [OpenCode API Skill](SKILL.md) <br>
- [OpenCode HTTP API Reference](references/api-reference.md) <br>
- [Server Deployment](references/server.md) <br>
- [SDK Reference](references/sdk.md) <br>
- [Permissions](references/permissions.md) <br>
- [Code Review Prompt](references/code-review-prompt.md) <br>
- [Artifact ClawHub metadata URL](https://clawhub.com/opencode-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets, plus JSON-compatible OpenCode API request and response examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenCode session identifiers, model settings, reasoning settings, structured-output schemas, and local server connection parameters.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata; artifact frontmatter says 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
