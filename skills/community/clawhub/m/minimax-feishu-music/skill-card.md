## Description:

Generate music using MiniMax music-2.6 or music-cover API and send as Feishu audio attachment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydoomed](https://clawhub.ai/user/raydoomed)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate original or cover-style music from prompts and lyrics, save the result as an MP3, and send it to a Feishu recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw cover file paths can cause unintended local files to be uploaded as reference audio.

Mitigation: Use only cover files from a dedicated audio folder and validate the selected path before running the helper script.

Risk: Unsanitized output titles can overwrite or create files in unintended workspace locations.

Mitigation: Sanitize output filenames and review the target title before routine use.

Risk: The skill sends generated audio to a Feishu recipient, so an incorrect recipient ID can disclose content to the wrong user.

Mitigation: Confirm the Feishu open_id and recipient context before sending generated audio.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raydoomed/skills/minimax-feishu-music)
- [MiniMax Music Generation API Endpoint](https://api.minimaxi.com/v1/music_generation)
- [Feishu Tenant Access Token API Endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown instructions with bash commands and MP3 file output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an MP3 audio file and sends it as a Feishu file attachment when valid MiniMax and Feishu credentials are configured.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
