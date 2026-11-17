## Description:

商品图转UGC带货视频｜AI-HIVE helps ecommerce and cross-border sellers turn authorized product images and verified selling points into UGC-style video plans, scripts, image and video generation prompts, AI-HIVE commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce marketers, merchants, cross-border sellers, and agent operators use this skill to plan and produce UGC-style promotional videos from product images. It turns product facts, audience, platform, duration, and tone into a reviewable workflow, runnable AI-HIVE media-generation commands, content drafts, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an AI-HIVE API key locally.

Mitigation: Use a limited API key, keep it out of prompts, logs, screenshots, and repositories, and review local configuration before use.

Risk: A custom AI_HIVE_BASE_URL or base-url value could send the API key to an arbitrary endpoint.

Mitigation: Use the default AI-HIVE endpoint unless you control and trust the endpoint, and reject untrusted base URL changes.

Risk: Uploaded product or reference media is sent to the external AI-HIVE service.

Mitigation: Upload only media that the user is authorized to use and that is appropriate for external processing.

Risk: Generated promotional content could make unsupported product claims or imitate protected content.

Mitigation: Review outputs against product facts, rights, platform rules, and human approval requirements before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-image-to-ugc-video-ai-hive)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON blueprints and inline bash or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local blueprint JSON, downloaded media files, task status records, and edited video files when the user runs the generated commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
