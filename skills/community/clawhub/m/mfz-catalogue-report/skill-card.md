## Description:

将单份 DRG 或 DIP 目录的 XLSX、PDF、扫描/OCR PDF 或 DOCX 原始材料整理为可检索交互报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[u201013903](https://clawhub.ai/user/u201013903)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to turn one DRG or DIP catalogue source file into traceable governance data and an interactive report. It supports catalogue extraction, validation, review resolution, quality summaries, warnings, and a final report link through the configured MedGroup Catalogue Report MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalogue source files are uploaded to an external MedGroup service.

Mitigation: Use the skill only with authorized DRG/DIP catalogue files and avoid patient-level, confidential, or unrelated documents unless the user is authorized and accepts the upload workflow.

Risk: The workflow requires an API key for the MedGroup MCP.

Mitigation: Keep the API key out of Skill files, scripts, reports, and user-visible responses, and send it only through the configured Authorization header.

Risk: OCR or scanned PDFs can produce uncertain codes, numbers, separators, or row alignment.

Mitigation: Provide field confidence, avoid guessing or rewriting values, and resolve validation review tasks against the original source before reporting completion.

Risk: A validation state of blocked or needs_review can be mistaken for a completed report.

Mitigation: Only present the report as complete after the workflow reaches report_ready or report_ready_with_warnings; otherwise report the current status and required review.

## Reference(s):

- [Skill page](https://clawhub.ai/u201013903/skills/mfz-catalogue-report)
- [MedGroup Catalogue Report MCP endpoint](https://medgroup.medchat.fun/catalogue-report/mcp)
- [Exchange contract](references/exchange-contract.md)
- [Review protocol](references/review-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or plain text status updates with quality summary, warnings, and report URL; structured catalogue rows and review resolutions are prepared for the MCP workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles one DRG or DIP catalogue per task and stops when extraction, validation, or review cannot meet the stated data quality requirements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
