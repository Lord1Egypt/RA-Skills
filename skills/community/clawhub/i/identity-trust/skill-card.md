## Description:

Decentralized Identity (DID) and Verifiable Credentials management for AI Agents

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent builders use Identity Trust to create and resolve decentralized identifiers, issue and verify W3C verifiable credentials, and evaluate agent trust for authentication or trust workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable external code through npm or a GitHub source checkout.

Mitigation: Use a pinned package version or reviewed commit in a sandboxed, unprivileged environment before adoption.

Risk: The skill creates persistent local identity credentials and keys under ~/.openclaw/identity/.

Mitigation: Protect that directory with strict local permissions and avoid syncing or casually exporting it.

Risk: DID creation, credential issuance, export, and network resolution can change identity state or expose sensitive identity data.

Mitigation: Require explicit user confirmation before creating DIDs, issuing credentials, exporting data, or enabling network resolution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/identity-trust)
- [README](https://github.com/ZhenRobotics/openclaw-identity-trust#readme)
- [Quick Start Guide](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/QUICKSTART.md)
- [API Reference](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/src/types.ts)
- [npm Package](https://www.npmjs.com/package/openclaw-identity-trust)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, TypeScript examples, and JSON-shaped DID or credential data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent identity files under ~/.openclaw/identity/ when commands are executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
