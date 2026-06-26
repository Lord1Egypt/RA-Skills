## Description: <br>
Self-hosted PDF operations and conversions with metered usage output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cap-txt](https://clawhub.ai/user/cap-txt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run local PDF workflows such as merging, splitting, compression, conversion, OCR, redaction, signing, and usage reporting while keeping inputs and outputs on disk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch URL content during HTML-to-PDF workflows. <br>
Mitigation: Use the skill only with trusted URLs and PDFs, especially in sensitive environments. <br>
Risk: The translate and agent flows can run user-supplied LLM commands. <br>
Mitigation: Do not use --llm-cmd with untrusted commands; prefer a controlled local backend when enabling LLM-backed workflows. <br>
Risk: Confidential document content may be sent to an LLM backend during translation. <br>
Mitigation: Avoid the translate feature for confidential PDFs unless you control and trust the LLM backend. <br>
Risk: PDF passwords may be visible to local users or monitoring tools while qpdf runs. <br>
Mitigation: Avoid running password-protected PDF operations in shared or heavily monitored local environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cap-txt/pdfagent) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance and shell commands; the CLI can emit JSON usage data and file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PDFs and converted document files are written to disk; --json output includes usage and outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
