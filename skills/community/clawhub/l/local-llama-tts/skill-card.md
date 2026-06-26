## Description: <br>
Local text-to-speech using llama-tts (llama.cpp) and OuteTTS-1.0-0.6B model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuxxin](https://clawhub.ai/user/wuxxin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to synthesize speech locally with llama-tts and the OuteTTS model. It provides guidance and a shell wrapper for producing WAV audio from text with configurable output, speaker reference, and temperature settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local shell wrapper and llama-tts binary, and the security guidance notes user-controlled paths should be reviewed for safe quoting. <br>
Mitigation: Review scripts/tts-local.sh before use, prefer trusted local model and speaker files, and quote or harden user-controlled file paths before running it in shared or automated environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuxxin/local-llama-tts) <br>
- [OuteTTS-1.0-0.6B GGUF model](https://huggingface.co/OuteAI/OuteTTS-1.0-0.6B-GGUF/resolve/main/OuteTTS-1.0-0.6B-Q4_K_M.gguf?download=true) <br>
- [WavTokenizer vocoder model](https://huggingface.co/ggml-org/WavTokenizer/resolve/main/WavTokenizer-Large-75-Q5_1.gguf?download=true) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local text-to-speech workflow guidance and references a script that writes WAV audio through llama-tts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
