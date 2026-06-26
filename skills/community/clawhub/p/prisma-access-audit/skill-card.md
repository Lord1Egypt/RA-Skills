## Description: <br>
Palo Alto Prisma Access SASE audit for security policy evaluation across mobile users and remote networks, GlobalProtect Cloud Service configuration review, service connection validation, threat prevention profile assessment, and Strata Cloud Manager posture analysis across Prisma Access tenants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, network security teams, and auditors use this skill to review Prisma Access tenant posture, identify policy and profile gaps, validate tunnel and service connection health, and prepare remediation guidance for SASE environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Prisma Access tenant credentials and may expose authorization headers or user, device, tenant, and network telemetry in audit notes or shared reports. <br>
Mitigation: Use a dedicated Auditor or View-Only service account, store tokens in an approved secret store, and redact Authorization headers plus sensitive tenant telemetry before sharing outputs. <br>
Risk: Running the audit against the wrong tenant or endpoint could produce misleading security findings for the organization. <br>
Mitigation: Confirm the tenant, TSG ID, publisher-approved scope, and Palo Alto endpoints before use. <br>


## Reference(s): <br>
- [Prisma Access API Reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/prisma-access-audit) <br>
- [Prisma Access configuration API endpoint](https://api.sase.paloaltonetworks.com/sse/config/v1) <br>
- [Prisma Access OAuth token endpoint](https://auth.apps.paloaltonetworks.com/oauth2/access_token) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline API request examples, audit checklists, threshold tables, decision trees, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit guidance that depends on authorized Prisma Access API credentials and tenant context supplied by the operator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
