## Description:

Provides step-by-step guidance for restoring Monero wallets from seed phrases, private keys, and hardware devices while emphasizing safe handling of recovery material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumaimiao](https://clawhub.ai/user/liumaimiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to walk through Monero wallet recovery paths, including deterministic seed restore, key-based restore, hardware wallet recovery, restore-height selection, and troubleshooting failed restores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet recovery requires sensitive seed phrases or private keys that can transfer control of funds if exposed.

Mitigation: Never share seed phrases or private spend keys with an agent, website, chat, or third party; enter recovery material only into trusted official wallet software or directly on a hardware wallet device.

Risk: Incorrect restore height, seed words, or wallet source can make recovered balances appear missing.

Mitigation: Use official Monero wallet tools, verify seed words and ordering, choose a conservative restore height when uncertain, and wait for full blockchain sync before treating a balance as missing.

## Reference(s):

- [Monero Skill Page](https://clawhub.ai/liumaimiao/skills/monero-wallet-recovery)
- [xmrchain.net](https://xmrchain.net)
- [Monero English Mnemonic Word List](https://github.com/monero-project/monero/blob/master/src/mnemonics/english.txt)
- [Monero StackExchange](https://monero.stackexchange.com/)
- [Official Monero Community](https://www.getmonero.org/community/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with ordered steps, troubleshooting notes, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the artifact; guidance may reference wallet CLI commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
