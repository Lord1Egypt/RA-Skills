## Description: <br>
Generate AI videos using Wan (v2.6) via Media.io OpenAPI, including text-to-video, image-to-video, and reference-to-video workflows with 1080p output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Media.io Wan video generation APIs for text-to-video, image-to-video, and reference-to-video tasks, then poll task results or check available credits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, reference inputs, and the Media.io API key are sent to Media.io when the skill invokes generation APIs. <br>
Mitigation: Use the skill only when Media.io processing is intended, avoid private or sensitive prompts and internal image URLs, and keep API keys scoped and rotated according to local policy. <br>
Risk: Video generation and polling can consume Media.io account credits or expose usage patterns. <br>
Mitigation: Check credits before generation, monitor account usage, and limit agent access to approved workflows. <br>


## Reference(s): <br>
- [Media.io OpenAPI Documentation](https://platform.media.io/docs/) <br>
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/mediaio-wan-video-generator) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Guidance] <br>
**Output Format:** [JSON API responses and Markdown usage guidance with Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key through API_KEY or an explicit api_key argument; generation APIs return task_id values that should be polled with Task Result.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
