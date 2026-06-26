## Description: <br>
Transforms photos and images into Studio Ghibli-style artwork using Media.io OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan Media.io API calls that convert user-authorized image URLs into Ghibli-style edited image previews, including credit checks, task polling, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs and generated previews are handled by Media.io, a third-party service. <br>
Mitigation: Use only user-authorized images, avoid sensitive or private images unless the service and URL host are trusted, and treat generated preview URLs as potentially public. <br>
Risk: The skill requires a Media.io API key for requests. <br>
Mitigation: Use a dedicated MEDIAIO_API_KEY where possible and avoid logging or returning raw API keys. <br>


## Reference(s): <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with JSON request and response examples and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY and a Media.io-reachable image URL; generated preview URLs may be publicly accessible.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
