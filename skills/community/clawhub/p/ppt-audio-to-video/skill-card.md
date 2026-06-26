## Description: <br>
Convert narration audio plus slide decks into a narrated video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzfxxx](https://clawhub.ai/user/lzfxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content producers use this skill to combine narration audio with slide decks, generate slide outlines and timing plans, and render a slide-based MP4 lecture video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated transcripts, slide outlines, timing CSVs, and rendered videos may contain private presentation content. <br>
Mitigation: Use a dedicated local working directory and treat generated working files as private artifacts. <br>
Risk: External dependencies and model downloads are required for transcription and media rendering. <br>
Mitigation: Verify package and model provenance when integrity matters before running the workflow. <br>
Risk: Rendering can overwrite existing output files when overwrite mode is used. <br>
Mitigation: Choose output paths carefully or run the render script with --no-overwrite. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lzfxxx/ppt-audio-to-video) <br>
- [whisper.cpp small multilingual model](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, CSV schemas, and generated working files such as transcripts, slide outlines, timing CSVs, ffconcat files, and MP4 video output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local media workflow; outputs may include private transcripts, slide outlines, timing plans, and rendered video files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
