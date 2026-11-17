## Description:

Configure OpenClaw's memory-lancedb plugin to enable local semantic vector memory using LanceDB and an OpenAI-compatible embedding provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssyvonne](https://clawhub.ai/user/ssyvonne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw semantic vector memory, install LanceDB dependencies, migrate selected MEMORY.md facts into vector recall, and troubleshoot common memory-lancedb setup failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory content may be embedded through an external provider and stored in a local vector database.

Mitigation: Store only non-secret memory content, do not store tokens or credentials, and consider a local embedding provider for confidential work.

Risk: Embedding API keys may be exposed through command history or broad reuse.

Mitigation: Use a dedicated low-quota API key, avoid placing keys in shell history, and rotate any key that may have been exposed.

Risk: The setup modifies a global OpenClaw installation and references unpinned npm package installs plus a direct native.js patch.

Mitigation: Review the patch before execution, back up the OpenClaw installation, and pin npm package versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssyvonne/skills/memory-lancedb-setup)
- [Troubleshooting: memory-lancedb](references/troubleshooting.md)
- [Apple Silicon LanceDB native patch script](references/patch_native.py)
- [Google AI Studio](https://aistudio.google.com)
- [Gemini OpenAI-compatible embedding endpoint](https://generativelanguage.googleapis.com/v1beta/openai/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands and a Python patch script reference]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and troubleshooting guidance for local OpenClaw vector memory; users provide their own embedding API key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
