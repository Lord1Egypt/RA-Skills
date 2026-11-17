## Description:

皮皮虾职场短剧全流程制作技能，用于生成职场短剧镜头视频、剪辑成片、配音配乐并发布到飞书群。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and agent users can use this skill to produce Pipixia workplace short-drama videos from image-to-video shots, normalize and edit clips, add TTS dialogue and background music, and send finished media to a Feishu chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because media filenames, temporary files, and credentials require review before installation.

Mitigation: Install only in a restricted workspace under a low-privilege account and review the helper scripts before use.

Risk: Feishu posting scripts can send video or audio messages to a chat when credentials and chat IDs are supplied.

Mitigation: Limit Feishu app credentials to the intended chat actions and require explicit operator confirmation before running send_video.sh or send_audio.sh.

Risk: Untrusted media paths may be unsafe until send_video.sh passes values as Python arguments instead of interpolating them into python3 -c.

Mitigation: Process only trusted media paths, or patch send_video.sh to pass arguments safely before accepting external inputs.

Risk: Shared temporary file paths can expose or collide with media processing artifacts.

Mitigation: Replace shared /tmp paths with mktemp-based private directories before using the skill in shared environments.

## Reference(s):

- [Pipixia Drama Production Reference](references/drama-reference.md)
- [ClawHub skill page](https://clawhub.ai/kylinr/skills/pipixia-drama-producer)
- [Kevin MacLeod music reference](https://incompetech.com)
- [Feishu auth API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu image upload API endpoint](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python, bash, ffmpeg, TTS, and Feishu API command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or send media files when the helper scripts are executed with local tools and Feishu credentials.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
