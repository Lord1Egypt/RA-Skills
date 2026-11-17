## Description:

Grago delegates web, API, and local data fetching to local LLMs for research tasks, helping agents save cloud tokens while keeping analysis on the user's machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solsuk](https://clawhub.ai/user/solsuk)

### License/Terms of Use:

Single-user license

## Use Case:

Developers and OpenClaw users use Grago to fetch live web, API, RSS, log, or local-file data and pass it to a local Ollama-compatible model for concise research analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grago gives an agent broad shell, file, network, and installer authority on the user's machine.

Mitigation: Install only on a dedicated, trusted single-user machine where the user accepts shell commands running with their user permissions.

Risk: Prompt injection or a compromised agent could cause arbitrary command execution through Grago's command-running design.

Mitigation: Do not use Grago with public-facing, multi-tenant, shared, or untrusted agents, and review commands before execution.

Risk: Research sources and API configuration can send data to unintended endpoints if configured carelessly.

Mitigation: Review sources.yaml and keep api_base pointed at localhost unless intentionally sending data elsewhere.

Risk: The bundled installer can install Ollama through a curl-to-shell path on non-macOS systems.

Mitigation: Prefer installing Ollama through a trusted package manager before running Grago's installer.

## Reference(s):

- [ClawHub Grago skill page](https://clawhub.ai/solsuk/skills/grago)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [Ollama](https://ollama.ai)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, or plain text returned from a local model, with shell commands and YAML configuration used for setup and sources.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input is truncated according to max_input_chars and output_format may be configured as markdown, json, or text.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
