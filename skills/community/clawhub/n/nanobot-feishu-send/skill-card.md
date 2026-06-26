## Description: <br>
Sends local images, files, audio, and video to Feishu through nanobot's message tool, with attachment upload and message type handling delegated to the Feishu channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinyuqinfeng](https://clawhub.ai/user/xinyuqinfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using nanobot with Feishu use this skill to send local media or file attachments to the current Feishu chat or a specified chat_id without manually calling Feishu APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may send a sensitive or unintended local file to Feishu. <br>
Mitigation: Verify the file path, file contents, and recipient or chat_id before sending attachments. <br>
Risk: Feishu credentials or nanobot configuration could be exposed if copied into chat or shared with others. <br>
Mitigation: Keep ~/.nanobot/config.json private and avoid sending secrets or personal data unless authorized. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Security Guide](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON examples] <br>
**Output Format:** [Markdown with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local file paths in the media field and an already configured nanobot Feishu channel.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
