## Description: <br>
Nad Wallet creates and manages Monad wallets for AI agents, signs SIWE messages for NadMail, and checks MON balances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create or load Monad wallets, check MON balances, and register a NadMail handle through SIWE authentication. It is intended for Nad ecosystem wallet automation and requires careful private-key handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private keys, mnemonics, wallet files, and NadMail access tokens. <br>
Mitigation: Use a dedicated low-value wallet, prefer temporary environment variables or a secret manager, and delete ~/.nad-wallet wallet and token files when they are no longer needed. <br>
Risk: Artifact guidance includes an example for persisting NAD_PRIVATE_KEY in shell startup files. <br>
Mitigation: Do not add NAD_PRIVATE_KEY to ~/.bashrc or ~/.zshrc; keep secrets out of persistent shell configuration. <br>
Risk: The skill can sign authentication messages and supports wallet operations that may carry financial authority. <br>
Mitigation: Review each signing or transaction workflow before use and keep MON balances limited to the minimum needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/daaab/nad-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/daaab) <br>
- [Monad RPC endpoint](https://rpc.monad.xyz) <br>
- [Monad explorer](https://explorer.monad.xyz) <br>
- [NadMail](https://nadmail.ai) <br>
- [NadMail API](https://api.nadmail.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript and shell command examples; scripts produce console text or JSON depending on command options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local wallet, mnemonic, token, and audit log files under ~/.nad-wallet when managed wallet or NadMail registration flows are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact package metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
