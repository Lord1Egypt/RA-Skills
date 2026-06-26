## Description: <br>
Read, extract, summarize, and compare office documents including PDF, Word, Excel, and PowerPoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windrunner20](https://clawhub.ai/user/windrunner20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract text from PDF, Word, Excel, and PowerPoint files so an agent can summarize, search, outline, extract fields from, or compare office documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted document text can appear in chat output, command output, logs, or orchestration traces. <br>
Mitigation: Use the skill only on documents the user intentionally provides, avoid highly confidential documents unless necessary, and clearly separate extracted content from summary or inference. <br>
Risk: OCR, spreadsheet, and layout extraction may be incomplete or noisy. <br>
Mitigation: State extraction limits, flag weak or OCR-derived content, and avoid claiming precise layout, formula, chart, or visual interpretation. <br>
Risk: Local parsers and OCR tools process user-selected files. <br>
Mitigation: Process only trusted files and keep document parsing and OCR dependencies updated. <br>


## Reference(s): <br>
- [Capabilities and Boundaries](references/capabilities.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON extraction results and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled extractor can cap output text with --max-chars and marks truncated results.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
