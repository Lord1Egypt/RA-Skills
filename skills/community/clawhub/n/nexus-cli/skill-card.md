## Description:

Manage a Jellyfin/Plex + *Arr media server stack by checking status, adding content, monitoring downloads, diagnosing issues, and restarting services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxtechera](https://clawhub.ai/user/maxtechera)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a self-hosted Jellyfin/Plex and *Arr stack through the Admirarr CLI for status, diagnostics, content additions, downloads, indexers, setup, and service management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can administer a user's media stack and Docker services.

Mitigation: Require explicit user approval before setup, doctor --fix, service restarts, indexer removals, or torrent deletion with --delete-files.

Risk: The installer and release integrity require careful review before use.

Mitigation: Prefer a pinned release and verify integrity where possible instead of using the pipe-to-shell installer.

Risk: Generated config.yaml and .env files may contain service API keys or VPN credentials.

Mitigation: Treat generated configuration files as secrets, restrict file permissions, and avoid cleartext remote service connections.

## Reference(s):

- [Nexus Cli on ClawHub](https://clawhub.ai/maxtechera/skills/nexus-cli)
- [Agent Skills standard](https://agentskills.io)
- [Recommended Indexers](artifact/docs/recommended-indexers.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with CLI commands and JSON-capable command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to use the Admirarr CLI as the interface to media-stack services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
