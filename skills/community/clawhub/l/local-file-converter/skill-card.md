## Description:

Converts local images, video, audio, documents, ebooks, and data files across many formats using common command-line conversion tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiantian-pago](https://clawhub.ai/user/tiantian-pago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and other agent users use this skill to identify source files, select an appropriate local converter, run the conversion, and return the converted file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk or overwrite-prone conversions can affect important local files or directories.

Mitigation: Run conversions on copies or backed-up directories and set an explicit OUTPUT_DIR for important work.

Risk: Large video or media conversions can consume significant CPU time and may produce lossy output.

Mitigation: Confirm the intended target format and quality settings before conversion, and run resource-heavy conversions when the machine is available.

Risk: The skill depends on locally installed converter tools such as ffmpeg, ImageMagick, LibreOffice, Pandoc, Calibre, and optionally dasel.

Mitigation: Install only the converters needed for the intended file types and review the generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tiantian-pago/skills/local-file-converter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown or text with shell commands, installation guidance, and local output file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates converted files locally, normally under a converted output directory unless OUTPUT_DIR is set.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
