## Description: <br>
Jimeng Video helps agents generate text-to-video and image-to-video content with optional AI-generated audio through the Volcengine/Dreamina API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content operators, and developers use this skill to generate short videos with optional AI-generated sound, manage generation tasks, and retrieve remote generation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded images, videos, audio, and generated outputs may be sent to Volcengine/Seedance for remote processing. <br>
Mitigation: Use only with organization-approved data and avoid secrets, private personal data, or confidential business assets unless that remote processing is approved. <br>
Risk: The skill requires Volcengine API credentials to create and query generation tasks. <br>
Mitigation: Store credentials in the documented credentials file or secret manager, avoid pasting keys into prompts or shared logs, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/jimeng-video-v1) <br>
- [Volcengine Ark content generation tasks API](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, API calls, files] <br>
**Output Format:** [Markdown with inline bash commands, curl examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or retrieve MP4 video files from remote task URLs when run with Volcengine credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
