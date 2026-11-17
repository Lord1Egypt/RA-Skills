## Description:

Set up, diagnose, repair, and quality-test private local OpenClaw semantic memory search using Ollama embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brasco05](https://clawhub.ai/user/brasco05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose and configure private local OpenClaw memory search with Ollama embeddings, then validate semantic retrieval quality before relying on memory_search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer path can run Ollama installation commands, including a Linux curl-to-shell vendor installer, when --install is used.

Mitigation: Review the installer before use and run default diagnostic mode first; use --install only after explicit approval or replace it with a verified manual install.

Risk: Changing the Ollama base URL can direct memory-search traffic away from the default local endpoint.

Mitigation: Keep the base URL on localhost unless the destination has been independently validated and is on a trusted private network.

Risk: Applying configuration persists the memory-search endpoint and model settings.

Mitigation: Use --apply-config only after confirming the intended OpenClaw configuration changes and validating the selected model and endpoint.

## Reference(s):

- [Troubleshooting - Ollama Memory Setup](references/troubleshooting.md)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend diagnostic checks, optional installation, OpenClaw memory configuration, reindexing, and quality-test commands.]

## Skill Version(s):

1.2.3 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
