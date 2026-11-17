## Description:

Generates a coordinated package of civil and commercial litigation filing documents, including a complaint, preservation materials, authorization documents, interview record, retainer agreement, and an Excel interest-loss calculation sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leahlu0124-creator](https://clawhub.ai/user/leahlu0124-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Legal professionals and support staff use this skill to draft Chinese civil and commercial litigation filing packages from case facts, templates, legal database lookups, and interest calculation inputs. Generated materials require professional review before filing or client delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes confidential legal and client materials.

Mitigation: Use only trusted or redacted uploads and review generated files before sharing them outside the matter team.

Risk: Generated statutes, case references, or legal conclusions may be inaccurate when professional legal databases are unavailable or incomplete.

Mitigation: Verify every citation and legal position with a qualified lawyer and current authoritative legal sources before filing.

Risk: The Excel interest calculator can receive user-provided values that may affect workbook formulas or shared spreadsheet content.

Mitigation: Validate numeric fields and neutralize formula-prefixed text before distributing generated workbooks.

Risk: Custom templates can replace bundled templates and change generated legal language.

Mitigation: Manually review any custom template before using it for client-facing documents.

## Reference(s):

- [Complaint Template](artifact/references/complaint_template.md)
- [Preservation Application Template](artifact/references/preservation_application_template.md)
- [Guarantee Letter Template](artifact/references/guarantee_letter_template.md)
- [Power of Attorney Template](artifact/references/power_of_attorney_template.md)
- [Legal Representative Certificate Template](artifact/references/legal_rep_certificate_template.md)
- [Interview Record Template](artifact/references/interview_record_template.md)
- [Retainer Agreement Template](artifact/references/retainer_agreement_template.md)
- [Yuandian Tools Guide](artifact/references/yuandian_tools_guide.md)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, Shell commands]

**Output Format:** [Markdown guidance plus generated .docx litigation documents and an .xlsx interest calculation workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates up to eight coordinated documents; legal citations, confidential client facts, and spreadsheet formulas require review before use.]

## Skill Version(s):

2.2.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
