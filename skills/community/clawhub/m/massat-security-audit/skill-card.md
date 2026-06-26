## Description: <br>
Security audit for multi-agent AI systems - OWASP ASI01-ASI10. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[craigmbrown](https://clawhub.ai/user/craigmbrown) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security teams use this skill to request BlindOracle MASSAT audits of multi-agent systems against OWASP ASI01-ASI10 before deployment, after major changes, or for compliance reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send repository URLs or system details to an external security-audit API. <br>
Mitigation: Confirm the target information is approved for external review before running the audit. <br>
Risk: The full audit path uses an optional x402 payment flow. <br>
Mitigation: Use the free quick scan unless intentionally approving the paid full audit and its payment header. <br>


## Reference(s): <br>
- [Massat Security Audit on ClawHub](https://clawhub.ai/craigmbrown/massat-security-audit) <br>
- [MASSAT Framework](https://github.com/craigmbrown/massat-framework) <br>
- [BlindOracle Marketplace](https://craigmbrown.com/blindoracle/) <br>
- [Whitepaper: Security Auditing a 94-Agent Fleet](https://craigmbrown.com/blindoracle/blog/agent-security-crisis.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with curl examples and JSON response structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes free quick-scan guidance and an optional paid x402 full-audit path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
