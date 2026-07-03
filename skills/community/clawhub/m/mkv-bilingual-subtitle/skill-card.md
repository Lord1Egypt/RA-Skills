## Description: <br>
Merges Chinese and English text subtitles from MKV files into a bilingual subtitle track and embeds it back into the video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlalamoon](https://clawhub.ai/user/vlalamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and media-processing developers use this skill to generate bilingual Chinese-English subtitle tracks for MKV videos. It supports single-file and batch workflows when the required MKVToolNix utilities are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default workflow can overwrite original MKV files, including during batch processing. <br>
Mitigation: Run with --dry-run first, use --output to write to a separate file or directory, and keep backups of source media. <br>
Risk: A mistaken batch target or subtitle merge can permanently replace files with undesired output. <br>
Mitigation: Review the planned file list before batch execution and confirm the intended MKV range before processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlalamoon/mkv-bilingual-subtitle) <br>
- [Publisher profile](https://clawhub.ai/user/vlalamoon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for extracting, merging, and embedding SRT or ASS/SSA subtitles; the underlying script can write modified MKV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
