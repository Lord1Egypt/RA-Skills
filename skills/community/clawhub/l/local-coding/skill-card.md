## Description:

Local coding assistant that routes code generation, review, refactoring, and debugging requests to open-source coding models running across a user's device fleet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure and operate local coding models for code generation, review, refactoring, debugging, and integration with OpenAI-compatible coding tools while keeping prompts and code on their local network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the local fleet package may expose users to ordinary package-install and local-service risks.

Mitigation: Install only if the ollama-herd package and local devices are trusted, prefer a virtual environment, avoid running pip as root or administrator, and consider pinning a reviewed package version.

Risk: Prompts, code snippets, traces, audio files, and image prompts may be handled by the local router and fleet logs.

Mitigation: Review local logging behavior and avoid submitting sensitive material unless the local fleet and log storage are appropriate for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/local-coding)
- [ollama-herd GitHub Repository](https://github.com/geeks-accelerator/ollama-herd)
- [ollama-herd PyPI Package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local API requests, IDE configuration guidance, and model selection recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
