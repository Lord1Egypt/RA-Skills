## Description:

Generates livestream commerce visual assets with Nano Banana 2 through AI Hive, including backgrounds, product explanation cards, benefit panels, countdown placeholders, and fallback static screens optimized for mobile readability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, merchants, and developers use this skill to generate reusable visual containers for livestream selling workflows while leaving prices, inventory, discounts, countdowns, and QR codes to be confirmed and overlaid at broadcast time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reference images may be sent to AI Hive service and related storage endpoints.

Mitigation: Use only images approved for upload to the third-party service and avoid sensitive or confidential reference material.

Risk: Remote API responses can influence upload and download destinations and local output filenames broadly.

Mitigation: Run the skill in a virtual environment, avoid sensitive internal networks, and choose a dedicated output folder before downloading results.

Risk: The AI Hive API key is a credential stored locally or passed through the environment or command line.

Mitigation: Treat the API key as secret, restrict local config file permissions, and rotate the key if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/livestream-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands that submit image-generation tasks and download generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the fixed public_model_nano_banana_2 image model, optional user-provided reference images, an AI_HIVE_API_KEY credential, and a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
