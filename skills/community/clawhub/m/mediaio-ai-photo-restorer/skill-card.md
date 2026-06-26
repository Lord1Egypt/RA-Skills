## Description: <br>
Restore damaged, old, and low-quality photos through Media.io OpenAPI by enhancing image quality, reducing scratches and noise, and colorizing black-and-white images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user has an authorized, publicly reachable image URL and wants Media.io to restore, enhance, or colorize the photo. The skill is also useful for checking available Media.io credits before submitting asynchronous restoration jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input photos and generated preview URLs may include personal or sensitive content processed by Media.io. <br>
Mitigation: Only process images the user owns or is authorized to edit, and avoid highly sensitive photos unless Media.io processing and returned public preview URLs are acceptable. <br>
Risk: The skill requires a Media.io API key and can consume Media.io credits. <br>
Mitigation: Use a dedicated or revocable API key, avoid exposing it in logs or responses, and check available credits before starting generation. <br>


## Reference(s): <br>
- [Media.io API Documentation](https://platform.media.io/docs/) <br>
- [Media.io Developer Portal](https://developer.media.io/) <br>
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/mediaio-ai-photo-restorer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with cURL commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns asynchronous task IDs, polling guidance, status handling, and generated image preview URLs when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
