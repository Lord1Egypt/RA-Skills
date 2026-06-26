## Description: <br>
Step-by-step instructions to securely restore Monero wallets from 25-word seeds, keys, and hardware devices, with troubleshooting and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liumaimiao](https://clawhub.ai/user/liumaimiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill as a recovery checklist for restoring access to Monero wallets from seed phrases, private keys, or hardware wallets. It also helps troubleshoot failed restores, missing balances, and multisig or hardware-wallet recovery issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet recovery secrets such as seed phrases or private keys may be exposed during use. <br>
Mitigation: Use the skill only as a recovery checklist; never enter secrets on untrusted, shared, browser-based, or network-exposed systems. <br>
Risk: A compromised or mishandled recovery secret can permanently endanger funds. <br>
Mitigation: Move funds to a fresh wallet if any recovery secret may have been exposed. <br>


## Reference(s): <br>
- [Monero mnemonic English word list](https://github.com/monero-project/monero/blob/master/src/mnemonics/english.txt) <br>
- [xmrchain.net block explorer](https://xmrchain.net) <br>
- [Monero community support](https://www.getmonero.org/community/) <br>
- [Monero StackExchange](https://monero.stackexchange.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with numbered recovery steps and inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recovery guidance may reference sensitive wallet seeds or private keys and should be treated as a checklist, not as a custody tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
