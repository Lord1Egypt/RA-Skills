## Description:

Generate or edit images with Gemini 3.1 Flash Image Preview (Nano Banana 2) through a direct API call, supporting text-to-image, image-to-image, and 1K, 2K, or 4K outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to have an agent generate new PNG images or edit existing images with Google's Gemini image API. It is suited for iterative image creation workflows that need explicit output filenames, input-image edits, and selectable 1K, 2K, or 4K resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and any input images are sent to Google's Gemini API.

Mitigation: Avoid sending confidential, regulated, or otherwise sensitive content unless that use is permitted by the user's policies and Google API terms.

Risk: The skill requires a Gemini API key and can accept the key as a command-line argument.

Mitigation: Prefer GEMINI_API_KEY from the environment, avoid pasting keys into chat or shell history, and rotate any key that may have been exposed.

Risk: The script saves to a user-provided filename and may create directories or overwrite an existing image.

Mitigation: Use a dedicated output directory and unique timestamped filenames, and review the output path before execution.

Risk: Python dependencies are installed or resolved from the package registry at install or run time.

Mitigation: Install in an isolated environment and pin or lock dependencies when organizational policy requires reproducible builds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/skills/nano-banana-2-direct)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and PNG image files saved by the script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; accepts prompt, filename, optional input image, optional API key, and 1K, 2K, or 4K resolution.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
