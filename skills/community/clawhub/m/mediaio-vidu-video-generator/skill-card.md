## Description: <br>
Generate AI videos from text prompts or image URLs using Vidu through the Media.io OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check Media.io credits, submit Vidu text-to-video or image-to-video generation jobs, and poll for generated video task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and the API key are sent to Media.io, and generation requests may consume account credits. <br>
Mitigation: Use a revocable Media.io API key, monitor credit usage, and submit only public, non-sensitive prompts and image URLs. <br>
Risk: Image-to-video workflows require externally reachable image URLs. <br>
Mitigation: Use public assets intended for upload to Media.io rather than private, internal, or sensitive URLs. <br>


## Reference(s): <br>
- [Media.io OpenAPI Documentation](https://platform.media.io/docs/) <br>
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/mediaio-vidu-video-generator) <br>
- [API definitions](artifact/scripts/c_api_doc_detail.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Configuration, Guidance] <br>
**Output Format:** [JSON API responses with Python invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key and returns task IDs for generation APIs that must be polled with Task Result.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
