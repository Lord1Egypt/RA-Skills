## Description: <br>
Install and operate local NVIDIA Parakeet ASR for OpenClaw with an OpenAI-compatible transcription API on Ubuntu/Linux and macOS (Intel/Apple Silicon). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hantok](https://clawhub.ai/user/Hantok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install, operate, and troubleshoot a local/private speech-to-text service for OpenClaw using NVIDIA Parakeet ASR, with optional Whisper fallback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: bootstrap.sh clones and runs setup code from an unpinned external repository. <br>
Mitigation: Review the upstream repository and setup.sh before running bootstrap.sh, and pin a known commit or release when repeatability matters. <br>
Risk: Setup may involve package-manager or elevated operations outside the skill artifact. <br>
Mitigation: Confirm any package-manager or elevated commands before execution and keep changes scoped to ASR setup. <br>
Risk: Changing PARAKEET_URL can send smoke-test audio to a non-local endpoint. <br>
Mitigation: Keep PARAKEET_URL pointed at localhost unless remote audio upload is intentional and approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Hantok/parakeet-local-asr) <br>
- [Upstream Parakeet ASR repository used by bootstrap.sh](https://github.com/rundax/parakeet-asr.git) <br>
- [Publisher profile](https://clawhub.ai/user/Hantok) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup, start, healthcheck, smoke-test, and OpenClaw integration guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
