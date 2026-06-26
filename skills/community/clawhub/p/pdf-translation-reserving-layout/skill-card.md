## Description: <br>
Translate PDFs by extracting page text locally, preserving page organization for agent-native translation, and using a hosted fallback only when local handling fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[getlinnk](https://clawhub.ai/user/getlinnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and external users use this skill to translate born-digital or lightly scanned PDFs into page-organized translated text while keeping processing local by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the hosted fallback may send confidential, regulated, unpublished, or personal documents to a third party. <br>
Mitigation: Use the local extraction and agent-native translation workflow for sensitive documents; use the hosted fallback only when the user intentionally accepts third-party handling. <br>
Risk: Installing local PDF processing dependencies from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install local dependencies only from trusted package sources and review the helper commands before execution. <br>


## Reference(s): <br>
- [BabelDOC Notes](references/babeldoc-notes.md) <br>
- [Hosted document translation fallback](https://linnk.ai/doc-translator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown, JSONL, or page-organized text with shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve page numbers and use batch files when long PDFs are translated in parallel.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
