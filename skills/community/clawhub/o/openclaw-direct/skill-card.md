## Description:

One-click OpenClaw installer with security hardening. No Docker required - runs directly on Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningtoba](https://clawhub.ai/user/ningtoba)

### License/Terms of Use:


## Use Case:

Developers and operators use this installer to set up OpenClaw without Docker, create a local configuration, connect an LLM endpoint, and start the OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer performs high-impact system and supply-chain actions, including global npm installs, fetching Ollama, pulling a model, installing additional skills, and starting local services.

Mitigation: Review setup.sh before installing, install Ollama manually when possible, and pin or verify package and model versions before use.

Risk: The optional firewall step may make system-level firewall changes.

Mitigation: Skip unneeded firewall changes and do not accept the firewalld change unless it has been reviewed for the target host.

Risk: The generated ~/.openclaw/openclaw.json file can contain gateway tokens and API keys.

Mitigation: Treat the configuration file as sensitive, restrict access to it, and back it up before using the documented rm -rf uninstall command.

Risk: The security verdict for this release is suspicious.

Mitigation: Avoid running the automatic installer as-is on a primary machine; test in a disposable or isolated environment first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningtoba/skills/openclaw-direct)
- [Node.js](https://nodejs.org)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local installer guidance and configuration for OpenClaw setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
