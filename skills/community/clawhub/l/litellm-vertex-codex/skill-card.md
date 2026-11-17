## Description:

Configure OpenAI Codex CLI to use Vertex AI Gemini models via LiteLLM. A guide for translating strict Codex requests for Gemini compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhrum](https://clawhub.ai/user/bhrum)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Codex CLI to route requests to Vertex AI Gemini models through a local LiteLLM proxy. It provides setup, verification, and troubleshooting guidance for compatibility between Codex's expected OpenAI-style responses interface and Gemini-backed model endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide changes persistent Codex and shell configuration, including model provider settings, local proxy routing, workspace trust, and an OPENAI_API_KEY placeholder.

Mitigation: Review each path, trust setting, endpoint, and shell-profile change before applying it; keep only settings that match the intended workspace and credential flow.

Risk: The setup relies on Vertex AI credentials and a local LiteLLM proxy, so misconfiguration can route requests to the wrong project, model, or endpoint.

Mitigation: Verify the GCP project, Vertex AI location, LiteLLM model aliases, and local base URL before running Codex against sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bhrum/skills/litellm-vertex-codex)
- [Publisher profile](https://clawhub.ai/user/bhrum)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML, TOML, and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces manual setup guidance for Codex CLI, LiteLLM, Vertex AI credentials, and local verification.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
