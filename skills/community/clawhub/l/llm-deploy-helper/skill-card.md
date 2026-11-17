## Description:

Detects local hardware, recommends local LLM deployment engines and models, and generates Docker Compose or systemd configuration for Ollama, vLLM, and llama.cpp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess local hardware for LLM serving and generate deployment recommendations and service configuration for Ollama, vLLM, or llama.cpp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Docker Compose or systemd service files can create persistent local LLM services with exposed API ports.

Mitigation: Inspect generated docker-compose.yml and .service files before running them, bind services to localhost unless remote access is intentionally secured, and review persistence settings before enabling services.

Risk: Deployment commands may rely on container images, model identifiers, or source installs that are not pinned.

Mitigation: Install only from a pinned release or commit and confirm container image and model provenance before deployment.

Risk: vLLM deployments may pass HF_TOKEN into containers.

Mitigation: Protect any HF_TOKEN value and avoid logging, committing, or broadly exposing generated environment configuration.

Risk: Generated systemd services may run Docker with elevated local privileges.

Mitigation: Review root privileges, cleanup behavior, and service enablement steps before installing or starting generated units.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/llm-deploy-helper)
- [Project homepage from metadata](https://github.com/minirr890112-byte/llm-deploy-helper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text with shell commands, Docker Compose YAML, and systemd unit content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local hardware recommendations, model and engine choices, generated service configuration, and follow-up commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
