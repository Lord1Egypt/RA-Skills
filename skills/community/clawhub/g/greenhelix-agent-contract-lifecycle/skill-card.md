## Description: <br>
Build automated contract lifecycle management for AI agents with machine-readable SLAs, escrow-backed execution, real-time obligation tracking, automated penalty enforcement, renewal workflows, and Python examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this guide to design machine-readable contract workflows for AI-agent commerce, including SLAs, escrow-backed execution, breach monitoring, penalties, renewals, termination, and audit trails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide teaches autonomous financial contract, escrow, penalty, dispute, and termination workflows. <br>
Mitigation: Require human approvals, transaction caps, and sandbox-only testing before adapting examples to systems that can move funds. <br>
Risk: Credential and sandbox expectations are inconsistent across the artifact and examples. <br>
Mitigation: Separate credentials by environment, keep production keys out of examples, and verify each endpoint and authorization path before use. <br>
Risk: Penalty, refund, release, and termination logic could move funds incorrectly if copied without validation. <br>
Mitigation: Add independent tests and manual review for all fund-moving paths before any production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-contract-lifecycle) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python and JSON code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples target GreenHelix sandbox and API endpoints.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
