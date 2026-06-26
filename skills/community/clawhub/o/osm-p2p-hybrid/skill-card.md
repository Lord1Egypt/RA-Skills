## Description: <br>
OSM-P2P Hybrid provides a UDP and Nostr based peer-to-peer communication system with intelligent routing, room types, gossip message propagation, QR-code node exchange, and CLI/API usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanara-osm](https://clawhub.ai/user/yanara-osm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, run, and integrate a hybrid P2P chat node that can communicate over local UDP paths and wide-area Nostr relays. It supports node discovery, status inspection, QR-code contact exchange, broadcasting, private messaging, room workflows, and TypeScript API integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can advertise node identity and local network addresses during P2P discovery. <br>
Mitigation: Run it only on networks where node identity and address exposure are acceptable, and review discovery settings before use. <br>
Risk: Messages may traverse relays or local network paths before encryption and relay behavior have been verified for the deployment. <br>
Mitigation: Avoid sensitive messages until the encryption, relay, and transport behavior has been independently reviewed and tested. <br>
Risk: The local data directory may contain the node private key and message logs. <br>
Mitigation: Protect access to ~/.osm-p2p, back it up only through approved secure channels, and periodically clear logs when retention is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanara-osm/osm-p2p-hybrid) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [skills/SKILL.md](skills/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes CLI commands, configuration paths, API snippets, and operational behavior for running a hybrid P2P communication node.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
