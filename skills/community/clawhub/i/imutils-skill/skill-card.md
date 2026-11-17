## Description:

Provides agent-facing commands and guidance for batch image rotation, resizing, translation, skeletonization, and image listing using imutils-based tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jumeng1997](https://clawhub.ai/user/jumeng1997)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operations teams can use this skill to prepare batches of images for ecommerce, social media, photography workflows, and dataset augmentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable wrappers build shell commands from unvalidated user input, creating arbitrary-command-execution risk.

Mitigation: Harden wrappers to avoid shell execution, validate numeric options, restrict input and output paths, and use disposable workspaces for any interim evaluation.

Risk: Image outputs may overwrite or modify local files if paths are chosen carelessly.

Mitigation: Use explicit output directories, keep backups of source images, and define non-overwrite behavior before batch processing.

Risk: Untrusted filenames or parameters can increase execution and file-system risk.

Mitigation: Process only trusted local files until validation and path restrictions are implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jumeng1997/skills/imutils-skill)
- [Publisher profile](https://clawhub.ai/user/jumeng1997)
- [PyImageSearch imutils](https://github.com/PyImageSearch/imutils)
- [imutils README](https://github.com/PyImageSearch/imutils#readme)
- [OpenCV documentation](https://docs.opencv.org/)
- [PyImageSearch](https://www.pyimagesearch.com/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with command examples and script-backed command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-processing guidance and command invocations for local image inputs and outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
