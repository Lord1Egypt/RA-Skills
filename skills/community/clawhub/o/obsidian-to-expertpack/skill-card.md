## Description:

Convert an existing Obsidian Vault into an agent-ready ExpertPack by copying Markdown content into a structured pack for retrieval and OpenClaw integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhearn](https://clawhub.ai/user/brianhearn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and knowledge-base maintainers use this skill to convert trusted Obsidian vaults into ExpertPacks that can be validated, improved, and added to OpenClaw memory search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter can copy Obsidian configuration, plugin data, workspace state, secrets, or symlinked files from outside the vault into the generated ExpertPack.

Mitigation: Use dry-run first, inspect the source vault's .obsidian directory, convert only trusted vaults, and review the generated pack before sharing it or adding it to global memory search.

## Reference(s):

- [Obsidian To Expertpack ClawHub Page](https://clawhub.ai/brianhearn/skills/obsidian-to-expertpack)
- [Publisher Profile](https://clawhub.ai/user/brianhearn)
- [ExpertPack Homepage](https://expertpack.ai)
- [Obsidian Vault to ExpertPack Migration Guide](references/migration-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON code blocks; the converter writes ExpertPack Markdown files and YAML configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and PyYAML. Supports dry-run previews before writing output files.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
