## Description: <br>
Analyze music and audio files locally without external APIs, producing tempo, groove, structure, harmony, timbre, temporal mood-energy, instrument, and lyric-aware emotional analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Adam-Researchh](https://clawhub.ai/user/Adam-Researchh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, producers, and reviewers use this skill to inspect local audio files, compare mixes, understand musical structure, and generate producer-facing notes without sending audio to external APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local media processing depends on ffmpeg, ffprobe, Python packages, and optional Whisper binaries or models, which can add supply-chain and file-handling risk. <br>
Mitigation: Use trusted, maintained installations, process only user-selected audio, and keep downloaded media, temporary files, and generated reports in a dedicated workspace. <br>
Risk: Tempo, swing, structure, instrument, lyric, and emotion reads are approximate analyses and may be misleading for ambiguous audio or transcription errors. <br>
Mitigation: Treat reports as decision support, review the source audio and generated notes, and validate important conclusions with human listening. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Adam-Researchh/music-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports, optional JSON reports, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on user-provided audio files and may write report files when an output path is supplied.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
