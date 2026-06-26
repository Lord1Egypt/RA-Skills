## Description: <br>
GizmoLab Tools guides agents through GizmoLab's browser-based blockchain developer tools and Web3 UI component library for smart contract interactions, token workflows, transaction decoding, ENS lookup, swaps, and dApp component integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gizmo-dev](https://clawhub.ai/user/gizmo-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Web3 builders use this skill to operate GizmoLab's web tools for blockchain lookups, transaction decoding, contract interaction, token workflows, swaps, and Web3 UI component integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent into wallet-connected blockchain operations, including token creation, minting, swaps, and contract writes. <br>
Mitigation: Use testnets or disposable wallets where possible; verify the GizmoLab URL, network, contract address, function, token amounts, fees, slippage, and destination before allowing any wallet approval or transaction confirmation. <br>
Risk: Burner wallet or private-key workflows can expose real funds if used outside testing. <br>
Mitigation: Use burner wallets only for testing, never use them for real funds, and require the user to decide whether any generated key material should be saved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gizmo-dev/gizmolab-tools) <br>
- [GizmoLab blockchain tools](https://tools.gizmolab.io/) <br>
- [GizmoLab UI library](https://ui.gizmolab.io/) <br>
- [GizmoLab UI docs](https://ui.gizmolab.io/docs/) <br>
- [GizmoLab UI components](https://ui.gizmolab.io/components) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with browser action steps and code or installation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct browser-based wallet workflows; transaction approvals require explicit user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
