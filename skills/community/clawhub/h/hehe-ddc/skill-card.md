## Description: <br>
Generates Douyin/TikTok-style vertical marketing videos from images and captions, with TTS voiceover, line-by-line subtitles, random background music, and automatic duration fitting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghu66](https://clawhub.ai/user/wanghu66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketing operators use this skill to turn product images and Chinese promotional copy into short vertical MP4 videos with voiceover, subtitles, and background music. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online TTS can transmit caption text to an external service. <br>
Mitigation: Do not include confidential or regulated text in captions when using online TTS. <br>
Risk: Internet BGM downloads require network access during generation. <br>
Mitigation: Set audio.bgm.from_internet to false in config/default.json for offline or network-restricted use. <br>
Risk: Generated videos may be copied outside the skill workspace by default. <br>
Mitigation: Set output.copyToWindows to false when generated files should remain inside the skill workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanghu66/hehe-ddc) <br>
- [README](README.md) <br>
- [Usage guide](docs/USAGE.md) <br>
- [Installation guide](docs/INSTALL.md) <br>
- [Configuration template](config/config.template.json) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [MP4 video files with generated MP3 audio and SRT subtitles; Markdown guidance with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses image paths, captions, voice, duration, BGM, subtitle, and output-copy configuration] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
