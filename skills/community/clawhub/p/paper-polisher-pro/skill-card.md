## Description:

Provides authors with local AI-writing self-checks and academic writing guidance, including terminology, consistency, and style checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Academic writers use this skill to review their own drafts for AI-like passages, terminology and consistency issues, and writing conventions, then consider sentence-level suggestions. Results are for author self-review and should be interpreted within the documented language and text-length limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the release suspicious because reported behavior exceeded the stated writing-advice scope and its evaluation checks had reliability weaknesses.

Mitigation: Review the reported scope mismatches and evaluation evidence before installing; do not rely on performance claims until they have been checked.

Risk: Inspection was partial: 173 of 176 components were scanned, with some references and analyzer work incomplete, so the scan cannot establish that all behavior is safe or harmful.

Mitigation: Treat the scan as incomplete and inspect the remaining components and rerun a complete review before relying on the release.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/docsor1212/skills/paper-polisher-pro)
- [Usage guidance](artifact/references/best-practices.md)
- [Skill scope and limitations](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, HTML reports, Guidance]

**Output Format:** [JSON, Markdown, and HTML reports with human-readable findings and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local draft analysis; texts under 100 characters receive no AI-risk verdict; suggestions require author review.]

## Skill Version(s):

7.7.0 (source: SKILL.md frontmatter, skill.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
