## Description: <br>
Local speech-to-text transcription with Qwen ASR, routed across a local Apple Silicon fleet for meetings, voice notes, podcasts, and recordings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to have an agent install, configure, call, and monitor local speech-to-text transcription for sensitive audio while keeping processing on trusted devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the PyPI package and model server introduces third-party package and model supply-chain risk. <br>
Mitigation: Verify the ollama-herd package and model installer sources before installing, and use trusted package indexes or pinned versions where possible. <br>
Risk: The local router may expose transcription and other AI endpoints if it binds outside localhost or a trusted network. <br>
Mitigation: Check how the router binds on the network before use, and only join devices you control or trust. <br>
Risk: Fleet Manager logs may contain sensitive usage metadata. <br>
Mitigation: Treat ~/.fleet-manager logs as sensitive and review them before sharing or retaining them outside trusted storage. <br>


## Reference(s): <br>
- [Local Transcription on ClawHub](https://clawhub.ai/twinsgeeks/local-transcription) <br>
- [ollama-herd package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume a local router at localhost:11435 and local audio processing; users should verify package and model sources and check network binding before installing.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
