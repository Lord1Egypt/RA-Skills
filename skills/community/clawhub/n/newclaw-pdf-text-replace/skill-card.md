## Description: <br>
Replace text in PDF files while preserving visual fidelity, including custom font encodings, embedded subsets, encrypted PDFs, image-based scans, variable-length replacements, and style changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newclaw26](https://clawhub.ai/user/newclaw26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document operators use this skill to replace specific text in PDF files when the original source document is unavailable or when preserving the PDF's visual layout matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter PDF contents, which may affect legally or operationally sensitive documents. <br>
Mitigation: Use it only on documents you are authorized to modify, keep originals, and review generated PDFs before sharing or relying on them. <br>
Risk: Encrypted PDFs may be handled through decrypted temporary files. <br>
Mitigation: Avoid encrypted or highly sensitive PDFs unless running in an isolated workspace and verifying temporary decrypted files are removed afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newclaw26/newclaw-pdf-text-replace) <br>
- [Skill homepage](https://clawhub.ai/skills/newclaw-pdf-text-replace) <br>
- [PDF Font CMap Encoding Guide](references/cmap-encoding-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce modified PDF files when its scripts are executed by the agent.] <br>

## Skill Version(s): <br>
2.1.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
