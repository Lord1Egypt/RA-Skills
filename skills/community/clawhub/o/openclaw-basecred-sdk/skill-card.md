## Description:

Check human reputation via Ethos Network, Talent Protocol, and Farcaster using the neutral basecred-sdk, returning raw scores, levels, and signals for identity verification and trust assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teeclaw](https://clawhub.ai/user/teeclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to fetch reputation and identity signals for Ethereum addresses across Ethos Network, Talent Protocol, and Farcaster. It supports trust-assessment workflows by reporting source-specific data without making a final trust judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads ~/.openclaw/.env, which can expose all values in that file to the Node process and dependencies.

Mitigation: Run it with an isolated environment containing only TALENT_API_KEY and NEYNAR_API_KEY when those sources are needed.

Risk: The SDK install is not consistently pinned in package metadata.

Mitigation: Verify that @basecred/sdk resolves to the reviewed version before installation or execution.

Risk: The isolation test can access the user's OpenClaw credential path.

Mitigation: Do not run the isolation test as an elevated user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teeclaw/skills/openclaw-basecred-sdk)
- [Security documentation](SECURITY.md)
- [@basecred/sdk package](https://www.npmjs.com/package/@basecred/sdk)
- [@basecred/sdk output schema](https://github.com/Callmedas69/basecred/tree/main/packages/sdk#output-schema)
- [Ethos Network](https://ethos.network)
- [Talent Protocol](https://talentprotocol.com)
- [Neynar](https://neynar.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, code, configuration]

**Output Format:** [JSON by default, with optional human-readable text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Ethereum address; optional TALENT_API_KEY and NEYNAR_API_KEY enable additional data sources.]

## Skill Version(s):

1.0.4 (source: evidence release, package.json, CHANGELOG, released 2026-02-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
