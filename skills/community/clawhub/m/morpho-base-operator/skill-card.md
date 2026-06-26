## Description: <br>
Operates a Base-first Morpho vault workflow with registry-based planning, external signature collection, pinned MCP execution, reconciliation, and report archival. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walioo](https://clawhub.ai/user/walioo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DeFi operators use this skill to plan and execute registry-constrained Morpho vault operations on Base while keeping signing authority outside the agent host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact DeFi vault execution can move assets incorrectly if registry, market, or adapter data is wrong. <br>
Mitigation: Use only a verified registry, reject unknown or paused markets before execution, and require explicit human approval for each transaction. <br>
Risk: Under-specified signing boundaries could allow an agent host to gain excessive transaction authority. <br>
Mitigation: Keep authority in an external signer or hardware wallet and never give the agent direct raw private-key control. <br>
Risk: MCP execution boundaries could be unsafe if the runtime or tool surface is not pinned and trusted. <br>
Mitigation: Use a trusted pinned MCP implementation, verify the required tool surface before execution, and reconcile receipts before archiving reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/walioo/morpho-base-operator) <br>
- [Incident Response Reference](references/incident-response.md) <br>
- [Policy](references/policy.md) <br>
- [Registry](references/registry.md) <br>
- [Runbook Reference](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with ordered operational steps and inline commands or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce deterministic plans, execution checklists, reconciliation notes, and archive/report guidance; does not include user secrets or signing keys.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
