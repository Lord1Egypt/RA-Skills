## Description:

Helps e-commerce, advertising, marketing, and product-visual teams turn product orbit video requests into Chinese production briefs, shot prompts, AI-HIVE video tasks, shell commands, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, product marketers, and visual-commerce teams use this skill to plan, generate, and check short product 360 orbit videos for e-commerce, ads, livestream commerce, and social media. It supports prompt writing, authorized media handling, model and price checks, AI-HIVE task submission, polling, downloads, and deterministic video inspection or aspect-ratio edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys and can upload private product media.

Mitigation: Use isolated environments, keep credentials out of logs and version control, protect ~/.ai-hive/config.json, and confirm media authorization before upload.

Risk: The API base URL can be overridden, which may route credentials or media to an untrusted endpoint.

Mitigation: Use the official AI-HIVE API URL unless the alternate endpoint is fully trusted, and avoid inheriting AI_HIVE_BASE_URL from untrusted environments.

Risk: Generated orbit videos may be mistaken for exact product scans or verified product claims.

Mitigation: Label uncertain facts for review, do not use generated output for dimensional or industrial verification, and require human approval before publishing product, price, efficacy, or endorsement claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-orbit-video-ai-hive)
- [AI-HIVE product entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls, files]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local blueprint JSON, submitted AI-HIVE task IDs, downloaded media files, and ffmpeg-edited video files when the user provides credentials and confirms generation parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
