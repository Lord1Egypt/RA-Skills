## Description: <br>
Create a local, speaker-separated plain text transcript from a meeting recording, speech audio file, or local video/audio file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henrCh1](https://clawhub.ai/user/henrCh1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert local meeting audio or video into timestamped plain text transcripts with speaker labels. It is suited for transcription workflows where the user supplies a local source file path and an output file or directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill may contact ModelScope to fetch a speaker model if the model is not already cached, despite presenting the workflow as fully local. <br>
Mitigation: For private or offline meetings, preinstall and verify all required models, then block network access during transcription runs. <br>
Risk: The skill runs a local Python and FFmpeg media-processing pipeline on files selected by the user. <br>
Mitigation: Run it only on trusted local files and review the requested output path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/henrCh1/meeting-to-text) <br>
- [Runtime Paths](artifact/references/runtime_paths.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [Evaluation Scenarios](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text transcript files, JSON run results, and concise agent status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript entries include timestamps and speaker labels such as \u8bf4\u8bdd\u4eba1. The final machine-readable result is the last non-empty stdout line.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
