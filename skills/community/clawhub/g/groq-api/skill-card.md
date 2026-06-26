## Description: <br>
Build and debug Groq API chat and speech workflows with low-latency routing, structured outputs, and production-safe patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build, integrate, and troubleshoot Groq API inference for chat, tool calling, structured responses, and speech transcription. It helps shape requests, select available models, verify credentials, and apply retry, fallback, and output-validation patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and requested audio transcription inputs are sent to Groq inference endpoints. <br>
Mitigation: Use the skill only for intended Groq workflows, avoid sensitive or unconsented audio, and confirm what data is being sent before making API calls. <br>
Risk: API credentials could be exposed if copied into files, logs, or shared troubleshooting output. <br>
Mitigation: Keep GROQ_API_KEY in the environment, never store it in project files, and sanitize troubleshooting reports before sharing them. <br>
Risk: Saved preferences or debug notes under ~/groq-api/ could retain sensitive workflow context. <br>
Mitigation: Record routing logic instead of private payloads and periodically review local memory and logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/groq-api) <br>
- [Groq API Base URL](https://api.groq.com/openai/v1) <br>
- [Groq Models Endpoint](https://api.groq.com/openai/v1/models) <br>
- [Groq Chat Completions Endpoint](https://api.groq.com/openai/v1/chat/completions) <br>
- [Groq Audio Transcriptions Endpoint](https://api.groq.com/openai/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Groq API request payloads, model-routing notes, retry guidance, and local memory setup instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
