## Description:

Clawnch coin-launch receipts + local verify: pull launches from clawn.ch, write receipt JSON/MD, optional Blockscout/Dexscreener checks, local bookmark ref files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

Developers and crypto operators use this skill to retrieve Clawnch token-launch receipts, normalize local receipt records, verify public indexing data, and prepare local monitoring references without wallet signing or repository publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some scripts may write outside advertised local folders when given crafted symbols or paths.

Mitigation: Run the skill only in a dedicated workspace, use trusted symbol and receipt inputs, and add or verify path validation before arbitrary inputs are accepted.

Risk: Installing with an unpinned ClawHub CLI can introduce supply-chain drift.

Mitigation: Pin or verify the ClawHub CLI version before installing or running this release.

Risk: Wallet private keys or GitHub credentials could be exposed if a user supplies them unnecessarily.

Mitigation: Do not paste wallet private keys, mnemonics, GitHub tokens, or repository credentials into this skill; the reviewed package does not require them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lyra-coin-launch-manager)
- [Publisher profile](https://clawhub.ai/user/deepseekoracle)
- [Project homepage](https://github.com/DeepSeekOracle/lyra-crypto-operator)
- [Security guidance](references/SECURITY.md)
- [SkillSpector audit response](references/SKILLSPECTOR_AUDIT.md)
- [Crypto lattice separation policy](CRYPTO_LATTICE_SEPARATION.md)
- [STARCORE family cron template](references/cron_template_starcore_family.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; scripts produce local JSON and Markdown receipt, verification, and bookmark files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for human review before relying on launch or indexer status.]

## Skill Version(s):

1.2.0 (source: frontmatter, claw.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
