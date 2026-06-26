## Description: <br>
Batch extracts audio from MP4 files in a selected folder and saves MP3 files while preserving the source folder structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill with OpenClaw agents to batch convert local MP4 video folders into MP3 audio, with optional source and output directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill automatically installs Python packages, changes packaging tools, downloads FFmpeg, writes logs, and generates MP3 files under the selected output path. <br>
Mitigation: Review before installing, run only in a disposable or dedicated environment, prefer preinstalling FFmpeg and dependencies yourself, and choose the output path deliberately. <br>
Risk: The documented URL-download workflow can bring unreviewed remote media into the conversion flow. <br>
Mitigation: Avoid URL downloads unless that workflow has been separately reviewed and explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wangminrui2022/mp4-to-mp3-extractor) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated MP3 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recursively processes .mp4 files and writes .mp3 outputs to the selected output directory while preserving relative paths.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
