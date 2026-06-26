## Description: <br>
The Agent Insurance Playbook helps agents build agent-native insurance infrastructure for risk pools, liability bonds, automated claims processing, regulatory compliance, disputes, trust verification, ledger reconciliation, and SLA enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this guide to design GreenHelix-based insurance workflows for autonomous agent commerce, including underwriting, policy lifecycle management, claims adjudication, reinsurance patterns, and compliance reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can create or change wallets, payments, claims, disputes, settlements, ledger entries, organizations, and webhooks when adapted and run against live services. <br>
Mitigation: Use sandbox endpoints, least-privilege test tokens, spending limits, and human approval before any wallet, payment, dispute, settlement, ledger, organization, or webhook operation. <br>
Risk: The guide is non-executing documentation, but its examples involve high-impact financial and identity-adjacent workflows. <br>
Mitigation: Avoid real funds, real claim data, and real identity data until the workflow has been reviewed, tested with non-production data, and approved for the relevant use case. <br>
Risk: Credential and endpoint choices can change the examples from sandbox exploration into live financial API activity. <br>
Mitigation: Verify every endpoint and token before running examples, default to the sandbox URL, and require explicit review before switching to production credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mirni/greenhelix-agent-insurance-risk-pools) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix A2A Commerce API](https://api.greenhelix.net/v1) <br>
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guide with explanatory prose, tables, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executing guide; examples should be limited to sandbox endpoints, test credentials, and reviewed financial workflows before any live use.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
