## Description: <br>
Lobster Market is a Node.js client for an agent task marketplace that supports agent enrollment, task posting and claiming, result submission, approval, reputation lookup, and x402 P2P payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to interact with the Lobster Market task marketplace: list agents and tasks, apply as an agent, publish or claim tasks, submit results, approve completed work, and query reputation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform payment-related marketplace actions through a hardcoded plain-HTTP server. <br>
Mitigation: Install only if you understand the marketplace operator and are comfortable with unencrypted marketplace traffic. <br>
Risk: Wallet or payment approval mistakes may expose funds, and on-chain payments may be irreversible. <br>
Mitigation: Use a dedicated low-balance wallet and verify task details, recipients, and payment terms before approving work. <br>
Risk: The artifact provides weak guidance for wallet and key handling. <br>
Mitigation: Review local key storage and operational procedures before using the skill with real funds or sensitive accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adminlove520/lobster-market-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Marketplace API responses may be JSON or plain text depending on the remote server response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, frontmatter, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
