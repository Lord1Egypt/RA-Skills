## Description:

Turns npm supply-chain findings or vague concerns about suspicious packages into concrete incident-response steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salemalem](https://clawhub.ai/user/salemalem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security responders use the skill to turn NPMScan findings or a described supply-chain concern into a relevant remediation playbook. It can interpret vague symptoms, while package-specific responses rely on investigation findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A benign scan verdict is not a guarantee of zero risk.

Mitigation: Review whether the skill's guidance fits your incident-response workflow before installing.

## Reference(s):

- [NPMScan MCP server](https://npmscan.com/api/mcp)
- [ClawHub release page](https://clawhub.ai/salemalem/skills/npmscan-incident-response)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with remediation steps and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory steps are based on NPMScan results or a best-fit symptom playbook; the skill does not change packages.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
