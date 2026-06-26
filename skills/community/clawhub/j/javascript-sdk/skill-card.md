## Description: <br>
Provides guidance and examples for using the inference.sh JavaScript/TypeScript SDK to run AI apps, build agents, stream responses, upload files, and integrate Node.js, React, and Next.js applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when integrating @inferencesh/sdk into JavaScript/TypeScript, Node.js, browser, React, or Next.js applications. It supports inference calls, file uploads, streaming, sessions, server proxy setup, and agent/tool workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill permits broad npm, npx, node, pnpm, and yarn command examples that can run package scripts or local code. <br>
Mitigation: Review commands before execution and approve package manager or Node.js actions case by case. <br>
Risk: Credential examples may lead users to expose inference API keys in frontend code or logs. <br>
Mitigation: Keep real API keys server-side, use the documented proxy pattern for frontend apps, and avoid NEXT_PUBLIC-style client credentials. <br>
Risk: File upload and public file examples can expose unintended or sensitive data. <br>
Mitigation: Upload only intended non-sensitive files and avoid public file settings for private data. <br>
Risk: Tool, webhook, browser automation, and eval-style examples can trigger unsafe external actions or code execution. <br>
Mitigation: Replace eval examples with a safe parser and validate or require approval for webhook calls, browser automation, and tool execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/okaris/javascript-sdk) <br>
- [inference.sh](https://inference.sh) <br>
- [JavaScript SDK Reference](https://inference.sh/docs/api/sdk-javascript) <br>
- [Agent SDK Overview](https://inference.sh/docs/api/agent-sdk) <br>
- [Tool Builder Reference](https://inference.sh/docs/api/agent-tools) <br>
- [Server Proxy Setup](https://inference.sh/docs/api/sdk/server-proxy) <br>
- [Authentication](https://inference.sh/docs/api/authentication) <br>
- [Streaming](https://inference.sh/docs/api/sdk/streaming) <br>
- [File Uploads](https://inference.sh/docs/api/sdk/files) <br>
- [Agent Patterns](references/agent-patterns.md) <br>
- [File Handling Reference](references/files.md) <br>
- [React Integration Reference](references/react-integration.md) <br>
- [Server Proxy Setup Reference](references/server-proxy.md) <br>
- [Sessions Reference](references/sessions.md) <br>
- [Streaming Reference](references/streaming.md) <br>
- [Tool Builder Reference File](references/tool-builder.md) <br>
- [TypeScript Reference](references/typescript.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript, JavaScript, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include npm, yarn, or pnpm command examples and SDK integration snippets.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
