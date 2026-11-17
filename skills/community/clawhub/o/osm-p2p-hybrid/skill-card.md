## Description:

OSM-P2P Hybrid provides a peer-to-peer messaging system that combines UDP direct networking with Nostr relay networking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanara-osm](https://clawhub.ai/user/yanara-osm)

### License/Terms of Use:

MIT

## Use Case:

Developers and technically capable users use this skill to install, run, and integrate a TypeScript P2P messaging CLI/library for peer discovery, chat, broadcasts, private messages, and QR-code node exchange over UDP and Nostr networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill joins UDP and Nostr networks by default and may publish node metadata to public relays.

Mitigation: Run it only on trusted networks, review relay and broadcast settings, and disable Nostr or UDP broadcast when that exposure is not acceptable.

Risk: The security evidence says message contents are sent without clear encryption.

Mitigation: Do not send secrets or sensitive content unless encryption has been independently verified or added.

Risk: The skill stores a reusable Nostr private key and message-content audit logs on disk.

Mitigation: Protect the data directory, rotate or remove identities when needed, and disable or restrict audit logging where possible.

Risk: Installation uses npm dependencies for networked runtime behavior.

Mitigation: Review dependency sources and the lockfile before running npm install.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Primary Skill Definition](artifact/SKILL.md)
- [Packaged Skill Definition](artifact/skills/SKILL.md)
- [Package Manifest](artifact/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, TypeScript snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on a Node.js/TypeScript CLI and library that can start network transports and write local identity and audit files.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog; package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
