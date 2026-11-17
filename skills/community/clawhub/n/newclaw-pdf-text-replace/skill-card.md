## Description:

Replace text in PDF files while preserving visual fidelity, including custom font encodings, embedded subsets, encrypted PDFs, image-based scans with OCR, variable-length replacements, and style changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newclaw26](https://clawhub.ai/user/newclaw26)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document operators, and agent users use this skill to modify specific text in local PDF files when the original editable source is unavailable or when PDF-level replacement is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Encrypted PDFs, passwords, or sensitive document excerpts may be exposed through local files or process arguments.

Mitigation: Use the skill only in a controlled local environment, avoid confidential documents unless approved, pass passwords through controlled workflows, and clean temporary files after processing.

Risk: Password-protected PDFs may be written out decrypted unless explicitly re-encrypted.

Mitigation: Review output files before sharing or storing them, and re-encrypt sensitive PDFs immediately when encryption must be preserved.

## Reference(s):

- [PDF Font CMap Encoding Guide](references/cmap-encoding-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/skills/newclaw-pdf-text-replace)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance, files]

**Output Format:** [Markdown guidance with shell and Python examples; generated PDF files when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create modified PDF outputs and temporary local work files during OCR or encrypted-PDF handling.]

## Skill Version(s):

2.1.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
