## Description: <br>
Converts office automation documents, including PDF, PPTX, DOCX, XLSX, and CSV files, into clean, readable Markdown when the user explicitly requests conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naimalarain13](https://clawhub.ai/user/naimalarain13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to convert office documents into Markdown for review, editing, analysis, or reuse. It is intended for explicit conversion requests and supports text-first extraction with optional vision-based OCR for scanned or image-only content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime dependency downloads can introduce supply-chain and network-execution risk. <br>
Mitigation: Install only when runtime downloads of pinned Python packages are acceptable, and review or mirror dependencies before use in restricted environments. <br>
Risk: Vision/OCR for scanned or image-only content sends page images or embedded images to Anthropic for processing. <br>
Mitigation: Use text-only conversion for confidential documents, and enable vision only after explicit user approval for external processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naimalarain13/office-to-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown file with a brief text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skipped-page notes when vision extraction is declined or unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
