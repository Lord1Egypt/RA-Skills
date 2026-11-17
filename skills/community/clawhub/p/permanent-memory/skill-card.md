## Description:

Auto Memory stores files and agent memory entries as permanent CID-addressed records on the Autonomys Network, then recalls linked memory chains from a known head CID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xautonomys](https://clawhub.ai/user/0xautonomys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use Auto Memory to upload and retrieve files, save agent memories, and reconstruct a memory chain after local state loss. It is intended for workflows where the user accepts permanent public storage by CID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded data can become permanent and publicly retrievable by CID.

Mitigation: Review content before upload, exclude secrets and personal or regulated data, and encrypt sensitive material before storing it.

Risk: The setup flow can persist an Auto Drive API key in local agent configuration.

Mitigation: Use a safer secret-management mechanism when available and rotate the key if it may have been exposed.

Risk: A memory chain restored from an untrusted CID can inject unverified content into agent context.

Mitigation: Only recall or continue chains from trusted sources and review restored entries before using them as agent state.

Risk: The optional Auto-Respawn integration can run an unpinned npx command.

Mitigation: Pin and audit the package version and target script before using that optional integration.

## Reference(s):

- [Auto Memory ClawHub Page](https://clawhub.ai/0xautonomys/skills/permanent-memory)
- [Auto Drive Dashboard and API Keys](https://ai3.storage)
- [Auto Drive Developer API Key Page](https://explorer.ai3.storage/mainnet/drive/developers)
- [Auto Drive API Reference](references/automemory-api.md)
- [Autonomys Network Overview](references/autonomys-network.md)
- [Memory Chain Reference](references/memory-chain.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CIDs, gateway links, local files, and memory-chain JSON; uploads require AUTO_DRIVE_API_KEY.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
