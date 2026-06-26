## Description: <br>
Compresses and converts image and video files with ffmpeg for file-size reduction, format conversion, resizing, and media optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1987566643](https://clawhub.ai/user/1987566643) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare images and videos for websites, email, social platforms, archiving, and storage-constrained workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chosen output files may be accidentally overwritten during compression or conversion. <br>
Mitigation: Use preview mode first, write results to a separate output folder, and enable the backup option when preserving originals matters. <br>
Risk: Using an untrusted ffmpeg installation can introduce avoidable local execution risk. <br>
Mitigation: Install ffmpeg only from trusted package managers or the official ffmpeg download source. <br>


## Reference(s): <br>
- [FFmpeg Guide](references/ffmpeg_guide.md) <br>
- [FFmpeg Download](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and local output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local ffmpeg-based scripts that can create compressed or converted media files at user-selected output paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
