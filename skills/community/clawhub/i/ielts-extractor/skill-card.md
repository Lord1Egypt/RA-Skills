## Description:

Extracts IELTS reading passages and questions from Cambridge IELTS PDFs into structured JSON, with guidance for multi-page extraction and two-column layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lava-chen](https://clawhub.ai/user/lava-chen)

### License/Terms of Use:


## Use Case:

Developers and content maintainers use this skill to convert Cambridge IELTS reading PDF content into local structured test JSON and related image assets for IELTS practice applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads local IELTS PDFs and writes JSON or image assets into project paths.

Mitigation: Run it only on intended local files and review generated JSON and images before committing or publishing them.

Risk: Source PDFs may be copyrighted or otherwise restricted.

Mitigation: Confirm rights to use the PDFs and extracted content before publishing or sharing outputs.

## Reference(s):

- [JSON format guide](references/json-format.md)
- [PDF extraction guide](references/pdf-extraction.md)
- [Question type standards](references/question-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON snippets, Python examples, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured IELTS reading JSON content and may create referenced image assets in local project paths.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
