## Description:

Convert PDF to Word (.docx) via Foxit PhantomPDF/PDF Editor keyboard automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaohuaruan](https://clawhub.ai/user/qiaohuaruan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to guide PDF-to-DOCX conversion on Windows systems with the Chinese Foxit PhantomPDF or Foxit PDF Editor UI installed. It supports single-file, custom output directory, retry, force-close, and batch conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on GUI keyboard automation for the Chinese Foxit UI, so conversion can fail or affect the wrong window if focus changes or menu shortcuts differ.

Mitigation: Use it only on Windows systems with the Chinese Foxit UI, keep Foxit focused during conversion, and test one document before batch runs.

Risk: Batch conversion can create or replace .docx outputs with matching names.

Mitigation: Choose the output folder deliberately and back up or rename existing .docx files before running batch conversion.

Risk: The inspected artifact references a PowerShell conversion script that is not included in the package.

Mitigation: Confirm the referenced script is available from the trusted source before relying on the skill for automated conversion.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/qiaohuaruan/skills/tree/main/pdf-to-word)
- [ClawHub skill page](https://clawhub.ai/qiaohuaruan/skills/pdf-to-word-2)
- [Publisher profile](https://clawhub.ai/user/qiaohuaruan)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with PowerShell command examples and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for Windows/Foxit GUI automation and PDF-to-DOCX conversion workflows.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
