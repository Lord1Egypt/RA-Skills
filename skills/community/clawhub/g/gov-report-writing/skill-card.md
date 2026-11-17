## Description:

Write formal Chinese government and state-owned enterprise documents including annual reports, work summaries, party-building reports, meeting minutes, and official correspondence following GB/T 9704-2012 standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mogician11111](https://clawhub.ai/user/mogician11111)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and document authors use this skill to draft, polish, format, and check Chinese official documents for government, state-owned enterprise, and public-institution workflows. It supports template selection, GB/T 9704-2012 formatting guidance, confidentiality checks, and optional quality or format validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may submit confidential or sensitive workplace material for drafting.

Mitigation: Use the skill only for non-confidential Chinese official-document drafting, invoke it deliberately for sensitive workplace material, and redact or replace sensitive facts before use.

Risk: Installation through an untrusted package flow could expose users to the wrong installer or package version.

Mitigation: Install through a trusted marketplace flow when possible, or pin and verify the installer version before using npx.

Risk: Validation scripts process local document files and may be unsuitable for untrusted or unusually large DOCX inputs.

Mitigation: Run the validation scripts only on trusted, expected-size files and avoid untrusted or unusually large DOCX inputs.

Risk: Generated official documents can contain placeholders, inaccurate facts, or unsupported policy references.

Mitigation: Have a responsible reviewer verify all placeholders, dates, names, departments, data, and policy citations before submission or distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mogician11111/skills/gov-report-writing)
- [Project homepage](https://github.com/Mogician11111/gov-report-writing)
- [README](artifact/README.md)
- [GB/T 9704-2012 format reference](artifact/references/gb-t9704-format.md)
- [Report templates](artifact/references/report-templates.md)
- [Vocabulary guide](artifact/references/vocabulary-guide.md)
- [Quality scoring standard](artifact/references/quality-scoring.md)
- [Capability matrix](artifact/references/capability-matrix.md)
- [Policy database](artifact/references/policy-database.md)
- [AI trace detection rules](artifact/references/ai-traces.md)
- [Polishing guide](artifact/references/polishing-guide.md)
- [Case examples](artifact/references/case-examples.md)
- [Expression library](artifact/references/expression-library.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese official-document drafts, Markdown instructions, optional DOCX-oriented formatting guidance, and validation report output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include placeholders for missing or sensitive facts and safety reminders for users to verify dates, names, data, and confidentiality requirements.]

## Skill Version(s):

1.6.0 (source: server release evidence, target metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
