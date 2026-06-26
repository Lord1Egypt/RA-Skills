## Description: <br>
Manage Aavegotchi pocket wallets (escrow) on Base with Bankr for deposits, withdrawals, balance and ownership checks, and plain-English pocket commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Aavegotchi pocket wallet addresses and ERC20 balances on Base, then deposit or withdraw supported tokens through Bankr-managed transaction submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real token transfers from or into Aavegotchi pocket wallets through Bankr. <br>
Mitigation: Verify the gotchi ID, token, amount, recipient, owner, and pocket address before approving any transaction. <br>
Risk: The BANKR_API_KEY grants transaction-submission capability for the configured Bankr wallet. <br>
Mitigation: Keep BANKR_API_KEY private and provide it only in trusted runtime environments. <br>
Risk: Bypassing the default Bankr owner check can allow commands to run without confirming the Bankr wallet controls the gotchi. <br>
Mitigation: Avoid SKIP_BANKR_OWNER_CHECK=1 unless ownership and transaction safety have been independently confirmed. <br>
Risk: Natural-language withdrawal commands can be misparsed or misunderstood before funds move. <br>
Mitigation: Use dry-run previews and the explicit withdraw approval flag only after reviewing the generated command and destination address. <br>


## Reference(s): <br>
- [Gotchi Pocket ClawHub listing](https://clawhub.ai/aaigotchi/gotchi-pocket) <br>
- [aaigotchi publisher profile](https://clawhub.ai/user/aaigotchi) <br>
- [Base transaction explorer](https://basescan.org) <br>
- [Base mainnet RPC endpoint](https://mainnet.base.org) <br>
- [Bankr API endpoint](https://api.bankr.bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text key-value output with shell command examples and transaction explorer URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BANKR_API_KEY plus cast, jq, curl, and python3; transaction commands submit Base mainnet ERC20 transfers through Bankr.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
