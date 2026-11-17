## Description:

Helps developers integrate a JavaScript AI SDK for agent construction, streaming responses, session management, tool builders, and server proxy patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to plan and implement JavaScript AI SDK integrations for agent workflows, streaming output, stateful sessions, tool calling, file handling, and framework-specific server proxies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may send prompts, files, webhook payloads, memory content, or code-execution requests to model providers, proxy servers, or external services.

Mitigation: Review data flows before reuse, avoid unnecessary sensitive data, and approve external endpoints and enabled tools before deployment.

Risk: API keys or webhook secrets could be exposed if copied into client-side code or examples.

Mitigation: Keep credentials in environment variables and route browser traffic through server-side proxy patterns.

Risk: Tool-calling and command-style examples may perform unintended actions if user input is executed without controls.

Mitigation: Use approval gates for dangerous tools, validate inputs, and restrict execution to reviewed commands or allowlisted operations.

## Reference(s):

- [Detailed JavaScript SDK examples](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/javascript-sdk-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK integration steps, proxy setup guidance, and example snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
