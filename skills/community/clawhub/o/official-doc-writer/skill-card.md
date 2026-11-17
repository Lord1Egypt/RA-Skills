## Description:

Generates Chinese party and government official documents such as notices, reports, requests, and letters, with guided information collection and GB/T 9704-2012 formatting for Word export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wonderslife](https://clawhub.ai/user/wonderslife)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agents drafting Chinese official documents use this skill to collect required document elements, compose standard phrasing, and generate GB/T 9704-2012-style Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The font installer can permanently change system fonts and Windows registry settings.

Mitigation: Review the skill before installing; prefer manual per-user font installation or project-local font handling unless elevated OS changes are understood and approved.

Risk: Document generation writes output files to local paths.

Mitigation: Use explicit trusted output paths and review generated .docx files before distribution.

## Reference(s):

- [GB/T 9704-2012 党政机关公文格式](references/GBT_9704-2012_党政机关公文格式.md)
- [方正字库官网](http://www.foundertype.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated documents are .docx files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .docx outputs and font-list files when the bundled scripts are used.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
