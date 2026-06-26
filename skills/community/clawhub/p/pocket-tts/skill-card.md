## Description: <br>
Generate high-quality English speech locally on CPU using Kyutai's Pocket TTS model, built-in voices, or a permitted custom voice sample. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sherajdev](https://clawhub.ai/user/sherajdev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add local English text-to-speech generation, choose preset voices, clone from an authorized WAV sample, and optionally run a local TTS server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup or first run may require downloads from the Pocket TTS package and Kyutai/Hugging Face model sources. <br>
Mitigation: Install only in an environment where those upstream sources are trusted, and plan for internet access before relying on offline runtime behavior. <br>
Risk: Voice cloning can use personal or third-party voice samples. <br>
Mitigation: Use custom WAV samples only with permission and review generated audio for consent, disclosure, and misuse concerns before distribution. <br>
Risk: The skill can start a local TTS server and write WAV files to user-selected paths. <br>
Mitigation: Start the server only when intended and choose output paths deliberately to avoid exposing services or overwriting files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sherajdev/pocket-tts) <br>
- [Kyutai Pocket TTS model card](https://huggingface.co/kyutai/pocket-tts) <br>
- [Kyutai Pocket TTS demo](https://kyutai.org/tts) <br>
- [Kyutai Pocket TTS GitHub repository](https://github.com/kyutai-labs/pocket-tts) <br>
- [Pocket TTS paper](https://arxiv.org/abs/2509.06926) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides generation of WAV audio files and optional local server use; the skill itself returns agent-facing instructions and commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
