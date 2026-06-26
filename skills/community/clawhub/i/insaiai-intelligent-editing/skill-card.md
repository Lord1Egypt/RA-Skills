## Description: <br>
Use when performing video/audio processing tasks including transcoding, filtering, streaming, metadata manipulation, or complex filtergraph operations with FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liudu2326526](https://clawhub.ai/user/liudu2326526) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, video editors, and automation engineers use this skill to draft FFmpeg and FFprobe command-line guidance for transcoding, filtering, media inspection, metadata work, streaming, and complex filtergraphs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated FFmpeg or FFprobe commands can affect local files through incorrect paths, unexpected overwrite behavior, or unintended input/output selection. <br>
Mitigation: Review every input path, output path, stream mapping option, and overwrite flag before running a generated command; test on copies for destructive edits. <br>
Risk: Live-streaming commands can send media to a remote destination and may expose stream keys if secrets are pasted into commands or logs. <br>
Mitigation: Verify the destination URL, treat stream keys as secrets, avoid sharing commands that contain real keys, and prefer secure secret handling where available. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are guidance for review before execution; they may include local file paths, overwrite behavior, and network destinations supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
