## Description: <br>
Generates instrumental music, songs with lyrics, and standalone lyrics through the MiniMax Music 2.5 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rexdong1](https://clawhub.ai/user/rexdong1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and agents use this skill to generate instrumental tracks, lyric-based songs, or standalone lyrics from style and theme prompts, with optional local download and Feishu sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and lyrics are sent to MiniMax using the user's API key, which can expose private or unpublished material to a remote service. <br>
Mitigation: Avoid submitting sensitive material unless MiniMax's terms and data handling meet the user's requirements. <br>
Risk: Generated audio can be shared through Feishu if the user chooses that workflow, which may expose files to unintended recipients or scopes. <br>
Mitigation: Verify the recipient, token scope, and audio content before uploading or sending generated files through Feishu. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rexdong1/minimax-music) <br>
- [Publisher profile](https://clawhub.ai/user/rexdong1) <br>
- [MiniMax API endpoint](https://api.minimaxi.com/v1) <br>
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, generated lyrics text, optional JSON metadata, and downloaded audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; generated audio URLs should be downloaded promptly because they may expire.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
