## Description:

OpenViking context database skill for AI agents that supports layered L0/L1/L2 context loading, semantic search, file-system-style memory management, and token-use comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyonepice](https://clawhub.ai/user/onlyonepice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to install and configure OpenViking, import project context, perform semantic search, browse layered context, and compare token consumption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and setup scripts perform local package installation, shell profile changes, and optional Rust CLI installation.

Mitigation: Review scripts before execution, run setup in a disposable environment or virtual environment, avoid running as root, and inspect any downloaded installer before use.

Risk: Provider API keys are written into local OpenViking configuration.

Mitigation: Use provider keys with limited quota or scope and check permissions on ~/.openviking/ov.conf after configuration.

Risk: Imported resources, indexed context, memory, and token statistics can persist across sessions.

Mitigation: Restrict imports to reviewed folders and URLs that exclude secrets, and periodically review or clear the OpenViking workspace and ~/.openviking/session_stats.json.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyonepice/skills/openviking-context)
- [OpenViking GitHub](https://github.com/volcengine/OpenViking)
- [OpenViking Website](https://www.openviking.ai)
- [OpenClaw Skill Documentation](https://docs.openclaw.ai/tools/creating-skills)
- [LiteLLM Provider Documentation](https://docs.litellm.ai/docs/providers)
- [NVIDIA NIM API](https://build.nvidia.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command output for search results, layered reads, status checks, and token statistics.]

## Skill Version(s):

1.0.0 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
