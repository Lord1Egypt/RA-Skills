## Description: <br>
Analyzes local audio files to produce tempo, groove, structure, harmonic, timbre, mood, lyric, and timeline reports without external APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dahuangfortoby](https://clawhub.ai/user/dahuangfortoby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, producers, and music reviewers use this skill to inspect audio files, compare mixes, audit track structure, and generate producer-facing notes from local analysis outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled setup script makes persistent shell changes and performs a remote model download. <br>
Mitigation: Review setup.sh before use, run analysis scripts directly in a controlled environment when possible, and manually vet any ~/.zshrc alias changes. <br>
Risk: Dependency and model installation can change the local execution environment. <br>
Mitigation: Use an isolated virtual environment, pin dependencies, and verify the Whisper model download before running analysis on important files. <br>
Risk: Audio feature and lyric-based interpretations can be approximate or misleading. <br>
Mitigation: Treat tempo, structure, mood, swing, and lyric-derived readings as review aids and confirm conclusions with human listening. <br>


## Reference(s): <br>
- [Music Analysis Skill Page](https://clawhub.ai/dahuangfortoby/music-analysis-84) <br>
- [Whisper large-v3-turbo model artifact](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable text or JSON reports, with shell commands for running local analysis scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include snapshot, instrument, temporal journey, emotional read, lyrics, synthesis, and aligned timeline sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
