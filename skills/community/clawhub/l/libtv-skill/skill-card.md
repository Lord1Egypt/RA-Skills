## Description: <br>
LibTV API Skills helps an agent create LibTV sessions, send image and video generation or editing requests, monitor progress, upload reference media, switch projects, and download generated media results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haofanwang](https://clawhub.ai/user/haofanwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to route natural-language image and video creation or editing requests through LibTV, poll for completion, and retrieve generated media and project links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, API keys, and selected reference images or videos may be sent to LibTV. <br>
Mitigation: Use a dedicated LibTV key when possible and avoid sending sensitive prompts or media unless LibTV is approved for that data. <br>
Risk: Changing OPENAPI_IM_BASE or IM_BASE_URL can route requests to a non-default endpoint. <br>
Mitigation: Keep the API base URL at the default unless the replacement endpoint is trusted. <br>
Risk: Generated image and video results can be saved to local storage. <br>
Mitigation: Choose an appropriate output directory and review local access controls for downloaded media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haofanwang/libtv-skill) <br>
- [Publisher profile](https://clawhub.ai/user/haofanwang) <br>
- [LibTV OpenAPI endpoint](https://im.liblib.tv) <br>
- [LibTV project canvas URL pattern](https://www.liblib.tv/canvas?projectId=) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files, URLs] <br>
**Output Format:** [Markdown/plain text guidance plus JSON responses, local file paths, and LibTV media or project URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and LIBTV_ACCESS_KEY; may send prompts and selected image or video files to LibTV and save generated media locally.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
