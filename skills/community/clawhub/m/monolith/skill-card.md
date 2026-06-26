## Description: <br>
Secure crypto wallet for AI agents. Hardware-isolated keys (Apple Secure Enclave), ERC-4337 smart wallet, on-chain spending caps, default-deny policy engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slaviquee](https://clawhub.ai/user/slaviquee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and OpenClaw operators use this skill to let agents prepare, review, and submit policy-gated crypto wallet actions through the Monolith macOS daemon. It supports ETH and USDC transfers, swaps, balance checks, policy management, allowlist changes, emergency freeze, and audit-log review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An AI agent may move crypto assets automatically within the policy limits configured for the wallet. <br>
Mitigation: Use conservative per-transaction and daily caps, maintain recipient allowlists, and avoid funding the wallet with more value than the operator is comfortable exposing to automated actions. <br>
Risk: The skill depends on downloaded macOS daemon and companion components for signing, approvals, and wallet control. <br>
Mitigation: Verify the downloaded daemon and companion source before installation, keep the audit log enabled, and run setup checks before sending transactions. <br>
Risk: Approval flows require an active macOS GUI session with Touch ID and notifications; headless sessions cannot complete those approvals. <br>
Mitigation: Operate from a logged-in macOS GUI session when policy changes, non-allowlisted transfers, token approvals, or other human approval paths may be needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/slaviquee/monolith) <br>
- [Monolith homepage](https://github.com/slaviquee/monolith) <br>
- [Monolith skill source](https://github.com/slaviquee/monolith/tree/main/skill) <br>
- [Monolith Daemon macOS package](https://github.com/slaviquee/monolith/releases/download/v0.1.5/MonolithDaemon-v0.1.5.pkg) <br>
- [Monolith Companion macOS app](https://github.com/slaviquee/monolith/releases/download/v0.1.3/MonolithCompanion.app.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with JSON policy inputs and transaction intent summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with the MonolithDaemon binary for signing and policy-gated transaction actions; balance checks can run read-only without the daemon.] <br>

## Skill Version(s): <br>
0.1.10 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
