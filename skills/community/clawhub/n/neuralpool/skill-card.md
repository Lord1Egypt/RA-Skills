## Description:

Monetize idle LLM API capacity or access 100+ models through a unified OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuralpool](https://clawhub.ai/user/neuralpool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and node operators use this skill to install and configure a NeuralPool node, monetize upstream LLM API capacity, or consume NeuralPool through an OpenAI-compatible API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may execute remote code and install a downloaded binary system-wide.

Mitigation: Avoid curl | bash, inspect the installer first, pin a specific release, and verify any published checksums or signatures before installation.

Risk: The node handles local provider API keys, prompts, responses, billing data, and a NeuralPool auth token.

Mitigation: Run it only in an environment where NeuralPool and configured upstream providers are trusted, and use least-privilege credentials where available.

Risk: Default installation may require writing to /usr/local/bin with sudo.

Mitigation: Prefer a user-owned INSTALL_DIR when possible to reduce the blast radius of installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/neuralpool/skills/neuralpool)
- [NeuralPool website](https://neuralpool.ai)
- [NeuralPool documentation](https://neuralpool.ai/docs)
- [NeuralPool registration](https://neuralpool.ai/register)
- [Manual binary downloads](https://github.com/neuralpool/neuralpool-node/releases)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installer commands, node setup steps, start commands, and OpenAI-compatible API examples.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
