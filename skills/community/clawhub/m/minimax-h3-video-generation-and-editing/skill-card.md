## Description:

Minimax H3 Video Generation and Editing helps creators, editors, post-production teams, advertisers, and ecommerce teams generate videos from text or guide video generation with images, video, audio, first frames, and last frames through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, advertising producers, and ecommerce operators use this skill to submit Minimax H3 video-generation jobs, upload reference media, monitor task status, and download generated assets for ads, product videos, TVC, social commerce, short drama, comic drama, and social media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom AI Hive base URL can receive the user's API key.

Mitigation: Use the official AI Hive endpoint unless the alternate server is fully trusted, and avoid setting AI_HIVE_BASE_URL from untrusted instructions.

Risk: Video, image, or audio reference files are uploaded to AI Hive or its object-storage upload endpoint.

Mitigation: Upload only media that is intended for the generation provider and appropriate for that service.

Risk: Video generation jobs can incur cost, especially in repeated or batch workflows.

Mitigation: Prefer a dedicated API key with limited balance or quota, review live pricing before large jobs, and use no-download task submission when separating submission from polling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/minimax-h3-video-generation-and-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key and chat portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON task responses, uploaded media IDs, task status, and downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is downloaded to the configured output directory by default; no-download mode returns task JSON for later polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
