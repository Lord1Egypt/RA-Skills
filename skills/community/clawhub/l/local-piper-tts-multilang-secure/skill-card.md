## Description: <br>
Generates local offline text-to-speech audio with Piper TTS, automatic language detection, per-call voice selection, and workspace file output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szafranski](https://clawhub.ai/user/szafranski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to synthesize local OGG or WAV speech from text, manage Piper voices, and keep generated audio in the OpenClaw workspace for attachment or sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup and voice installation require external downloads from PyPI and HuggingFace. <br>
Mitigation: Run setup or voice downloads only after user confirmation, keep OpenClaw current, and rely on the skill's HTTPS-only and isolated-venv behavior. <br>
Risk: Generated audio may preserve sensitive text as local files in the OpenClaw workspace. <br>
Mitigation: Avoid synthesizing sensitive text unless local retention is acceptable, and delete generated audio when it is no longer needed. <br>
Risk: Voice models and generated audio can consume local disk space. <br>
Mitigation: Use the documented voice removal flow for unused models and clean up generated workspace audio as needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szafranski/local-piper-tts-multilang-secure) <br>
- [Piper voice model catalog](https://github.com/rhasspy/piper/blob/master/VOICES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [OGG/Opus or WAV audio files with JSON-style status objects and concise setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes audio under OPENCLAW_WORKSPACE/tts or ~/.openclaw/workspace/tts; model downloads occur only during setup and voice installation.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
