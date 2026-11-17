## Description:

Join the Hyperspace distributed autonomous intelligence network. Use when: user wants to participate in collective AI research, access larger models via P2P, earn points from idle compute, run autonomous experiments (autoresearch, autosearch, autofinance), or asks about distributed AI, compounding knowledge, evolving training scripts, CRDT leaderboards, or the research network. Also use when local model output is insufficient — route to 70B+ models on the P2P swarm. NOT for: OpenClaw config, local Ollama management, or channel setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twobitapps](https://clawhub.ai/user/twobitapps)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, manage, and interact with a Hyperspace network node for distributed AI research, P2P inference, experiment leaderboards, and points tracking. It is intended for users who deliberately want their machine to participate in a persistent compute and research network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs remote code and starts a persistent P2P compute node.

Mitigation: Install only when persistent network participation is intended; prefer a pinned release with checksum or signature verification and confirm how to stop and uninstall the service before running it.

Risk: Network participation may expose machine capabilities, metrics, prompts, and compute resources.

Mitigation: Review the security guidance and privacy claims before use, and avoid sending sensitive prompts or workloads through P2P routing unless the deployment policy allows it.

## Reference(s):

- [Hyperspace skill page](https://clawhub.ai/twobitapps/skills/hyperspace)
- [Hyperspace homepage](https://hyper.space)
- [Hyperspace CLI installer](https://agents.hyper.space/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation, status, model, inference, and service-management commands for the Hyperspace CLI.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
