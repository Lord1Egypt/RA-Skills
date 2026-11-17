## Description:

A document conversion skill that helps agents convert and inspect Markdown, HTML, LaTeX, Docx, and PDF files through a WebAssembly-based converter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyoung](https://clawhub.ai/user/guyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document authors, and agents use this skill to convert documents among supported formats and to run document statistics or validation tasks in a sandboxed working directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an external WebAssembly file that may change outside the skill artifact.

Mitigation: Install only from a trusted source and verify the WASM component before running document conversions.

Risk: The WASM component needs access to a host working directory containing the files to convert.

Mitigation: Use a dedicated temporary directory containing only intended input files, avoid granting home or project roots, and review output paths before execution.

## Reference(s):

- [Pandoc Rs Usage Guide](references/USAGE.md)
- [Pandoc WASM component](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/pandoc-rs/files/pandoc-component.wasm)
- [ClawHub skill page](https://clawhub.ai/guyoung/skills/pandoc-rs)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and file-format guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create converted document files in the selected working directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
