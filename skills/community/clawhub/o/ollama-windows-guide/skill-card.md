## Description:

Complete Windows setup guide for Ollama: installation, CORS header fix for web apps, custom model creation with Modelfiles, and integration with desktop AI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and Windows users use this skill to install Ollama, configure browser access for local web apps, create custom Modelfile-based models, and troubleshoot common local AI setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wildcard CORS origin guidance can allow any website to reach a local Ollama service if the setting is made permanent.

Mitigation: Use an exact trusted origin for the local web UI, keep wildcard origins temporary for troubleshooting, and remove persistent OLLAMA_ORIGINS=* settings after use.

## Reference(s):

- [Ollama](https://ollama.com)
- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/ollama-windows-guide)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell, bash, and Modelfile snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; does not execute commands or call external services by itself.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
