## Description: <br>
Extract text from PDF files for LLM processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract plain text from local PDF documents for LLM processing, including full-document extraction or specified page ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted PDF text may contain confidential, personal, or internal information. <br>
Mitigation: Treat extracted content as sensitive and avoid sending it to webhooks, shared logs, or group channels unless the user intentionally chooses an appropriate sharing path. <br>
Risk: Autonomous file creation can persist sensitive extracted content on disk. <br>
Mitigation: Return extracted text in the conversation by default and write to disk only when the user explicitly names an output file. <br>
Risk: The skill depends on the local pdftotext binary from poppler-utils. <br>
Mitigation: Confirm pdftotext is installed locally before use and install poppler-utils through the system package manager when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/pdf-extract-hardened) <br>
- [Faberlens PDF Extract Safety Evaluation](https://faberlens.ai/explore/pdf-extract) <br>
- [Faberlens](https://faberlens.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns extracted text by default; writes to a named output file only when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
