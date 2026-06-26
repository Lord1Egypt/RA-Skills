## Description: <br>
Generates AI videos with Volcengine Ark Seedance 2.0 models from text prompts and optional image, video, or audio references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jancong](https://clawhub.ai/user/jancong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and external users use this skill to submit Seedance video generation tasks, poll task status, and retrieve generated video outputs through the Volcengine Ark API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials are required to submit, query, and download video generation results. <br>
Mitigation: Use a scoped or quota-limited ARK_API_KEY and avoid exposing it in prompts, logs, or shared shell history. <br>
Risk: Prompts and reference media are sent to the Volcengine Ark/Seedance provider endpoint. <br>
Mitigation: Do not submit sensitive prompts or private media unless the user accepts that external processing. <br>
Risk: Generated videos and cover images may be downloaded to local output directories. <br>
Mitigation: Review output paths and access permissions before storing or sharing generated media. <br>
Risk: Changing ARK_API_URL can redirect requests to an untrusted endpoint. <br>
Mitigation: Keep ARK_API_URL at the trusted provider default unless there is a deliberate, reviewed reason to change it. <br>


## Reference(s): <br>
- [Seedance 2.0 API Reference](references/api_reference.md) <br>
- [Seedance 2.0 Prompt Guide](references/prompt_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jancong/jancong-seedance-video-gen) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/jancong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API payloads, task IDs, status summaries, generated video URLs, and local output file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
