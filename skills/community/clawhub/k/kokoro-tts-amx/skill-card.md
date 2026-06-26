## Description: <br>
Local Kokoro-82M text-to-speech on Intel CPU with bf16 autocast and oneDNN AMX-BF16 acceleration that synthesizes Chinese, English, Japanese, French, Spanish, Hindi, Italian, and Portuguese speech to 24 kHz mono WAV without a cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wray151](https://clawhub.ai/user/wray151) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate local multilingual narration, dubbing, and speech synthesis from text on compatible Intel CPU systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can change local system packages, create a Python virtual environment, install PyPI dependencies, and download the Kokoro model into the Hugging Face cache. <br>
Mitigation: Review install.sh and requirements.txt first, run installation in a controlled environment, and approve system package, PyPI, and model downloads before use. <br>
Risk: The remote one-line installer path executes a downloaded shell script. <br>
Mitigation: Prefer cloning the repository, reviewing a pinned revision, and running install.sh locally instead of piping curl output to bash. <br>
Risk: The installer replaces any existing kokoro-tts-amx skill directory at the target location. <br>
Mitigation: Back up or move any existing kokoro-tts-amx skill directory before running the installer. <br>


## Reference(s): <br>
- [Kokoro-82M voices](https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated audio is a 24 kHz mono WAV file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default audio output is output.wav unless the user supplies another --output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
