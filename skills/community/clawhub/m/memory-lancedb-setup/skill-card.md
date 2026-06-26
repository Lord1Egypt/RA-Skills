## Description: <br>
Configure OpenClaw's memory-lancedb plugin to enable local semantic vector memory using LanceDB and an OpenAI-compatible embedding provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssyvonne](https://clawhub.ai/user/ssyvonne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure semantic vector memory, install LanceDB dependencies, configure an embedding provider, troubleshoot memory-lancedb errors, or migrate key facts from flat-file memory into vector recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persisted embedding API keys and semantic memory may expose secrets or live tokens to local storage or the configured embedding provider. <br>
Mitigation: Use a limited-scope embedding key, avoid storing secrets or live tokens in memory, and assume memory contents may be sent to the configured embedding provider. <br>
Risk: The patch script modifies installed OpenClaw and LanceDB files in place. <br>
Mitigation: Inspect the target file, create a rollback copy, and run the patch only after confirming the snippet and platform match. <br>
Risk: The setup installs npm packages into global OpenClaw locations. <br>
Mitigation: Pin or verify npm packages before installation and review package names for the target platform. <br>


## Reference(s): <br>
- [Troubleshooting: memory-lancedb](references/troubleshooting.md) <br>
- [Apple Silicon native.js patch script](references/patch_native.py) <br>
- [Google AI Studio](https://aistudio.google.com) <br>
- [Gemini OpenAI-compatible embedding endpoint](https://generativelanguage.googleapis.com/v1beta/openai/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform-specific setup commands, configuration values, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
