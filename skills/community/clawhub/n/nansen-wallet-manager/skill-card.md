## Description: <br>
Wallet management: create local or Privy server-side wallets, list and show wallets, export local wallet keys, send tokens, delete wallets, and check balances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to operate Nansen CLI wallet workflows, including wallet creation, balance checks, token sends, key export for local wallets, and wallet deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables high-impact wallet actions, including sending funds, exporting local private keys, deleting wallets, and changing the default wallet. <br>
Mitigation: Require the agent to show the exact command and obtain explicit approval before send, export, delete, or default-wallet changes; prefer dry-run previews when available. <br>
Risk: Local wallet credentials may fall back to an insecure .credentials file when no OS keychain is available. <br>
Mitigation: Use low-value or purpose-built wallets, prefer secure keychain or Privy-backed storage, and avoid environments where credentials fall back to local plaintext-adjacent storage. <br>
Risk: The security review verdict is suspicious because the skill grants wallet authority without clear per-action approval safeguards. <br>
Mitigation: Review before installing and constrain use to trusted environments where the nansen-cli package, API credentials, and wallet provider secrets are controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-wallet-manager) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require NANSEN_API_KEY, nansen-cli, wallet provider credentials, and explicit user approval for high-impact wallet actions.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
