## Description:

Interact with the Mutinynet Bitcoin testnet faucet to get testnet bitcoin on-chain, pay lightning invoices, open lightning channels, and generate BOLT11 invoices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benthecarman](https://clawhub.ai/user/benthecarman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to obtain Mutinynet signet/testnet bitcoin and exercise Lightning workflows, including paying invoices, opening channels, and generating BOLT11 invoices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login can exchange a GitHub OAuth token with a user-configurable faucet URL.

Mitigation: Use the default trusted faucet URL for login, avoid inherited or untrusted MUTINYNET_FAUCET_URL values, and revoke GitHub authorization if an untrusted endpoint was used.

Risk: A reusable faucet token may be stored on disk or supplied through the MUTINYNET_FAUCET_TOKEN environment variable.

Mitigation: Treat the stored token and environment variable as secrets, avoid shared machines unless permissions are locked down, and remove or rotate tokens when no longer needed.

## Reference(s):

- [Mutinynet CLI repository](https://github.com/benthecarman/mutinynet-cli)
- [Mutinynet CLI releases](https://github.com/benthecarman/mutinynet-cli/releases/latest)
- [Mutinynet](https://mutinynet.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Rust/cargo installation path or prebuilt binary, network access to the configured faucet URL, and careful handling of faucet authentication tokens.]

## Skill Version(s):

0.1.1 (source: server release, SKILL.md metadata, Cargo.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
