## Description: <br>
Payment Skill helps agents create payment requests, check payment status, and initiate refunds through a configured payment API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neverSatRabbit](https://clawhub.ai/user/neverSatRabbit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to integrate payment workflows that create payment authorization requests, query transaction status, and initiate refunds through configured credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use payment credentials to create payments and initiate refunds. <br>
Mitigation: Use least-privilege, low-limit credentials and require manual approval outside the skill before any payment creation or refund. <br>
Risk: Endpoint and permission ambiguity can send payment operations to an unintended API domain. <br>
Mitigation: Verify the intended payment API domain before installation and before setting PAYMENT_API_URL. <br>
Risk: Diagnostics and local logs may expose live secrets or sensitive payment metadata. <br>
Mitigation: Avoid running diagnostics with live secrets in captured logs and treat local logs as sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neverSatRabbit/payment-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON payment operation responses with setup and environment configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires payment API credentials and network access to the configured payment API.] <br>

## Skill Version(s): <br>
1.0.3 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
