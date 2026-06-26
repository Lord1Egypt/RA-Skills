## Description: <br>
Control local music playback with play, pause, resume, stop, status, and song listing commands from a configured music directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awspace](https://clawhub.ai/user/awspace) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to control local audio playback through shell commands, including starting playback, pausing, resuming, stopping, checking status, and selecting songs from a local directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented entry point depends on a play-music wrapper that is not present in the artifact file list. <br>
Mitigation: Verify that the wrapper is supplied elsewhere before installation or use. <br>
Risk: Installing pygame from an untrusted package source could introduce dependency risk. <br>
Mitigation: Install pygame only from a trusted Python package source. <br>
Risk: A broad MUSIC_DIR may expose unintended local audio files to playback commands. <br>
Mitigation: Keep MUSIC_DIR limited to the intended audio directory. <br>
Risk: A custom MUSIC_LOCK_FILE path could point at a sensitive or inappropriate file location. <br>
Mitigation: Do not set MUSIC_LOCK_FILE to sensitive paths. <br>
Risk: Troubleshooting with broad process-kill commands can stop unrelated processes. <br>
Mitigation: Prefer the documented server-stop command over broad pkill troubleshooting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/awspace/play-music) <br>
- [README](artifact/README.md) <br>
- [Setup Instructions](artifact/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target local audio files and a localhost playback server; playback depends on pygame and available music files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
