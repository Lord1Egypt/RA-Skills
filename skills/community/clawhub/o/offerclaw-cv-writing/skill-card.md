## Description:

Writes study abroad admissions CVs and resumes, primarily for master's applications, covering education, research, internships, publications, awards, and optional PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[offerclaw](https://clawhub.ai/user/offerclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External applicants and admissions advisors use this skill to collect applicant background details, draft or polish English graduate admissions CVs, review content quality, and optionally export the confirmed CV to PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default PDF export adds an OfferClaw footer watermark.

Mitigation: Use '--watermark off' or skip the exporter unless the footer is acceptable.

Risk: PDF export installs unpinned packages at runtime and CV files may contain sensitive personal and academic details.

Mitigation: Prefer pinned, reviewed dependencies or run export in a sandboxed environment before processing applicant data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/offerclaw/skills/offerclaw-cv-writing)
- [CV Information Requirements](references/info-requirements.md)
- [CV Writing Instructions](references/writing-instructions.md)
- [CV Format Example](references/cv-format-example.md)
- [CV Quality Checklist](references/quality-checklist.md)
- [Bullet Expansion Guide](references/bullet-expansion-guide.md)
- [PDF Export Scripts](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text review drafts, Markdown CV files, and optional PDF export commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write tagged Markdown for rendering and produce a PDF after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
