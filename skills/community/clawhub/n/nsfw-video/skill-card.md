## Description:

Generates adult (18+) creative AI videos through Atlas Cloud models, supporting text-to-video, image-to-video, video-to-video, media upload, polling, and downloaded MP4 outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

External adult users and developers use this skill to choose Atlas Cloud video models, prepare prompts or source media, generate mature creative videos, poll job status, and save returned video files. It is intended only for lawful adult creative work with rights and consent for any uploaded media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill generates mature adult video content.

Mitigation: Confirm users are 18 or older before use and refuse execution when age confirmation is not provided.

Risk: Prompts, image URLs, audio URLs, video URLs, and uploaded media are sent to Atlas Cloud.

Mitigation: Use only media the user has rights and consent to process, and tell users that submitted prompts and media are visible to Atlas Cloud.

Risk: The Atlas Cloud API key can incur pay-as-you-go charges and is not described as scope-limited.

Mitigation: Use a dedicated API key, keep the account balance limited, monitor usage, and revoke the key when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/nsfw-video)
- [Atlas Cloud](https://www.atlascloud.ai)
- [Atlas Cloud video generation API endpoint](https://api.atlascloud.ai/api/v1/model/generateVideo)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with bash commands, JSON payload examples, Python CLI usage, and local MP4 file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY; prompts and media are sent to Atlas Cloud, and generated videos are downloaded locally when the script is run.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
