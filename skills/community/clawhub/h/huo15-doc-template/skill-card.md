## Description:

Provides Chinese Word document template guidance and Python snippets for generating Huo15-branded .docx documents with prescribed fonts, margins, headers, footers, page numbers, and naming conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to create formal Chinese Word documents such as contracts, quotes, meeting minutes, reports, notices, and specification documents with consistent company formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically use local Odoo credentials while generating documents.

Mitigation: Install only where Huo15-branded Chinese documents are intended and require explicit user approval before credential-backed company-system access.

Risk: The embedded Odoo retrieval code disables TLS certificate verification.

Mitigation: Restore TLS verification before using the retrieval code and constrain access to approved endpoints.

Risk: Company identity details and logo assets may be pulled from external Huo15 endpoints.

Mitigation: Confirm the endpoint scope and data handling expectations before enabling automatic company-system retrieval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-doc-template)
- [Huo15 company system](https://huihuoyun.huo15.com)
- [Huo15 website logo endpoint](https://huihuoyun.huo15.com/web/image/website/1/logo)
- [Huo15 fallback logo asset](https://tools.huo15.com/uploads/images/system/logo-colours.png)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python code snippets and generated .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Chinese Word/WPS formatting conventions and may retrieve company logo and profile information from configured Huo15 Odoo services.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
