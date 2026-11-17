## Description:

Prepare a desk computer for Hyperliquid by installing client SDKs, selecting testnet or mainnet, checking connectivity, and guiding user-authorized API wallet setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading desk operators use this skill to prepare a workstation for Hyperliquid research, testnet, or mainnet access, check connectivity, and guide user-authorized API wallet setup and readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If a secure secret provider is unavailable, the instructions allow an API wallet private key to be stored in a plaintext file.

Mitigation: Use an approved secure secret provider and avoid installation until the file fallback is removed or secure secret handling is confirmed.

Risk: Some setup instructions are described as read-only even though they install software or change files.

Mitigation: Clearly disclose installation and file changes, and obtain authorization before carrying them out.

Risk: The security scan was partial because some local references could not be resolved.

Mitigation: Review unresolved local references and complete security review before relying on the skill.

## Reference(s):

- [Hyperliquid Mainnet App](https://app.hyperliquid.xyz)
- [Hyperliquid Testnet App](https://app.hyperliquid-testnet.xyz)
- [Hyperliquid Testnet Faucet](https://app.hyperliquid-testnet.xyz/drip)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers SDK setup, connectivity checks, network selection, and optional API wallet provisioning and readiness guidance.]

## Skill Version(s):

1.9.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
