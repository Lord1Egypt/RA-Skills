## Description:

AI-powered global compliance checker, document generator, and risk assessor for GDPR, CCPA, SOC2, ISO27001, HIPAA and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:


## Use Case:

Developers, compliance teams, and enterprises use this skill to check documents, generate compliance policies, assess multi-region compliance risks, and query requirements for privacy and security frameworks. Outputs should be reviewed by qualified legal or compliance personnel before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package identity mismatch: the target and root skill describe compliance, while the English and Chinese artifact files describe an unrelated video generator.

Mitigation: Do not install this package as-is; republish it so all language files describe the same skill before deployment.

Risk: Commands may install packages, run CLIs, or process user-provided documents and arguments.

Mitigation: Require explicit user confirmation before installation or execution, pin dependencies, and validate file paths and user-provided arguments.

Risk: Compliance reports and generated policies may be mistaken for legal advice or guaranteed compliance.

Mitigation: Require qualified legal or compliance review and avoid presenting generated outputs as complete or authoritative compliance determinations.

Risk: Unaligned artifact behavior may send content to external APIs or execute commands outside the expected compliance workflow.

Mitigation: Review the package contents and scanner summary before use, and require explicit confirmation before sending content to external services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/global-compliance)
- [Repository link from release changelog](https://github.com/ZhenRobotics/openclaw-global-compliance)
- [Support issues link from artifact](https://github.com/ZhenRobotics/openclaw-global-compliance/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated document or report file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or reference JSON, Markdown, PDF, and HTML compliance outputs depending on command options.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
