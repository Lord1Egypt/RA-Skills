## Description:

Connect OpenClaw to Manus task APIs for chat-driven image generation, document/slides jobs, task polling, output collection, and messaging-surface return flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t0nyren](https://clawhub.ai/user/t0nyren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to route clear Manus generation, research, image, document, and slide tasks from chat into Manus APIs, then poll and return files or status back to the current messaging surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security evidence flags broad handling of credentials, URLs, and file writes.

Mitigation: Review before installing, run in a locked-down environment, and keep Manus credentials only in trusted local configuration.

Risk: A misconfigured Manus API base URL could send tasks or credentials to the wrong endpoint.

Mitigation: Set MANUS_API_BASE explicitly to the expected HTTPS Manus endpoint and verify the value before use.

Risk: Automatic chat triggers can launch unintended Manus jobs, especially in group conversations.

Mitigation: Use strict trigger rules, such as bot mentions plus an explicit Manus prefix, before submitting tasks.

Risk: Downloaded outputs and slide JSON may contain untrusted content.

Mitigation: Process returned files cautiously and avoid untrusted slide JSON until downloader and path handling have been reviewed.

## Reference(s):

- [Manus API Documentation](https://open.manus.im/docs)
- [Manus Tasks API](https://api.manus.ai/v1/tasks)
- [Setup](references/setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Chat Patterns](references/chat-patterns.md)
- [Feishu Return](references/feishu-return.md)
- [Slides Handling](references/slides.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration examples, and JSON result summaries from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local downloaded files under the skill workspace and PPTX files when converting slide JSON outputs.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
