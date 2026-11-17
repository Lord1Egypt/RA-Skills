## Description:

Helps users prepare responses to Chinese patent office actions, including a draft response statement, amended claims, and an amendment comparison table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent applicants and patent professionals use this skill to review Chinese examination objections, select a response strategy, and prepare draft response documents for professional review.

### Deployment Geography for Use:

China (Chinese patent applications only)

## Known Risks and Mitigations:

Risk: Full office-action and patent-application materials are sent to a third-party service.

Mitigation: Check confidentiality, client authorization, and export-control constraints before consenting to upload.

Risk: Draft claims and response arguments may be unsuitable for filing without review.

Mitigation: Have a patent professional review the response and amendments before submission.

Risk: Server-provided output filenames may create unintended local file paths.

Mitigation: Sanitize downloaded filenames and verify the output directory before saving Word files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/patentmax-oa-response)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Chinese-language response text and Word (.docx) documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft statement, amended claims, and amendment comparison table; patent-agent review required before filing.]

## Skill Version(s):

1.0.1 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
