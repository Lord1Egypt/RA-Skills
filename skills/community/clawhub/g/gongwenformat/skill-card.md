## Description:

Format, review, or rewrite Chinese official documents to the GB/T 9704-2012 official-document format standard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johamwon](https://clawhub.ai/user/johamwon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and administrative staff use this skill to format, review, or rewrite Chinese official-document drafts, including notices, reports, requests, replies, letters, meeting minutes, and orders. It can return normalized document text, exact revision instructions, formatting checklists, and local script commands for supported Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scripts process local Word documents and can alter layout, fonts, page setup, and pagination.

Mitigation: Run the scripts only on documents intended for processing, keep an original copy, and manually review generated .docx output in Word or WPS.

Risk: Document parsing and formatting depend on third-party Python packages.

Mitigation: Install dependencies in a virtual environment and consider pinning reviewed versions of python-docx and olefile.

Risk: The formatter leaves some official-document header and footer work for manual completion.

Mitigation: Use the generated checklist and complete unresolved header, red-line, footer, seal, and metadata elements in Word or WPS before release.

## Reference(s):

- [Gongwen Formatting Guidelines](references/formatting_guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/johamwon/skills/gongwenformat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with document text, checklists, revision instructions, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or transform local .docx and .txt files when the user asks to run the bundled scripts; manual Word or WPS review is still needed for some header and footer elements.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
