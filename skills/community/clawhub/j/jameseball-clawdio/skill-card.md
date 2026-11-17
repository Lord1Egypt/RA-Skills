## Description:

Secure P2P communication for AI agents with a Noise XX handshake, XChaCha20-Poly1305 encryption, connection consent, human verification, and no central servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameseball](https://clawhub.ai/user/jameseball)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Clawdio to add encrypted peer-to-peer messaging, connection consent, and human peer verification between agents across machines or networks without relying on a central server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Peer-authentication and key-storage weaknesses may undercut security-sensitive use.

Mitigation: Verify peers out of band before trust-sensitive use and protect or avoid persistent identityPath files.

Risk: Automatic acceptance and exposed listeners can admit unintended peers.

Mitigation: Keep autoAccept disabled outside local tests and restrict listener exposure with host binding and firewall controls.

Risk: Sensitive agent traffic may rely on unreviewed dependency ranges or connection-string key validation.

Mitigation: Prefer a version that pins dependencies and fixes connection-string key validation before handling sensitive traffic.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jameseball/skills/jameseball-clawdio)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript and shell code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup steps, API usage examples, connection-string handling, identity persistence options, and peer verification workflow guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
