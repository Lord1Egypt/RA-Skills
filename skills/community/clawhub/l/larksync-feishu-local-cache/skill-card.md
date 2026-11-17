## Description:

Sync Feishu docs into local cache for OpenClaw-first reading, reducing API calls and token cost.

This skill is for research and development only.

## Publisher:

[gooderno1](https://clawhub.ai/user/gooderno1)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

OpenClaw users, developers, and teams with Feishu document repositories use this skill to create a low-frequency local cache so day-to-day retrieval can prefer local Markdown and files over repeated Feishu API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The WSL helper can automatically select a discovered non-loopback endpoint before sending sensitive sync details such as cloud folder tokens.

Mitigation: Use an explicit trusted --base-url when possible and avoid sending cloud folder tokens to automatically discovered non-loopback HTTP endpoints.

Risk: The helper can create or run sync tasks against a local LarkSync backend.

Mitigation: Install only when the local LarkSync backend is trusted, run check before task changes, and keep the default download_only mode unless uploads are intentionally required.

Risk: Bidirectional and upload-only modes can propagate local changes back to Feishu.

Mitigation: Use download_only by default and test bidirectional behavior in a non-production folder before enabling it for important documents.

## Reference(s):

- [LarkSync homepage](https://github.com/gooderno1/LarkSync)
- [ClawHub skill page](https://clawhub.ai/gooderno1/skills/larksync-feishu-local-cache)
- [Publisher profile](https://clawhub.ai/user/gooderno1)
- [OPENCLAW_AGENT_GUIDE.md](OPENCLAW_AGENT_GUIDE.md)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper commands can check service health, configure low-frequency download schedules, create or reuse sync tasks, run tasks, and emit JSON results for auditability.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
