## Description: <br>
Multi-role audio generator skill v1.0.1 全家桶版 - Universal professional tool for creating dialogue audio with multiple character voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsun4414](https://clawhub.ai/user/johnsun4414) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content teams use this skill to turn multi-character dialogue scripts into role-separated and merged speech audio with configurable voices and spatial positioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation may make privileged system changes and can invoke Homebrew's remote installer path. <br>
Mitigation: Review install.sh before use, install ffmpeg and edge-tts manually when possible, and avoid the Homebrew curl-to-bash path unless it is trusted in the target environment. <br>
Risk: Dialogue text is sent to Microsoft Edge TTS, creating privacy exposure for sensitive scripts. <br>
Mitigation: Do not submit private, regulated, or proprietary dialogue text unless use of Microsoft Edge TTS is approved for that data. <br>
Risk: The bundled shell generator appears incomplete, which may cause reliability issues. <br>
Mitigation: Prefer the Python generator entry point and test with neutral sample dialogue before using the skill in a release workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/johnsun4414/multi-role-tts-skill) <br>
- [Usage guide](docs/usage-guide.md) <br>
- [Edge TTS project](https://github.com/rany2/edge-tts) <br>
- [FFmpeg documentation](https://ffmpeg.org/documentation.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate MP3 audio outputs using Edge TTS and FFmpeg when executed by the user or agent environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, package.json, and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
