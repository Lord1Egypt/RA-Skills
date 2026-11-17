## Description:

Memory Garden provides N-count validated, local-first knowledge for AI agents by surfacing patterns that have proven useful through repeated use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to search, validate, and optionally extract reusable knowledge patterns for AI conversations. It can add relevant stored or community patterns into prompts while keeping local storage as the default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts a local background daemon and stores memory under ~/.memory-garden.

Mitigation: Review the daemon behavior before installation, monitor the local data directory, and remove stored memory when it is no longer needed.

Risk: Stored or community knowledge can be added to model prompts by default.

Mitigation: Treat injected patterns as untrusted context, review augmented prompts for sensitive work, and disable search with MG_SEARCH_ENABLED=false when prompt augmentation is not appropriate.

Risk: Conversation harvesting and sharing can expose information when extraction or sync are enabled.

Mitigation: Keep MG_EXTRACTION_ENABLED and MG_SYNC_ENABLED disabled unless intentional, and keep confirmation required for any extracted patterns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/memory-garden)
- [Memory Garden repository](https://github.com/live-neon/memory-garden)
- [OpenClaw quick start](https://github.com/live-neon/memory-garden/blob/main/docs/guides/openclaw-quickstart.md)
- [P2P sync setup](https://github.com/live-neon/memory-garden/blob/main/docs/guides/p2p-sync-setup.md)
- [Safe defaults](https://github.com/live-neon/memory-garden/blob/main/docs/standards/safe-defaults.md)
- [Daemon lifecycle architecture](https://github.com/live-neon/memory-garden/blob/main/docs/architecture/daemon-lifecycle.md)
- [Continuous improver integration](https://github.com/live-neon/memory-garden/blob/main/docs/guides/continuous-improver-integration.md)
- [Memory Garden daemon download for macOS arm64](https://github.com/live-neon/memory-garden/releases/download/v1.0.0/mg-daemon-darwin-arm64)
- [Memory Garden daemon download for Linux amd64](https://github.com/live-neon/memory-garden/releases/download/v1.0.0/mg-daemon-linux-amd64)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text and JSON tool results, with Markdown installation and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search is enabled by default; extraction and sync are opt-in; outputs depend on the local mg-daemon and stored or community patterns.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
