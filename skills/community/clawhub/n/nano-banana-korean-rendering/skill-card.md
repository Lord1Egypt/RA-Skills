## Description:

Generates images with accurately rendered Korean and other non-Latin text by prerendering text with Canvas and using Gemini for prompt analysis and image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wonyoung-huh](https://clawhub.ai/user/wonyoung-huh)

### License/Terms of Use:


## Use Case:

Developers and image-generation users use this skill to create posters, banners, logos, and other generated images that need legible Korean, Japanese, Chinese, Thai, Arabic, Devanagari, Cyrillic, or other non-Latin text. It detects text that needs prerendering, extracts the intended text and style, renders a PNG with local fonts, and can send the rendered text image to Gemini for final image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, rendered text images, and user-provided reference images may be sent to Google Gemini during analysis or final image generation.

Mitigation: Use the skill only with content approved for Gemini processing, avoid unnecessary sensitive reference images, and configure GEMINI_API_KEY in an environment intended for this workflow.

Risk: Setup installs npm dependencies and may download font files from external sources, which can affect reproducibility and supply-chain review.

Mitigation: Run setup in a minimal environment without unrelated secrets, and review or pin dependencies and downloaded fonts when reproducible builds are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wonyoung-huh/skills/nano-banana-korean-rendering)
- [ClawHub publisher profile](https://clawhub.ai/user/wonyoung-huh)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, image files, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON command responses, and PNG image outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js dependencies, local font assets, and GEMINI_API_KEY for Gemini-backed analysis and image generation; render-only mode can produce a prerendered PNG without final Gemini image generation.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact package.json: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
