## Description:

根据用户提供的研发材料或初步想法，生成供专利代理人审阅的中文技术交底书及核对说明。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can turn R&D materials or an early invention idea into a Chinese technical disclosure for review by a patent agent. It can also outline possible invention directions and provide a separate checklist of assumptions and missing information; it does not prepare a patent application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential storage and authenticated network requests need review before use.

Mitigation: Provide the API key privately through PATENTMAX_API_KEY, not in chat; use a version that protects credential files and restricts authenticated requests to trusted HTTPS destinations.

Risk: Selected invention materials are sent to PatentMax, and submissions may incur charges.

Mitigation: Review the materials for sensitive information and review PatentMax's confidentiality and retention terms; approve the upload and charges before submitting.

## Reference(s):

- [ClawHub release](https://clawhub.ai/ip930/skills/patent-disclosure-cn)
- [Materials guide](references/materials-guide.md)
- [Workflow guide](references/workflow.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Word documents, Analysis, Guidance]

**Output Format:** [DOCX technical disclosure and review notes, with task results and user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include inferred content and items needing inventor confirmation; generated documents are not patent applications.]

## Skill Version(s):

1.1.9 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
