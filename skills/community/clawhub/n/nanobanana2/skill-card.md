## Description:

Generate/edit images with nanobanana2 (Gemini 3.1 Flash Image preview). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 512/1K/2K/4K; aspect ratios; use --input-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zealman2025](https://clawhub.ai/user/zealman2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create or edit PNG images through Google's Gemini image API from natural-language prompts, including text-to-image and image-to-image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Gemini API key and allows passing it as a command-line argument, which can expose credentials in chat, shell history, or process listings.

Mitigation: Prefer setting GEMINI_API_KEY in a protected environment and avoid pasting API keys in chat or using --api-key unless necessary.

Risk: The local Python script contacts Google's Gemini image API and writes files in the user's working directory.

Mitigation: Install only when external API use is acceptable, run from an intended working directory, and consider a restricted environment for execution.

Risk: Dependencies are declared with lower bounds and may resolve to newer package versions over time.

Mitigation: Consider pinning dependencies before deployment in controlled or sensitive environments.

## Reference(s):

- [Google Gemini API image generation documentation](https://ai.google.dev/gemini-api/docs/image-generation?hl=zh-cn)
- [ClawHub skill page](https://clawhub.ai/zealman2025/skills/nanobanana2)
- [ClawHub publisher profile](https://clawhub.ai/user/zealman2025)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated or edited PNG images are saved to the user's working directory or specified output path; generated images include SynthID watermarking per the skill documentation.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
