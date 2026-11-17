## Description:

Generate images using MiniMax API (image-01 model). Automatically optimizes prompts for better results. Use when user asks to generate images, create pictures, or draw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilmrmeeseeks](https://clawhub.ai/user/lilmrmeeseeks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a 16:9 image from a Chinese or English prompt through the MiniMax image-01 API. The skill rewrites the user's prompt with concise English image-generation terms before making the API request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send an AIMLAPI credential to the MiniMax endpoint.

Mitigation: Configure only a MiniMax-specific API key for this skill and avoid AIMLAPI_API_KEY until provider-specific credential routing is fixed.

Risk: User prompts are sent to MiniMax and written to runtime logs in plaintext.

Mitigation: Do not include sensitive or confidential details in prompts; prefer a version that removes plaintext prompt logging.

Risk: Security evidence marks this release as suspicious.

Mitigation: Review and scan the skill before installation or deployment, and refresh dependencies from a trusted registry when maintaining a fork.

## Reference(s):

- [MiniMax image generation endpoint](https://api.minimaxi.com/v1/image_generation)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown text with an image attachment URL when generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns status text for missing input, missing credentials, API errors, or image-generation failures.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
