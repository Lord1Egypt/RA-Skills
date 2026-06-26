## Description: <br>
Multi Edge Tts Cn converts Chinese text into speech with Microsoft Edge TTS voices and exports audio for Feishu, WeCom, and general file-based workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itian932](https://clawhub.ai/user/itian932) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and operations teams use this skill to generate Chinese voice messages or audio files from text, with configurable voices and output formats for Feishu and WeCom delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user-provided text to external speech or model services. <br>
Mitigation: Use it only with non-sensitive text and avoid confidential scripts, private business content, credentials, or regulated data. <br>
Risk: The skill can write audio output to caller-specified paths and may overwrite files if directed to an unsafe location. <br>
Mitigation: Keep output paths inside a dedicated workspace or approved media directory, and review requested paths before execution. <br>
Risk: The release was flagged for review by ClawHub security evidence. <br>
Mitigation: Review the skill before installation and run it in a constrained workspace with only the dependencies and network access needed for text-to-speech generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itian932/multi-edge-tts-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI and Python examples; generated skill output is an audio file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OGG, OPUS, AMR, MP3, WAV, FLAC, or AAC audio files; default output is an OGG file under /tmp/openclaw.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
