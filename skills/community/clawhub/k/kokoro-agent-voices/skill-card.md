## Description: <br>
Local text-to-speech skill that gives agents distinct Kokoro TTS voice profiles and writes generated speech to WAV files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local Kokoro TTS voice output, list available voices, map named agent profiles to voices, and save synthesized speech as WAV audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The playback helper can turn a crafted output filename into a local shell command when --play is used. <br>
Mitigation: Review before installing or using, and avoid --play with untrusted or unusual output paths until playback uses a safe subprocess argument list. <br>
Risk: The first run performs outbound network access to download Kokoro model weights from Hugging Face Hub. <br>
Mitigation: Plan for the one-time model download and verify the deployment environment permits that fetch; subsequent TTS inference is documented as local. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/kokoro-agent-voices) <br>
- [Kokoro-82M model on Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline bash and Python examples; runtime script output includes console text and WAV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates 24 kHz WAV audio locally after the one-time Kokoro model download.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
