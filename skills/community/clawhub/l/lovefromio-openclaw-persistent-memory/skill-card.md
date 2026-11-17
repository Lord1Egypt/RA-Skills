## Description:

Persistent memory system for OpenClaw agents with automatic context capture, recall, and semantic search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory to OpenClaw agents, including saved observations, full-text search, and automatic recall across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer path and curl-to-bash installation can execute remote code before review.

Mitigation: Review the installer path first, prefer bundled or manual install steps, and pin the npm package version where possible.

Risk: Always-on auto-capture and auto-recall can persist sensitive conversation content and later reintroduce it into agent context.

Mitigation: Keep auto-capture disabled for sensitive conversations unless persistent storage and later recall are acceptable.

Risk: The memory worker exposes local REST endpoints for search, observation access, update, and deletion.

Mitigation: Keep the worker URL bound to localhost and do not expose the service outside the local machine.

Risk: Documented deletion commands can remove the local memory directory.

Mitigation: Back up or inspect the memory directory before running deletion or uninstall commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovefromio/skills/lovefromio-openclaw-persistent-memory)
- [npm package: openclaw-persistent-memory](https://www.npmjs.com/package/openclaw-persistent-memory)
- [Installation guide](artifact/INSTALL.md)
- [Full skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local REST endpoint usage and memory-management command guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
