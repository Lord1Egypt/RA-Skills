## Description:

Share your idle Ollama inference with the community, or use community inference when your API credits run out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurejunk](https://clawhub.ai/user/futurejunk)

### License/Terms of Use:


## Use Case:

External developers and agent operators use IdleClaw to contribute idle local Ollama capacity to a community inference network, consume community-hosted Ollama responses, and check available models when their own API credits or local capacity are constrained.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, responses, model names, and contributor-node metadata pass through the IdleClaw routing service or a configured server.

Mitigation: Avoid sensitive prompts, use only trusted routing servers, and self-host the server path when privacy requirements demand it.

Risk: Plaintext http:// server URLs can expose inference traffic outside local development.

Mitigation: Use the default HTTPS endpoint or another HTTPS server for normal use; reserve plaintext HTTP for local development only.

Risk: The installer adds Python dependencies to the active environment.

Mitigation: Install and run the skill in a dedicated virtual environment after reviewing the dependency list.

Risk: Contribute mode shares locally available Ollama models for remote inference requests.

Mitigation: Run contribute mode only on machines and models intended for community sharing, and stop the process when sharing is no longer desired.

## Reference(s):

- [IdleClaw on ClawHub](https://clawhub.ai/futurejunk/skills/idleclaw)
- [IdleClaw security assessment](https://github.com/futurejunk/idleclaw/blob/main/security/SECURITY.md)
- [Ollama download](https://ollama.com/download)
- [Python downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime scripts stream plain text responses and status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Ollama; uses HTTP, HTTPS, WebSocket, or local Ollama endpoints configured by environment variables.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
