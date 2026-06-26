## Description: <br>
妙音AI 音乐创作助手，生成歌曲、查询任务、续写音乐、生成歌词。当用户需要 AI 作曲或音乐生成时调用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phongf](https://clawhub.ai/user/phongf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create songs, continue music, generate lyrics, query music task status, and retrieve generated audio or video outputs through the 妙音AI REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends lyrics, prompts, song IDs, and music task data to the third-party ai.growingth.com service. <br>
Mitigation: Use the skill only when the user intends to share that content with the service, and avoid submitting private or sensitive lyrics or prompts. <br>
Risk: Music generation, video creation, WAV conversion, and stem separation may consume account quota. <br>
Mitigation: Request explicit user confirmation before quota-consuming actions and report API errors without inventing results. <br>
Risk: The skill requires an API token in MIAOYIN_API_TOKEN. <br>
Mitigation: Keep the token in the environment, redact it from logs, and do not validate or expose its raw value. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phongf/miaoyin-ai-music) <br>
- [Publisher profile](https://clawhub.ai/user/phongf) <br>
- [妙音AI API service](https://ai.growingth.com/api-service) <br>
- [妙音AI REST API base endpoint](https://ai.growingth.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Text, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown and text responses with JSON REST request details and returned music links or task status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MIAOYIN_API_TOKEN and sends prompts, lyrics, song IDs, and task data to ai.growingth.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
