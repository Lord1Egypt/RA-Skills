## Description: <br>
Creates bilingual Chinese and English picture-book story videos from story scripts, including scene images, narration, subtitles, final MP4 files, and Douyin publishing copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and developers use this skill to turn a provided picture-book story script into Chinese and English video outputs with generated scenes, narration, subtitles, and posting metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can hand generated videos and posting copy to a Douyin publishing workflow without a clear final consent step. <br>
Mitigation: Require explicit manual confirmation before invoking any publishing skill or upload step, and review generated videos, titles, descriptions, and topics first. <br>
Risk: Story text may be processed by remote TTS when the Edge TTS fallback is used. <br>
Mitigation: Avoid sensitive or private story text when remote TTS fallback is enabled, or disable the fallback for sensitive projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/picture-book-video) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, generated file paths, and publishing copy] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local scripts to create bilingual MP4 files, narration audio, subtitle files, scene metadata, and Douyin publishing descriptions after user-confirmed story planning.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
