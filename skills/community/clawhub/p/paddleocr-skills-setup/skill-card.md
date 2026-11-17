## Description:

Install and configure two PaddleOCR agent skills for OCR text recognition and structured document parsing across compatible coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidenwu0209](https://clawhub.ai/user/aidenwu0209)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and engineers use this setup skill to install and verify PaddleOCR text-recognition and document-parsing skills for screenshots, scanned documents, PDFs, CJK OCR, tables, formulas, layout extraction, Markdown, and JSON workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow requests a global installation of mutable, unpinned OCR skills.

Mitigation: Review the install command before approving it, verify the repository and installer version, and prefer pinned versions or explicit skill names instead of a wildcard.

Risk: PaddleOCR tokens could be exposed if entered into chat, command history, source files, or logs.

Mitigation: Provide tokens only through secure local configuration for the target skill, and do not print, store, or echo tokens during setup.

Risk: The OCR service may not be ready until endpoint and token configuration are complete.

Mitigation: Report incomplete configuration plainly and avoid claiming the OCR service works until the installed target skills are configured and verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aidenwu0209/skills/paddleocr-skills-setup)
- [PaddleOCR Skills repository](https://github.com/Aidenwu0209/PaddleOCR-Skills)
- [PaddleOCR official site](https://www.paddleocr.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports prerequisite versions, executed commands, installed skill names and paths, and any remaining user configuration.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
