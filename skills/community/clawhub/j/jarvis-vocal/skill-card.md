## Description: <br>
Authentic J.A.R.V.I.S. voice synthesis using Piper TTS with HuggingFace-trained model. Generates movie-accurate voice locally and can push to connected Android devices via OpenClaw nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kishen35](https://clawhub.ai/user/kishen35) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate local J.A.R.V.I.S.-style speech with Piper TTS and optionally send announcements to trusted Android devices over ADB. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup depends on upstream Piper TTS, HuggingFace CLI, ffmpeg, and a downloaded voice model. <br>
Mitigation: Verify those upstream packages and model sources before installing or running the workflow. <br>
Risk: ADB pairing permits file pushes and playback actions on connected Android devices. <br>
Mitigation: Use ADB only with trusted devices and review pairing state before sending generated audio. <br>
Risk: The artifact references jarvis-speak and jarvis-tts wrapper commands that are not included in the scanned files. <br>
Mitigation: Review any local wrapper scripts with those names before adding them to the workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kishen35/jarvis-vocal) <br>
- [jgkawell/jarvis Hugging Face model](https://huggingface.co/jgkawell/jarvis) <br>
- [jgkawell/jarvis discussions](https://huggingface.co/jgkawell/jarvis/discussions) <br>
- [Piper TTS](https://github.com/rhasspy/piper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce WAV audio files locally and can optionally push audio to a paired Android device via ADB.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
