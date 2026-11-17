## Description:

ModelCLI lets agents run local ModelCLI workflows for object detection, OCR, speech recognition, speech synthesis, model management, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[graysilver](https://clawhub.ai/user/graysilver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ModelCLI to route local image and audio requests through a structured wrapper for detection, OCR, transcription, speech synthesis, model management, and diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On a machine without ModelCLI, ordinary use may download and execute an unpinned remote installer.

Mitigation: Install ModelCLI manually from a trusted, pinned source before enabling the skill, and avoid relying on automatic installation.

Risk: Normal invocations allow model downloads and may create persistent local models or generated output files.

Mitigation: Review network and local storage expectations before use, and keep explicit confirmation for overwrites, model refresh or removal, and deep diagnostics.

## Reference(s):

- [ModelCLI command reference](references/commands.md)
- [Agent JSON protocol and error handling](references/protocol.md)
- [Server-resolved GitHub provenance](https://github.com/GraySilver/modelcli/tree/main/skills/modelcli)
- [ClawHub skill page](https://clawhub.ai/graysilver/skills/modelcli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown summaries with shell commands, parsed JSON results, and local file paths when outputs are generated]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report absolute paths to generated speech audio, OCR text, annotated images, or other local output files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
