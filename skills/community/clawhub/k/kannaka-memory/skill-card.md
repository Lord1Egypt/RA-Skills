## Description:

Kannaka Memory gives agents persistent wave-based memory, recall, dream consolidation, audio perception, and optional QueenSync swarm coordination through a Rust CLI and OpenClaw tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Kannaka Memory to add persistent local memory, semantic recall, dream consolidation, memory status metrics, audio perception, and optional swarm synchronization to OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer creates a persistent OpenClaw extension with a command-injection flaw and builds unpinned remote code.

Mitigation: Review or fix the generated extension before installation and prefer a pinned, verified upstream source or signed release.

Risk: Swarm commands can publish presence or phase state to the configured NATS server.

Mitigation: Treat swarm mode as remote data sharing and use it only with an approved NATS endpoint and appropriate disclosure expectations.

Risk: Memory deletion can remove persisted local memory.

Mitigation: Back up the Kannaka data directory and require confirmation expectations before enabling destructive memory operations.

Risk: Text may be sent to a remote Ollama endpoint when OLLAMA_URL points outside localhost.

Mitigation: Keep OLLAMA_URL local unless remote embedding processing has been reviewed and approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nickflach/skills/kannaka-memory)
- [Publisher Profile](https://clawhub.ai/user/nickflach)
- [Kannaka Memory Source](https://github.com/NickFlach/kannaka-memory)
- [Rust Toolchain](https://rustup.rs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and tool-output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local memory data under the configured Kannaka data directory and can emit memory search results, status reports, IDs, metrics, and swarm state.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
