## Description:

Guides OpenClaw users through Windows-focused local embedding memory-search deployment, Nomic Atlas visualization, and troubleshooting for restricted network environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to deploy local embedding-backed OpenClaw memory search, configure related memory tooling, and troubleshoot setup issues in Windows and restricted network environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide includes steps to bypass centralized OpenClaw configuration and edit installed OpenClaw files.

Mitigation: Use those steps only in an authorized environment with administrator approval, and preserve centralized configuration policy unless that change has been explicitly approved.

Risk: Remote embedding configuration can expose memory data if endpoint privacy and retention terms are not understood.

Mitigation: Prefer local embedding for sensitive memory data, or confirm the remote endpoint's privacy, retention, and authorization rules before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/node-llama-cpp-install-guide)
- [nomic-embed-text v1.5 GGUF model mirror](https://hf-mirror.com/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q4_K_M.gguf)
- [Source skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with JSON, PowerShell, Bash, and batch snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment requirements, deployment checklist, validation commands, and troubleshooting notes.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
