## Description:

Encrypted credential management for OpenClaw keeps API keys, tokens, and passwords out of the AI agent's context window with AES-256-GCM encryption, subprocess-scoped injection, and automatic output scrubbing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karanuppal](https://clawhub.ai/user/karanuppal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to store credentials encrypted and inject them only into authorized subprocesses, reducing the chance that agents expose secrets in context, tool output, outbound messages, or transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install global npm code that handles credential storage and OpenClaw execution and message hooks.

Mitigation: Review and pin the exact npm package version and source before installing, and use it only in trusted OpenClaw environments where those hooks are acceptable.

Risk: Passing real secrets through --key command arguments can expose them through shell history or process inspection.

Mitigation: Prefer interactive credential entry where available and avoid entering production secrets directly in command-line arguments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/karanuppal/skills/openclaw-credential-vault)
- [Source Repository](https://github.com/karanuppal/openclaw-credential-vault)
- [npm Package](https://www.npmjs.com/package/openclaw-credential-vault)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0-beta.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
