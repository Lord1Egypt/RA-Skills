## Description:

Assess ISO/IEC 42001:2023 AI Management System (AIMS) readiness and generate compliance gap analysis with remediation roadmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and governance teams use this skill to collect AI governance details, call the ToolWeb ISO 42001 API, and receive an AIMS readiness score, gap analysis, and remediation roadmap for ISO 42001 certification preparation and related AI governance work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends organization name, AI use, governance status, and control gap information to ToolWeb.

Mitigation: Use it only under acceptable privacy and contractual terms, and avoid sending confidential information beyond what is required for the assessment.

Risk: The skill performs paid third-party API calls that may be billed to the configured ToolWeb account.

Mitigation: Confirm the subscription, quota, and cost expectations before enabling the skill for routine use.

Risk: The security guidance flags unsafe API-key handling guidance.

Mitigation: Store TOOLWEB_API_KEY in a secret manager or protected runtime environment, and do not commit real keys to configuration files.

Risk: The bundled test script should be avoided until TLS verification is fixed.

Mitigation: Do not run the test script as-is; use a request path that validates TLS certificates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/iso42001-aims-readiness)
- [ToolWeb API portal](https://portal.toolweb.in)
- [ToolWeb ISO 42001 API endpoint](https://portal.toolweb.in/apis/iso42001)
- [ToolWeb platform](https://toolweb.in)
- [OpenClaw skills information](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown assessment summary with API call guidance and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API responses may include an overall score, readiness level, executive summary, detailed report, category scores, and priority actions.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
