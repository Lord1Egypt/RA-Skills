## Description: <br>
Web3 bug bounty and protocol security agent for evidence-backed vulnerability discovery and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaniidev](https://clawhub.ai/user/shaniidev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security researchers use Lance for authorized Web3 bug bounty and protocol security reviews across smart contracts, DeFi protocols, wallet/signature flows, bridges, EVM bytecode/source, Solidity repositories, and Sui Move packages. It emphasizes evidence-backed findings that pass exploitability, economic feasibility, false-positive, and triage gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for Web3 security review and could be misapplied to targets without authorization. <br>
Mitigation: Use it only with explicit scope confirmation from a bug bounty program, written permission, or owned/internal systems. <br>
Risk: Audit prompts or local inputs may expose unrelated private repositories or secrets. <br>
Mitigation: Limit provided targets to the authorized review scope and avoid sharing unrelated private code or credentials. <br>
Risk: Included local scripts write generated reports or normalized outputs to user-selected paths. <br>
Mitigation: Review script arguments and output paths before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shaniidev/lance) <br>
- [Project Homepage](https://github.com/shaniidev/lance) <br>
- [Workflow](references/workflow.md) <br>
- [Audit Rules](references/audit-rules.md) <br>
- [Exploit Validation](references/exploit-validation.md) <br>
- [Economic Validation](references/economic-validation.md) <br>
- [False Positive Elimination](references/false-positive-elimination.md) <br>
- [Severity Guide Web3](references/severity-guide-web3.md) <br>
- [Triage Simulation](references/triage-simulation.md) <br>
- [Finding Schema](assets/templates/finding.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured finding text, JSON-compatible finding data, and local shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs only findings that pass exploitability, economic feasibility, false-positive, and triage gates; reports no exploitable on-chain vulnerabilities when no finding passes.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter, changelog released 2026-02-25, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
