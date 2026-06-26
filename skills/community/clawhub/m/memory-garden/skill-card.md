## Description: <br>
N-count validated knowledge for AI agents. Patterns that prove themselves through repeated use. Local-first, community-ready. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agent users use Memory Garden to search, reuse, extract, and validate recurring knowledge patterns across conversations while keeping storage local by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local daemon can reuse stored patterns in future prompts. <br>
Mitigation: Periodically review saved data under ~/.memory-garden and disable search or remove patterns that should not influence future responses. <br>
Risk: Pattern extraction may store conversation-derived knowledge when enabled. <br>
Mitigation: Leave MG_EXTRACTION_ENABLED=false unless storage is intentional, and keep MG_EXTRACTION_CONFIRM=true so extracted patterns require review. <br>
Risk: Sync can share patterns outside the local machine when enabled. <br>
Mitigation: Leave MG_SYNC_ENABLED=false unless P2P sharing is intended and the configured peers are trusted. <br>
Risk: The skill depends on a downloaded mg-daemon binary. <br>
Mitigation: Verify the daemon source or expected SHA-256 hash before use. <br>


## Reference(s): <br>
- [Memory Garden ClawHub listing](https://clawhub.ai/leegitw/memory-garden) <br>
- [Memory Garden repository](https://github.com/live-neon/memory-garden) <br>
- [OpenClaw Quick Start](https://github.com/live-neon/memory-garden/blob/main/docs/guides/openclaw-quickstart.md) <br>
- [P2P Sync Setup](https://github.com/live-neon/memory-garden/blob/main/docs/guides/p2p-sync-setup.md) <br>
- [Safe Defaults](https://github.com/live-neon/memory-garden/blob/main/docs/standards/safe-defaults.md) <br>
- [Daemon Lifecycle Architecture](https://github.com/live-neon/memory-garden/blob/main/docs/architecture/daemon-lifecycle.md) <br>
- [Memory Garden daemon release for macOS arm64](https://github.com/live-neon/memory-garden/releases/download/v1.0.0/mg-daemon-darwin-arm64) <br>
- [Memory Garden daemon release for Linux amd64](https://github.com/live-neon/memory-garden/releases/download/v1.0.0/mg-daemon-linux-amd64) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown and JSON tool responses with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can augment prompts with retrieved patterns, return pattern search results, queue extracted patterns when enabled, and report validation outcomes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
