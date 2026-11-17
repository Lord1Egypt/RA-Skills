## Description:

PDF.co (pdf.co). Use this skill for ANY PDF.co request — reading, creating, and updating data. Whenever a task involves PDF.co, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect PDFs, extract text or metadata, convert HTML or web pages to PDF, and compress, merge, or split PDF documents through PDF.co.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run downloaded CLI installer code that has not been verified, and skill synchronization can install or refresh additional agent skills.

Mitigation: Review setup before enabling the skill, install a verified CLI release separately, and set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: PDF processing may send documents to OOMOL/PDF.co and conversion actions may incur credit costs.

Mitigation: Submit only documents authorized for OOMOL/PDF.co processing and check credit costs before conversion actions.

## Reference(s):

- [PDF.co API documentation](https://docs.pdf.co/api-reference/index)
- [PDF.co homepage](https://pdf.co)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Text, File URLs]

**Output Format:** [oo CLI commands with JSON payloads and PDF.co response data, including text or generated file URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs should follow the live connector schema; available results depend on the selected action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
