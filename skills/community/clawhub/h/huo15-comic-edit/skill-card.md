## Description:

Huo15 Comic Edit helps an agent assemble ordered lipsync or video clips into a final MP4 with BGM mixing, generated subtitles, and FFmpeg-based encoding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and media-production agents use this skill to compose short comic-style video projects from prepared scene clips, dialogue audio, background music, and script metadata into final.mp4.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled cloud API helpers can transmit prompts, text, and selected local media to external services if invoked by another workflow.

Mitigation: Review, remove, or disable the shared Ark helper before installation when a strictly local FFmpeg-only tool is required, and do not set ARK_API_KEY unless that cloud behavior is intended.

Risk: The editing workflow writes derived media and subtitle files into the selected project directory.

Mitigation: Run the skill against a prepared project workspace and review generated files before reusing or publishing the final video.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-comic-edit)
- [VolcEngine Seedance documentation](https://www.volcengine.com/docs/82379/1520757)
- [VolcEngine TTS documentation](https://www.volcengine.com/docs/6561/97465)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated local files include final.mp4, subtitle.srt, concat.mp4, and concat.txt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a project directory with script.json, scene media, optional bgm.mp3, FFmpeg 5.0 or newer, and Source Han Serif SC for the documented subtitle style.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
