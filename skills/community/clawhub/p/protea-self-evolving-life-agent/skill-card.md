## Description:

Protea is a self-evolving artificial life agent that uses a three-ring architecture for supervision, LLM-driven evolution, and evolvable code with fitness scoring, memory, skill crystallization, Telegram interaction, and a local dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edisonchenai](https://clawhub.ai/user/edisonchenai)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up and operate a local self-evolving agent that mutates code with LLM assistance, tracks fitness, rolls back failures, and exposes interaction through Telegram and a local web dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged suspicious because it describes a self-changing AI program and recommends running an unverified remote installer.

Mitigation: Review and pin the installer before execution; do not use the one-line curl-to-bash command directly.

Risk: The agent uses LLM API keys and local persistence, which can expose sensitive credentials or state if run in a broad user environment.

Mitigation: Run as an unprivileged user in a disposable directory or container and provide only the credentials strictly required for testing.

Risk: Self-modifying code can introduce unwanted behavior even when rollback and fitness checks are present.

Mitigation: Inspect generated mutations, retain Git snapshots, and deploy only after review and security scanning.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edisonchenai/skills/protea-self-evolving-life-agent)
- [Protea GitHub Repository](https://github.com/EdisonChenAI/protea)
- [Remote Setup Script](https://raw.githubusercontent.com/EdisonChenAI/protea/main/setup.sh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides local execution of a self-modifying agent that uses LLM API keys, Git snapshots, local persistence, Telegram integration, and a localhost dashboard.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
