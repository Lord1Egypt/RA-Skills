## Description: <br>
Extract text from PDF files for LLM processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert PDF documents into plain text for downstream review, summarization, or LLM processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the required PDF utility from an untrusted source could introduce supply-chain risk. <br>
Mitigation: Install poppler-utils only from a trusted operating-system package repository. <br>
Risk: Extracted PDF text may contain sensitive content or instruction-like text that should not control agent behavior. <br>
Mitigation: Use the skill only on PDFs whose contents are appropriate for agent or model context, and treat extracted text as document content rather than trusted instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xejrax/pdf-extract) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text output with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pdftotext binary from poppler-utils and can extract full documents or selected page ranges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
