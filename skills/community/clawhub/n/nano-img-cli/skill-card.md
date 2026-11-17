## Description:

Drives the local nano-img Gemini image CLI for image generation, model selection, saved defaults, reference-image workflows, and output sizing or format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dishant0406](https://clawhub.ai/user/dishant0406)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate the local nano-img or nano-image CLI, generate Gemini images, inspect or update saved defaults, manage reference assets, and troubleshoot local generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run the local CLI and change persistent nano-img defaults, including model, save directory, style files, instructions, or reference assets.

Mitigation: Use the documented nano-img commands for changes, inspect `nano-img config --json` or `nano-img refs --json` before and after changes, and report the exact resulting model, output directory, or generated path.

Risk: Image generation can fail or produce no output when credentials, quota, model selection, references, or output directories are invalid.

Mitigation: Verify `NANO_IMAGE_API_KEY`, inspect the saved configuration, check readable references and writable output paths, and validate with one concrete CLI command.

## Reference(s):

- [Command Reference](references/command-reference.md)
- [Defaults And Files](references/defaults-and-files.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact saved model, output directory, generated file path, or JSON-inspection command results when relevant.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
