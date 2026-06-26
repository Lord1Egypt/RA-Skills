## Description: <br>
Use the Phaya SaaS backend to generate images, videos, audio, music, and run LLM chat completions via simple REST API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boombignose](https://clawhub.ai/user/boombignose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to instruct an agent to call the Phaya REST API for paid image, video, audio, music, embedding, subtitle, download, and chat-completion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation endpoints use a paid credit system and successful jobs can deduct real credits. <br>
Mitigation: Use a scoped or low-balance API key, check endpoint costs before submitting jobs, and start with a low-cost request to verify connectivity. <br>
Risk: Prompts, files, media URLs, and chat content are sent to Phaya and may be processed by downstream providers. <br>
Mitigation: Avoid confidential or regulated data unless Phaya and its downstream providers meet the user's privacy and compliance requirements. <br>
Risk: Video downloading can raise permission, policy, or content-rights concerns. <br>
Mitigation: Use video-download workflows only when the user explicitly requests them and the source content is permitted for that use. <br>


## Reference(s): <br>
- [Phaya Media API on ClawHub](https://clawhub.ai/boombignose/phaya) <br>
- [README.md](README.md) <br>
- [Endpoint reference](endpoints.md) <br>
- [Usage examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with Python and curl examples, JSON request and response shapes, and environment variable setup instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs commonly include asynchronous job creation calls, polling instructions, media URLs, character IDs, chat text, and credit-balance checks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
