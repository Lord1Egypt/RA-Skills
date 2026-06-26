## Description: <br>
Generates adult-only creative AI videos through Atlas Cloud video models, supporting text-to-video, image-to-video, video-to-video, model selection guidance, media upload, polling, and MP4 download workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Adult users, creators, and developers use this skill to generate mature creative video assets through Atlas Cloud models after confirming they are 18 or older. It is suited for legitimate adult artistic, fashion, choreography, animation, and professional media workflows that require text, image, or video conditioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for mature adult content and may be inappropriate or unlawful for underage users or restricted contexts. <br>
Mitigation: Require explicit 18+ confirmation before use and apply local policy, consent, and legal checks before generating content. <br>
Risk: Prompts, image URLs, audio URLs, video URLs, and uploaded files are sent to Atlas Cloud for processing. <br>
Mitigation: Use only consented, non-sensitive media and review Atlas Cloud handling terms before uploading personal or confidential content. <br>
Risk: The Atlas Cloud API key can incur paid generation or upload costs if misused. <br>
Mitigation: Use a dedicated ATLASCLOUD_API_KEY, keep it in environment variables, monitor account usage, and limit account balance exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihhhh/nsfw-video) <br>
- [Publisher profile](https://clawhub.ai/user/xixihhhh) <br>
- [Atlas Cloud](https://www.atlascloud.ai) <br>
- [Atlas Cloud video generation API endpoint](https://api.atlascloud.ai/api/v1/model/generateVideo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with command examples and generated MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY; prompts and media URLs are sent to Atlas Cloud; generated videos are downloaded to the selected local output directory.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
