## Description: <br>
Generates Jimeng AI videos with audio through the Volcengine API, supporting text-to-video, image-to-video, multiple models, batching, task status checks, and result retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, operators, and developers use this skill to generate short AI videos with optional generated audio from text or image prompts through Volcengine/Jimeng. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, and generated content may be sent to the Volcengine/Jimeng cloud service. <br>
Mitigation: Avoid confidential, regulated, or sensitive content unless the user has approved that cloud processing path. <br>
Risk: Volcengine API keys are required and could be exposed or misused. <br>
Mitigation: Store credentials only in the configured credential file or secret store, restrict file access, and rotate keys if exposure is suspected. <br>
Risk: Broad or accidental use may consume paid Volcengine quota, especially with batch generation or higher-cost audio models. <br>
Mitigation: Confirm model choice, prompt count, and batch size before running large jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/jimeng-video-clawd) <br>
- [Volcengine content generation tasks API](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API request examples, task status responses, and MP4 video outputs or video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create paid Volcengine generation tasks; requires configured Volcengine access credentials.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, skill.yaml, _meta.json, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
