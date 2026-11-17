## Description:

Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guogithubname](https://clawhub.ai/user/guogithubname)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate new images or edit existing images through Google's Gemini image API from natural-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images are sent to Google's API.

Mitigation: Use the skill only with prompts and images that are appropriate to share with Google.

Risk: The skill can accept a Gemini API key as a command-line argument.

Mitigation: Prefer GEMINI_API_KEY from the environment and avoid putting secrets in chat or shell history.

Risk: Dependencies are declared with open version ranges.

Mitigation: Pin or lock dependencies before running the helper script in a trusted environment.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/guogithubname/skills/nano-banana-pro-1-0-1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and saved PNG image files from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved to the current working directory or to the path supplied as the filename.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
