## Description:

A P2P encrypted social friend-management skill for discovering peers, managing trusted relationships, sending secure messages, and maintaining a local social graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage peer discovery, friend trust levels, encrypted messaging workflows, groups, and local social-graph views in a P2P communication environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network discovery may scan or broadcast on local networks.

Mitigation: Use the skill only on trusted networks after reviewing what discovery scans, broadcasts, and stores.

Risk: The skill describes social recommendations based on message content.

Mitigation: Confirm what message content is analyzed and avoid sensitive communications unless the processing and storage behavior is acceptable.

Risk: The published artifact references an installer that is not present in the release evidence.

Mitigation: Confirm the package contains the expected installer and scripts before running installation commands.

Risk: Encrypted messaging behavior depends on secure-p2p-messenger.

Mitigation: Use a pinned, reviewed secure-p2p-messenger dependency before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/skills/lobster-friends-protocol-real)
- [Publisher profile](https://clawhub.ai/user/puppetcat-fire)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local P2P discovery, encrypted messaging, SQLite-backed friend data, and secure-p2p-messenger dependency setup.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
