## Description:

Nanobanana Pro helps agents generate, edit, and compose images through the Gemini Image API with automatic model fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yazelin](https://clawhub.ai/user/yazelin)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to produce new images, edit one image, or compose up to 14 input images while letting the script try a configured Gemini model fallback chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to Google's Gemini API for external processing.

Mitigation: Use only data approved for external processing, avoid confidential or regulated images unless authorized, and disclose this dependency to users.

Risk: Gemini API keys may be exposed if passed directly on the command line or stored insecurely.

Mitigation: Set GEMINI_API_KEY in the environment or approved agent configuration rather than passing keys as command arguments.

Risk: Unpinned dependency ranges can reduce repeatability across installs.

Mitigation: Review dependencies before deployment and consider pinning versions or using a lockfile for controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yazelin/skills/nanobanana-pro-fallback)
- [yazelin publisher profile](https://clawhub.ai/user/yazelin)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and saved image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit a MEDIA line pointing to the generated PNG file for supported OpenClaw chat providers.]

## Skill Version(s):

0.4.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
