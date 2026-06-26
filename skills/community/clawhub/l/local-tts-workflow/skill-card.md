## Description: <br>
OpenClaw text-to-speech workflow for an OpenAI-compatible TTS server, including remote/self-hosted deployments such as vLLM Omni. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozi1924](https://clawhub.ai/user/mozi1924) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure, test, and debug OpenClaw text-to-speech integration with OpenAI-compatible TTS servers, including local and self-hosted deployments. It also guides preparation of text for speech by normalizing numbers before synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice recordings and transcripts used for consent-based cloning may contain sensitive personal data. <br>
Mitigation: Use trusted local or owned servers, obtain consent before uploading voices, and confirm how recordings and metadata are access-controlled and deleted. <br>
Risk: Incorrect request mode, voice, or reference-text settings can produce failed or misleading TTS behavior. <br>
Mitigation: Follow the documented test ladder, compare requests against the local OpenAPI schema, and verify direct server behavior before changing OpenClaw integration settings. <br>


## Reference(s): <br>
- [TTS API Calling Documentation](references/tts-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mozi1924/local-tts-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces diagnostic steps, request-shape guidance, and text-preparation guidance; it does not generate audio directly.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
