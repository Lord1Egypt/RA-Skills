## Description:

Generate instrumental music, songs with lyrics, and lyrics from prompts using the MiniMax Music 2.5 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rexdong1](https://clawhub.ai/user/rexdong1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate music or lyrics from prompts, download generated audio, and optionally share audio through Feishu after generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, and generated audio are sent to MiniMax, and may be sent to Feishu when sharing is used.

Mitigation: Avoid sensitive or proprietary prompts and lyrics, and use Feishu sharing only after confirming the recipient and token scope.

Risk: Passing credentials with command-line arguments can expose the MiniMax API key in shell history or process listings.

Mitigation: Prefer the MINIMAX_API_KEY environment variable instead of --api-key.

Risk: Generated audio URLs and downloaded files may expose user-created content if shared or stored in unintended locations.

Mitigation: Download only to intended directories and treat generated audio URLs and files as sensitive user content.

## Reference(s):

- [MiniMax API endpoint](https://api.minimaxi.com/v1)
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with CLI commands; generated lyrics text, audio files, or JSON metadata when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can download MP3, WAV, or FLAC audio and can emit JSON metadata with audio URL and generation details.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
