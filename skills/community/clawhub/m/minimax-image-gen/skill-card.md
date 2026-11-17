## Description:

Generates images with the MiniMax Image API from text prompts, style presets, aspect-ratio options, and optional local preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluestar-34](https://clawhub.ai/user/bluestar-34)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate PNG images from prompts through the MiniMax Image API, with built-in presets for common visual styles and command-line controls for model, count, aspect ratio, output directory, and preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a MiniMax API key and sends prompts to an external image-generation API.

Mitigation: Use a restricted MiniMax API key, rotate it regularly, and avoid confidential or sensitive prompts.

Risk: Security evidence reports insecure TLS handling and weak validation of downloaded image URLs.

Mitigation: Prefer a fixed version that preserves normal TLS certificate validation and validates downloaded image URL scheme, response type, and size before saving.

Risk: The optional preview mode opens generated files in local viewer applications.

Mitigation: Use preview only for trusted outputs, or leave --preview disabled and inspect saved files through normal review workflows.

## Reference(s):

- [MiniMax Image Generation API Reference](https://platform.minimaxi.com/docs/api-reference/image-generation-t2i)
- [MiniMax API Key Management](https://platform.minimaxi.com/user-center/interface-key)
- [ClawHub Skill Page](https://clawhub.ai/bluestar-34/skills/minimax-image-gen)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with command-line examples and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and MINIMAX_API_KEY; generated images are saved to the configured output directory.]

## Skill Version(s):

1.1.0 (source: server release evidence, artifact changelog, script __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
