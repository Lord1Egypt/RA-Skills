## Description: <br>
Pipixia Drama Producer helps agents create workplace short dramas for the Pipixia lobster AI bot by generating image-to-video shots, normalizing and editing clips, adding TTS voice and BGM, and sending media to Feishu groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylinr](https://clawhub.ai/user/kylinr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creative operators, and employees use this skill to produce short workplace drama videos, including clip generation, ffmpeg-based trimming and editing, TTS voiceover, background music mixing, and Feishu delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post media to Feishu groups. <br>
Mitigation: Use a least-privilege Feishu app, keep credentials in environment variables, and verify the target chat_id and media files before sending. <br>
Risk: The security summary reports an unsafe script pattern that could run unintended local code with crafted inputs. <br>
Mitigation: Use the skill only in a trusted workspace and avoid or patch send_video.sh when handling untrusted filenames or FFPROBE values. <br>


## Reference(s): <br>
- [Pipixia Drama Production Reference](references/drama-reference.md) <br>
- [ClawHub release page](https://clawhub.ai/kylinr/pipixia-drama-producer) <br>
- [Incompetech royalty-free music source](https://incompetech.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify video and audio files and may send media to Feishu when provided valid credentials and target chat IDs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
