## Description:

LiaoGong-OCR helps agents extract text from images using local EasyOCR and Tesseract OCR workflows with documented preprocessing chains for screenshots, posters, documents, phone photos, and batch image folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jnbno1163](https://clawhub.ai/user/jnbno1163)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to run local OCR on image files and convert screenshots, posters, documents, phone photos, or folders of images into extracted text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and first-run OCR model behavior may vary because the artifact uses mutable dependency ranges and EasyOCR may download a local model on first use.

Mitigation: Install in a virtual environment and use pinned, reviewed dependency versions before deployment.

Risk: OCR inputs and outputs can contain sensitive screenshot, photo, document, or extracted text content.

Mitigation: Invoke the skill explicitly for sensitive files and handle generated text outputs with the same access controls as the source images.

Risk: The release security summary notes that some documentation overstates automatic engine selection and full preprocessing-chain behavior.

Mitigation: Test the selected engine and preprocessing mode on representative images, and use explicit engine or preprocessing options for critical extraction tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jnbno1163/skills/liaogong-ocr)
- [Benchmark Results](references/benchmark-results.md)
- [Preprocessing Guide](references/preprocessing-guide.md)
- [Project homepage](https://github.com/jnbno1163/liaogong-ocr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with extracted OCR text, inline shell commands, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extracted text to local output files when the CLI or batch script is invoked with an output path.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter and setup.py report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
