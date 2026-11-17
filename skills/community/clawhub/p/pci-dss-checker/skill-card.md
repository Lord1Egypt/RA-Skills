## Description:

Evaluates an organization's payment card processing environment against PCI DSS requirements and returns a comprehensive compliance assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, payment processors, service providers, security teams, and compliance officers use this skill to submit PCI scoping and security-control answers to a third-party API and receive a PCI DSS compliance assessment with scores, requirement summaries, recommendations, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends PCI scoping and security-control details to a third-party API, which may expose sensitive compliance information.

Mitigation: Confirm organizational approval for third-party data sharing before use, and omit live cardholder data, credentials, secrets, and unnecessary infrastructure details.

Risk: Compliance results depend on the submitted self-assessment inputs and may not replace formal PCI DSS validation.

Mitigation: Have qualified security or compliance personnel review outputs before using them for audit, remediation, or governance decisions.

## Reference(s):

- [PCI DSS Checker ClawHub Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/pci-dss-checker)
- [PCI DSS Checker API Docs](https://api.mkkpro.com:8038/docs)
- [PCI DSS Checker API Route](https://api.mkkpro.com/compliance/pci-dss-checker)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON response containing compliance status, overall score, PCI DSS requirement summaries, recommendations, and next steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structured organization and PCI security-control inputs; do not submit live cardholder data, credentials, secrets, or unnecessary infrastructure details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
