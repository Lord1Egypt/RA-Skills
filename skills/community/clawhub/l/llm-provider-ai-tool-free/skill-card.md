## Description: <br>
Lightweight OpenAI API calling guidance for chat completions, file management, embeddings, assistants, and image generation for personal developer integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure and issue external LLM API requests for chat, embeddings, file upload and search, assistant workflows, and image generation from shell, Python, or Node.js examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, metadata, and uploaded files may be sent to an external LLM API. <br>
Mitigation: Avoid sensitive or regulated data unless the use is approved, and use an approved provider configuration. <br>
Risk: API keys are required for the external service. <br>
Mitigation: Use scoped credentials, store keys outside source files, and rotate or revoke credentials when no longer needed. <br>
Risk: Generated text or images can be inaccurate or unsuitable for high-stakes use. <br>
Mitigation: Review outputs before use and avoid medical, legal, or other critical decision workflows without qualified oversight. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/llm-provider-ai-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, Python, and Node.js code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request examples, environment variable setup, error-handling guidance, and upgrade notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, evidence release, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
