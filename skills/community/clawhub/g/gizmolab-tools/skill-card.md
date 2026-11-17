## Description:

GizmoLab Tools guides agents to use GizmoLab's web-based blockchain developer tools and Web3 UI component library for dApp development, smart contract interaction, and blockchain operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gizmo-dev](https://clawhub.ai/user/gizmo-dev)

### License/Terms of Use:


## Use Case:

Developers building dApps or performing blockchain operations use this skill to navigate GizmoLab's web tools for Ethereum and Solana tasks and to find Web3 UI component installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-connected blockchain tools can create, mint, swap, or write transactions that may move assets or change on-chain state.

Mitigation: Use testnet or devnet first, verify contract addresses and transaction details, and require fresh human approval before any wallet signature or transaction confirmation.

Risk: The skill points agents to external installation commands and component code that could be copied into a project without review.

Mitigation: Inspect installation commands, dependencies, and component code before adding them to a project.

Risk: Burner wallet workflows can expose private keys or be mistaken for production wallets.

Mitigation: Use burner wallets only for testing and never fund them with real assets; save keys only according to the user's security practices if persistence is needed.

## Reference(s):

- [GizmoLab Tools](https://tools.gizmolab.io/)
- [GizmoLab UI Library](https://ui.gizmolab.io/)
- [GizmoLab UI Documentation](https://ui.gizmolab.io/docs/)
- [GizmoLab Skill Page](https://clawhub.ai/gizmo-dev/skills/gizmolab-tools)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with browser-action steps, URLs, and code or installation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct wallet-connected blockchain actions and external code installation; human approval and inspection are required before transactions or project changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
