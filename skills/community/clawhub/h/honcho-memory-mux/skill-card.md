## Description:

Install and enable Honcho and the @alloralabs/honcho-memory-mux extension, migrate legacy file memory, and update workspace instructions so agents use Honcho-first multiplexed retrieval with local-file fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spooktheducks](https://clawhub.ai/user/spooktheducks)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to set up Honcho-backed memory retrieval, migrate existing markdown memory, and document fallback behavior. It is intended for workspaces that need persistent memory with local-file backup and clear migration reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation memory, including sensitive prompts and assistant responses, may be sent to and retained by Honcho.

Mitigation: Use a self-hosted or approved Honcho endpoint, avoid sessions containing secrets, and require clear opt-in, deletion, and retention controls before broad deployment.

Risk: Stored memory is injected into future prompts and may carry stale, misleading, or prompt-injected content.

Mitigation: Treat recalled memory as untrusted context, prefer targeted retrieval with source awareness, and review memory-influenced behavior before acting on sensitive tasks.

Risk: The skill updates workspace instruction files and may change agent behavior across later sessions.

Mitigation: Review all instruction-file diffs before applying them, preserve custom content, and keep changes reversible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spooktheducks/skills/honcho-memory-mux)
- [Honcho homepage](https://honcho.dev)
- [Honcho documentation](https://docs.honcho.dev)
- [Honcho repository](https://github.com/plastic-labs/honcho)
- [honcho-memory-mux repository](https://github.com/allora-network/honcho-memory-mux)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands, JSON configuration, and TypeScript plugin behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update workspace instruction files, migrate memory files, install OpenClaw plugins, and configure Honcho environment variables.]

## Skill Version(s):

0.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
