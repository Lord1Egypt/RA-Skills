## Description:

Guides agents through deploying, configuring, monitoring, and troubleshooting Ika validators, fullnodes, and notifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omersadika](https://clawhub.ai/user/omersadika)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, infrastructure engineers, and validator operators use this skill to deploy, configure, monitor, recover, and troubleshoot Ika network nodes on Sui.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides high-value validator and staking guidance where incorrect release artifacts, package IDs, object IDs, staking portals, or signed transactions can put funds or validator participation at risk.

Mitigation: Independently verify official Ika sources, release artifacts, package/object IDs, staking portal authenticity, and every wallet transaction before signing.

Risk: Validator key material, especially root-seed.key, is sensitive and may be irreplaceable if lost.

Mitigation: Back up validator keys securely, store secrets in protected storage, and avoid exposing key files through logs, config sharing, or support requests.

Risk: Metrics, admin, or monitoring endpoints can expose operational data or control surfaces if reachable from the public Internet.

Mitigation: Keep admin endpoints bound to localhost, restrict metrics access, use HTTPS where applicable, and protect monitoring credentials.

Risk: Recovery and database deletion procedures can discard local node state and require a resync.

Mitigation: Run database deletion or recovery commands only when intentionally discarding local state, and confirm backups or resync plans before proceeding.

## Reference(s):

- [Configuration Reference](references/configuration.md)
- [Operations Reference](references/operations.md)
- [Mainnet Validator Setup](references/validator-setup.md)
- [Ika Homepage](https://ika.xyz)
- [Ika Releases](https://github.com/dwallet-labs/ika/releases)
- [Mainnet Contract Addresses](https://github.com/dwallet-labs/ika/blob/main/deployed_contracts/mainnet/address.yaml)
- [Testnet Contract Addresses](https://github.com/dwallet-labs/ika/blob/main/deployed_contracts/testnet/address.yaml)
- [Ika Mainnet Validator Staking Portal](https://ika-mainnet-validators-staking.pages.dev/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational checklists, configuration snippets, command examples, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
