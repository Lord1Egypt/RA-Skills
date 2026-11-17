## Description:

Comprehensive novel writing assistant for creating, managing, continuing, formatting, and converting novel manuscripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External authors and writing agents use this skill to draft or continue chapters, maintain character and plot consistency, check chapter formatting, and compile Markdown chapters to TXT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read existing chapters and save manuscript or compiled text files in the project folder it is pointed at.

Mitigation: Run it only in intended manuscript workspaces and review file paths before allowing writes or conversions.

Risk: EPUB/PDF conversion is advertised, but the bundled scripts only provide Markdown-to-TXT conversion.

Mitigation: Use the bundled converter for TXT output only unless separate EPUB/PDF tooling is supplied and reviewed.

Risk: The format checker is tailored to Chinese-style chapter markers.

Mitigation: Confirm or adapt chapter naming and section conventions before relying on checker results for other manuscript formats.

## Reference(s):

- [Character Management Guide](references/characters.md)
- [Plot Management Guide](references/plot.md)
- [Novel Writing Style Guide](references/writing_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown manuscript drafts, plain-text compiled output, and concise guidance with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled scripts check Chinese-style chapter formatting and convert Markdown chapters to TXT; EPUB/PDF conversion is advertised but not provided by the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
