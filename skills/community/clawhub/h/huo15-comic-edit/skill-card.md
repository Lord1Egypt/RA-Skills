## Description: <br>
Uses FFmpeg to concatenate lipsync comic video scenes, mix background music, burn subtitles, apply short fades, and write final.mp4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and developers use this skill to assemble pre-generated comic video scenes into a finished video with subtitles and optional background music. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes cloud AI helper code that can use ARK_API_KEY and send prompts or media to external services if invoked. <br>
Mitigation: Use the documented edit.py workflow for local FFmpeg editing and leave ARK_API_KEY unset unless external cloud helpers are intentionally needed. <br>
Risk: The FFmpeg editor reads and writes media files inside the selected project directory. <br>
Mitigation: Run the command only against intended project directories and review generated media and subtitles before distribution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaobod1/huo15-comic-edit) <br>
- [Volcengine Seedance documentation](https://www.volcengine.com/docs/82379/1520757) <br>
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/97465) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; execution writes local media and subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented workflow writes final.mp4 under the selected project directory and may also create concat.mp4, concat.txt, and subtitle.srt.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
