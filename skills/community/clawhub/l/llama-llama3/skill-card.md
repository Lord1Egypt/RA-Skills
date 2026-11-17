## Description:

Llama 3 by Meta routes Llama 3.3, Llama 3.2, and Llama 3.1 requests across a local device fleet through an OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate ollama-herd as a local fleet router for Llama models, choose model sizes that fit available hardware, and call the fleet through curl or OpenAI-compatible examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned PyPI package can introduce supply-chain risk.

Mitigation: Use a virtual environment, avoid root or administrator shells, and pin or review the ollama-herd package version before installation.

Risk: Prompts, audio files, traces, and logs may be visible to devices participating in the local fleet.

Mitigation: Do not send sensitive prompts or audio files unless every fleet device and its local logs are trusted.

Risk: Large Llama models can consume substantial storage and memory.

Mitigation: Confirm downloads before pulling models, choose smaller variants when hardware is insufficient, and keep model deletion user-confirmed.

## Reference(s):

- [Skill page](https://clawhub.ai/twinsgeeks/skills/llama-llama3)
- [ollama-herd project](https://github.com/geeks-accelerator/ollama-herd)
- [ollama-herd PyPI package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with shell, Python, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local service endpoints, model sizing guidance, fleet monitoring commands, and guardrails for model downloads and local files.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
