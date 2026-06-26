## Description: <br>
Gives an agent its own Nostr identity, Cashu ecash wallet, profile, posting, direct messaging, follows, reactions, zaps, and wallet commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnyeager](https://clawhub.ai/user/shawnyeager) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to bootstrap and operate an agent-owned Nostr social presence with an associated ecash wallet. It supports setup, profile management, posting, replies, DMs, follows, zaps, balance checks, invoices, and wallet payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use existing local Nostr or cocod wallet secrets even though it is framed as creating an agent-owned identity and wallet. <br>
Mitigation: Install only in a dedicated agent account or clean HOME directory, and do not run it where existing Nostr or cocod wallet credentials are stored. <br>
Risk: The skill can perform social and wallet actions such as posts, DMs, follows, deletes, zaps, invoice payments, and autoresponse workflows. <br>
Mitigation: Require explicit approval before those actions and keep only small wallet balances available to the agent. <br>
Risk: Loss or exposure of the mnemonic can affect both the Nostr identity and ecash wallet. <br>
Mitigation: Back up the mnemonic securely and protect the local wallet and identity files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawnyeager/nostr-social) <br>
- [Publisher profile](https://clawhub.ai/user/shawnyeager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local Nostr and wallet configuration under the user's HOME directory during setup.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
