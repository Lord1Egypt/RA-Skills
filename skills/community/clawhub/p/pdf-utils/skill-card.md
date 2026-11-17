## Description:

PDF Utils enables OCR of image-based PDFs, extraction of arXiv IDs from text or OCR output, and scriptable PDF tasks like merging, splitting, and rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwllu](https://clawhub.ai/user/wangwllu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for local, repeatable PDF processing when they need OCR for scanned PDFs, arXiv reference extraction and download workflows, or scriptable merge, split, and page-render operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command bypasses Python package safety protections and uses unpinned dependencies.

Mitigation: Install in a virtual environment with pinned, audited dependencies, and avoid using --break-system-packages unless the environment owner explicitly accepts that tradeoff.

Risk: The arXiv download workflow contacts arXiv and writes downloaded PDFs to the chosen output directory.

Mitigation: Use --download only when network access and local file creation are acceptable, and choose an output directory that can be reviewed and cleaned.

Risk: PDFs from unknown sources are untrusted parser inputs.

Mitigation: Process untrusted PDFs in a constrained local environment and review outputs before relying on extracted text, references, or rendered images.

Risk: OCR and reference parsing can be incomplete for handwriting, low-resolution scans, very large PDFs, corrupt files, or unusual citation formats.

Mitigation: Process large PDFs in page ranges, inspect reference pages when results look partial, and treat OCR/reference extraction as a helper rather than a completeness guarantee.

## Reference(s):

- [PDF Utils Reference](references/usage.md)
- [ClawHub Skill Page](https://clawhub.ai/wangwllu/skills/pdf-utils)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and Python code snippets; executed scripts can produce PDFs, images, and text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local output files such as downloaded arXiv PDFs, OCR text, merged or split PDFs, and rendered page images.]

## Skill Version(s):

1.0.1 (source: server release evidence, pyproject.toml, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
