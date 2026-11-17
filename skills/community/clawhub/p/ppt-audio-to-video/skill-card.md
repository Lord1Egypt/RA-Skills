## Description:

Convert narration audio plus slide decks into a narrated video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzfxxx](https://clawhub.ai/user/lzfxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media production engineers use this skill to rebuild a slide-based lecture video from narration audio and a presentation deck by extracting slide text, planning slide timings, and rendering an MP4.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs local media tools, may install optional dependencies, and may download a transcription model.

Mitigation: Review commands before execution, install dependencies intentionally, and run the workflow in a trusted local workspace.

Risk: Untrusted slide decks, image directories, filenames, or generated CSV files can create local file-handling or spreadsheet-safety concerns.

Mitigation: Use trusted media inputs, avoid attacker-controlled paths or filenames, and sanitize CSV files before opening them in spreadsheet software.

Risk: ASR and timing alignment can place slide boundaries incorrectly.

Mitigation: Review the transcript, slide outline, and timing CSV, then iterate on uncertain slide boundaries before treating the rendered video as final.

## Reference(s):

- [whisper.cpp ggml-small model download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and CSV examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce working files such as slide outlines, transcripts, slide timing CSVs, ffconcat files, and rendered MP4 videos when the agent runs the described local tools.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
