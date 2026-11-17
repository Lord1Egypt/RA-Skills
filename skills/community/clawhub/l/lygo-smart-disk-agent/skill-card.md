## Description:

LYGO SMART DISK AGENT provides a lean localhost control portal for a local Ollama-backed assistant with P0-P5 kernel checks, local operator token authentication, and no HTTP chat-memory export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local AI operators use this skill to install and run a lightweight, offline-first disk agent that serves a localhost portal backed by host Ollama for chat, status, and constrained local limbs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local operator token can expose the localhost API if it is shared or stored insecurely.

Mitigation: Keep the generated token private, run the skill as an unprivileged local user, and protect the local data directory.

Risk: Disabling token authentication or allowing LAN binding increases exposure beyond the intended local service model.

Mitigation: Keep auth.required enabled and avoid LAN binding unless the operator has explicitly accepted and mitigated the network exposure.

Risk: Installer and local-service behavior can affect files under the skill's data directory.

Mitigation: Use a pinned installer version where practical and review local data-file writes before deploying in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-smart-disk-agent)
- [LYGO Protocol Stack](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [LYGO Smart Disk Source Tree](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/lygo_smart_disk)
- [Security Reference](artifact/references/SECURITY.md)
- [SkillSpector Audit](artifact/references/SKILLSPECTOR_AUDIT.md)
- [Quick Start](artifact/references/QUICK.md)
- [Model Selection](artifact/public/docs/06_MODEL_SELECTION.md)
- [Capacity and Old-Tech Performance](artifact/public/docs/07_CAPACITY_AND_OLD_TECH.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, local portal responses, and JSON HTTP responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core operation depends on a host Ollama service and local model availability; chat metadata is stored as hashes and lengths only.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
