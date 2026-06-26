## Description: <br>
Agent Workforce Orchestration: Hybrid Human+AI Teams helps build agent-led workforce orchestration for capability matching, escrow-based payments, unified reputation scoring, SLA enforcement, dispute resolution, and compliance reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and workforce automation teams use this skill to design an agent-led orchestration system for hybrid human and AI workforces. It provides patterns for capability matching, escrow payments, reputation scoring, SLA enforcement, dispute handling, and compliance reporting with GreenHelix examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runnable examples can create wallets, escrows, payments, disputes, and other live account changes if pointed at a production GreenHelix account. <br>
Mitigation: Use the sandbox or a non-production endpoint first, require human approval before wallet or payment operations, and avoid running financial examples against live accounts without review. <br>
Risk: The skill references GREENHELIX_API_KEY for API authentication. <br>
Mitigation: Use least-privilege test credentials, store keys outside chat and source files, and rotate credentials after testing. <br>
Risk: Security evidence flags the guide as suspicious because setup text may understate credential, sandbox, and budget-control requirements. <br>
Mitigation: Set budget limits, verify the endpoint before execution, and review all examples before adapting them for operational workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mirni/greenhelix-agent-workforce-orchestration) <br>
- [GreenHelix Sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API Endpoint](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python code examples, architecture diagrams, tables, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples reference GREENHELIX_API_KEY and can perform wallet, escrow, payment, dispute, and compliance actions if adapted and run against a live GreenHelix account.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
