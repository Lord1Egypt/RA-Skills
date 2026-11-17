## Description:

Happy Horse 视频生成 helps creators, marketing teams, e-commerce teams, and short-form story teams generate videos from text prompts and optional image, video, or audio references through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, e-commerce operators, and production teams use this skill to submit AI Hive video-generation jobs, attach reference media when needed, monitor task status, and download generated video assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the AI Hive bearer key with API requests, and the base URL can be configured.

Mitigation: Use the default AI Hive endpoint or another trusted endpoint only, and prefer a dedicated low-privilege API key.

Risk: Prompts and referenced image, video, or audio files may be uploaded to AI Hive for generation.

Mitigation: Avoid sensitive prompts or media unless the user is comfortable with that processing, and confirm rights or consent for commercial assets.

Risk: Video generation can incur account costs, and retries after local timeouts may duplicate already-submitted work.

Mitigation: Check runtime pricing and routing before large jobs, keep task IDs, query existing tasks after timeouts, and monitor account usage.

Risk: Generated media and API configuration are saved locally.

Mitigation: Keep the API key configuration file restricted, choose an appropriate output directory, and remove sensitive generated files when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/happy-horse)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples, JSON task/status responses, configuration snippets, and locally downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs are saved to the configured local output directory; task queries can return JSON without downloading media.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
