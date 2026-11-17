## Description:

Diagnoses and repairs Chinese font rendering problems in PDFs, audits glyphs before delivery, and provides progressive PDF and PowerPoint export fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to inspect PDF font risks, locate missing glyphs, and repair or export PDFs that may display Chinese text incorrectly on other devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair operations may replace an original PDF, and text-preservation options may not be honored.

Mitigation: Work on disposable copies, choose explicit unused output paths, and verify the original and the repaired file's searchable text.

Risk: Validation may report success after incomplete checks.

Mitigation: Check extracted and searchable text, inspect glyph coverage, and review rendered pages visually before delivery.

Risk: Outline or scanned fallback PDFs may lose text search and copying.

Mitigation: Keep the native PDF alongside any converted version and use the converted copy only after checking the native version on the target device.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sedey999/skills/pdf-font-fixer)
- [Noto CJK releases](https://github.com/notofonts/noto-cjk/releases)
- [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC)
- [Ghostscript downloads](https://ghostscript.com/releases/gsdnld.html)
- [LibreOffice downloads](https://www.libreoffice.org/download/)

## Skill Output:

**Output Type(s):** [Analysis, Files, Configuration instructions]

**Output Format:** [PDF files, plain-text diagnostics, and CSS configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide paired native and converted PDFs; outline and scanned versions can lose text search and copy support.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
