## Description:

Nano Banana 2 营销图片 helps agents plan and generate AI Hive Nano Banana 2 marketing images across awareness, explanation, conversion, and retention assets while keeping brand visuals consistent across web, email, social, sales, and event channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, content operators, and agents use this skill to structure campaign image work by funnel stage and run fixed-model Nano Banana 2 image generation through AI Hive. It supports text-only prompts and user-approved reference images for website banners, email headers, sales presentation backgrounds, event assets, and retention content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an AI Hive API key locally.

Mitigation: Use a virtual environment, keep the API key in a protected environment variable or the local config file, and rotate the key if it is exposed.

Risk: Reference images are uploaded to AI Hive when supplied for generation.

Mitigation: Provide only authorized reference images that are acceptable to upload to the AI Hive service.

Risk: Generated marketing assets can imply unsupported product claims, customer facts, environmental claims, or performance data.

Mitigation: Require written approval and evidence for customer names, case data, environmental claims, and performance claims; label concept imagery clearly.

Risk: Generated media is downloaded to the user's Downloads folder by default.

Mitigation: Review and manage files in ~/Downloads/AiHive, or use --no-download when only task metadata is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-marketing-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples; CLI output may include JSON task data and downloaded generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key from AI_HIVE_API_KEY, a CLI argument, or local config; generated media downloads to ~/Downloads/AiHive by default.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-08-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
