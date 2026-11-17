## Description:

P2P file transfer between AI agents via message channels. Supports chunked transfer, IPFS fallback for large files, and trusted peer management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stormixus](https://clawhub.ai/user/stormixus)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to transfer files between AI agents over text-based channels, configure trusted peer relationships, and use chunked transfer or IPFS fallback for larger files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable OCFT secrets and auto-accept behavior can allow a trusted peer to send files without human review.

Mitigation: Treat OCFT secrets like passwords, avoid sharing them in public or logged channels, and keep auto-accept narrowly scoped or disabled unless the peer is fully trusted.

Risk: Transferred files and an unpinned global npm install can affect the local host environment.

Mitigation: Use a sandboxed download directory and prefer a pinned or locally reviewed package version before installing or running OCFT.

Risk: IPFS fallback can expose sensitive files through third-party providers or gateways.

Mitigation: Avoid IPFS for sensitive files unless you control the provider and gateway configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stormixus/skills/ocft)
- [GitHub Repository](https://github.com/stormixus/ocft)
- [npm Package](https://www.npmjs.com/package/ocft)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, TypeScript examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through OCFT CLI setup, peer trust management, file transfer flows, IPFS fallback configuration, and security precautions.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
