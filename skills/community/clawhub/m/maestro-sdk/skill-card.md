## Description: <br>
Build AI agents that operate Solana policy-controlled vaults using the Maestro SDK for token transfers, swaps, and vault interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yamancan](https://clawhub.ai/user/yamancan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure agents that operate Maestro Solana vaults, check vault health, and execute policy-controlled payment or balance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through token transfer and swap flows using a policy-controlled Solana vault. <br>
Mitigation: Use a dedicated limited wallet or session key, enforce strict Maestro vault policies, and require explicit user confirmation before each transfer or swap. <br>
Risk: Automatic key setup and persistent memory may leave sensitive operational state in local files. <br>
Mitigation: Protect generated key material and MEMORY.md files, restrict file permissions, and clear or re-verify saved vault ownership and session key data when access changes. <br>
Risk: Incorrect vault, owner, recipient, or policy state could cause failed or unintended financial operations. <br>
Mitigation: Run the documented health checks before transactions, verify the vault owner on first connection, and use Maestro recipient policies and spending limits. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yamancan/maestro-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational status messages, wallet setup guidance, vault health checks, transfer instructions, and error-handling guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
