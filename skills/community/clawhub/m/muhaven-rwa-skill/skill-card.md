## Description: <br>
Confidential real-world-asset (RWA) portfolio agent for reading encrypted MuHaven balances and staging buy, yield-claim, and pause intents for human confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hastodev](https://clawhub.ai/user/hastodev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External MuHaven users and developers use this skill to inspect encrypted RWA portfolio state, review yields and audit records, and prepare buy, claim, or pause requests that require out-of-band human confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-adjacent actions can stage buy, claim, and pause workflows through a persistent authenticated broker. <br>
Mitigation: Install only when the publisher is trusted, prefer read-only mode unless state-changing workflows are needed, and verify every confirmation request before approval. <br>
Risk: Security boundaries may depend on the local OpenClaw runtime and may be advisory rather than enforced in host-native operation. <br>
Mitigation: Verify that the runtime enforces sandbox permissions before relying on egress, filesystem, process, keychain, or hash-pinning protections. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/hastodev/muhaven-rwa-skill) <br>
- [Publisher profile](https://clawhub.ai/user/hastodev) <br>
- [MuHaven homepage](https://muhaven.app) <br>
- [Security posture](artifact/SECURITY.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, configuration] <br>
**Output Format:** [MCP tool responses with structured JSON payloads and human-facing text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wallet-adjacent actions are staged as confirmation intents; read-only mode limits exposed tools to read operations.] <br>

## Skill Version(s): <br>
0.1.4 (source: SKILL.md frontmatter, manifest.json, package.json, CHANGELOG released 2026-05-17, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
