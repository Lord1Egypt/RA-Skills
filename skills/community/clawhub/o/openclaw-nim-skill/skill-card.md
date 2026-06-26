## Description: <br>
Invoke various LLMs via the NVIDIA NIM API to save main agent tokens and use specialized model capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d-wwei](https://clawhub.ai/user/d-wwei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to delegate summarization, explanation, and reasoning prompts from OpenClaw or Claude Code to NVIDIA NIM-hosted models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill disables HTTPS certificate verification while sending the NVIDIA API key and prompts to NVIDIA, creating an interception risk. <br>
Mitigation: Fix TLS verification before sensitive use; until then, use only a limited NVIDIA API key, avoid untrusted networks, and do not send secrets, private source code, regulated data, or sensitive documents. <br>
Risk: Prompt text and any file content included in /nim requests are shared with an external provider. <br>
Mitigation: Review data handling requirements before use and keep confidential or regulated content out of prompts unless external processing is approved. <br>


## Reference(s): <br>
- [NVIDIA Build](https://build.nvidia.com/) <br>
- [NVIDIA NIM Chat Completions endpoint](https://integrate.api.nvidia.com/v1/chat/completions) <br>
- [ClawHub skill page](https://clawhub.ai/d-wwei/openclaw-nim-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Plain text model responses and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a selected model alias, sends the prompt to NVIDIA NIM, and requests up to 2048 tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
