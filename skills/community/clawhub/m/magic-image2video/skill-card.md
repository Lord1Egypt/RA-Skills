## Description: <br>
Generate a video task from user-provided text and images, including image URLs or local file paths, and submit it to a remote video service using an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyuangao](https://clawhub.ai/user/zhangyuangao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create image-to-video generation tasks from a text prompt and an image URL or local image file. The skill guides task creation, polling, and user-facing reporting of the final video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided prompts, image URLs, and local image files to a remote video-generation service. <br>
Mitigation: Avoid confidential prompts, private local files, internal URLs, and sensitive images unless the user intentionally wants that content sent to the remote service. <br>
Risk: The skill requires a MAGIC_API_KEY for the remote service. <br>
Mitigation: Install and run the skill only when the Magiclight service is trusted with the API key and generated media inputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhangyuangao/magic-image2video) <br>
- [Publisher profile](https://clawhub.ai/user/zhangyuangao) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON stdout parsing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAGIC_API_KEY; reports a generated task ID and final video URL when the remote service completes successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
