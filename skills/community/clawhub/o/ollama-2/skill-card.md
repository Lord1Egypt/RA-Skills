## Description:

Provides guidance and Python helper scripts for calling local or remote Ollama models through the Ollama API for text generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayflying](https://clawhub.ai/user/ayflying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure an Ollama host and model, send prompts through the Ollama generate API, and test connectivity before relying on local or trusted remote LLM inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to a non-local HTTP Ollama endpoint if the default or configured OLLAMA_HOST is not reviewed.

Mitigation: Set OLLAMA_HOST to localhost or a trusted HTTPS endpoint before sending sensitive prompts.

Risk: Installation guidance uses unpinned package commands, which can change dependencies over time.

Mitigation: Prefer pinned package versions or a reviewed lockfile for installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayflying/skills/ollama-2)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell examples; helper scripts return plain text responses or error strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OLLAMA_HOST and OLLAMA_MODEL environment variables; default behavior can send prompts to a configured HTTP Ollama endpoint.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
