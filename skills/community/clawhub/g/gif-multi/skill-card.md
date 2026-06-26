## Description: <br>
Search and send GIF reactions on any messaging platform (Telegram, WhatsApp, Discord, Signal, etc). Auto-detects your enabled channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chdlc](https://clawhub.ai/user/chdlc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to find reaction GIFs, convert them for the active messaging channel, and send the resulting media in conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GIF search queries are sent to Giphy and the skill requires a GIPHY_API_KEY credential. <br>
Mitigation: Configure the API key deliberately and avoid using sensitive or private terms as GIF search queries. <br>
Risk: In natural mode, the agent may send GIF media spontaneously in conversations. <br>
Mitigation: Use on_request mode when GIFs should only be sent after an explicit user request. <br>
Risk: Generated media is stored locally for a short period and channel or mode preferences persist in the skill configuration. <br>
Mitigation: Review local storage expectations before deployment and rely on the skill's cleanup behavior for generated media after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chdlc/gif-multi) <br>
- [Giphy Developers](https://developers.giphy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON status objects with media file paths, plus Markdown and shell snippets for setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates GIF or MP4 media files in .gif_cache and stores channel and mode preferences in config.json.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
