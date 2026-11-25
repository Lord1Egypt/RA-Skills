## Description:

For developers and small teams running open-weight language models on their own machines or intranet: size models and quantization from a VRAM budget, verify downloads, deploy with Ollama or llama.cpp, expose an OpenAI-compatible endpoint, and assess throughput and sampled quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjianli0721](https://clawhub.ai/user/fengjianli0721)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and small teams use this skill to size, deploy, connect, and evaluate open-weight language models on a workstation or intranet. It produces a deployment and acceptance record with VRAM estimates, launch guidance, benchmark results, and rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment examples may expose inference services without authentication to reachable networks, allowing unintended use of compute resources or service disruption.

Mitigation: Keep the service bound to localhost unless remote access is required; for remote use, restrict access with network controls and authentication before making the endpoint reachable.

Risk: The security assessment is partial because some local references were missing, so it may not cover all behavior described by the skill.

Mitigation: Review the complete release artifacts and the deployment configuration before using it in a networked environment.

## Reference(s):

- [Hardware sizing and VRAM budget](artifact/references/hardware-sizing.md)
- [Model selection](artifact/references/model-selection.md)
- [Serving recipes](artifact/references/serving-recipes.md)
- [Benchmarking and quality checks](artifact/references/benchmarking.md)
- [ClawHub release page](https://clawhub.ai/fengjianli0721/skills/modeldeck-local)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration guidance, JSONL benchmark data]

**Output Format:** [Markdown deployment and acceptance report with runnable launch commands or scripts and JSONL benchmark records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hardware-specific VRAM estimates, endpoint checks, sampled quality results, and rollback guidance; performance estimates require measurement on the target machine.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
