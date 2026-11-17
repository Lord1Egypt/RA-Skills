## Description:

Generates vertical Douyin/TikTok-style marketing videos from images and copy, adding Chinese TTS narration, line-by-line subtitles, optional random BGM, and adaptive duration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghu66](https://clawhub.ai/user/wanghu66)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn product images and Chinese marketing copy into short vertical MP4 videos with narration, subtitles, and background music for Douyin/TikTok-style publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls external TTS and BGM services and may download audio from the internet.

Mitigation: Use a virtual environment with pinned dependencies, run only where those network calls are approved, and disable internet BGM when external downloads are not needed.

Risk: The default configuration may copy generated videos to a mounted Windows directory and uses weak output-path controls.

Mitigation: Restrict output names to simple .mp4 filenames inside the skill output folder, review windowsPath before running, or set copyToWindows to false.

Risk: Generated promotional copy can include sensitive details when supplied by the user.

Mitigation: Provide prices, contact details, addresses, and promotions explicitly only when they are approved for publication, and review the final video before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanghu66/skills/hehe-ddc)
- [Publisher profile](https://clawhub.ai/user/wanghu66)
- [Skill documentation](SKILL.md)
- [Usage guide](docs/USAGE.md)
- [Install guide](docs/INSTALL.md)
- [Baidu TTS endpoint](https://fanyi.baidu.com/tts)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [MP4 video, MP3 audio, SRT subtitles, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to the skill output folder; the generated MP4 may also be copied to a configured Windows-mounted directory when enabled.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and clawhub.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
