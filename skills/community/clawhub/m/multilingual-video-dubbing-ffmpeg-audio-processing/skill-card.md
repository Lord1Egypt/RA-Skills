## Description: <br>
Extract, normalize, mix, convert, and analyze audio tracks for video and audio workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media engineers use this skill to draft FFmpeg and ffprobe commands for extracting, normalizing, mixing, converting, delaying, filtering, concatenating, and inspecting audio tracks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated FFmpeg commands may overwrite output files or target unintended local paths. <br>
Mitigation: Review output paths, concat list files, and command flags before running commands. <br>
Risk: Audio processing commands may select the wrong stream, codec, channel, or normalization settings for a specific media file. <br>
Mitigation: Inspect inputs with ffprobe and verify stream mappings, filters, and output quality on a sample before batch processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/multilingual-video-dubbing-ffmpeg-audio-processing) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be reviewed and adapted to local file paths, stream mappings, codecs, and overwrite behavior before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
