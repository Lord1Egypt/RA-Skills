## Description:

Persistent memory CLI for LLM agents. Store facts, recall past knowledge, link related memories, manage lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grivn](https://clawhub.ai/user/grivn)

### License/Terms of Use:


## Use Case:

Developers and LLM agent users use this skill to install and operate the mnemon CLI for persistent agent memory, including storing, recalling, linking, and lifecycle-managing memories across OpenClaw sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default setup runs mutable third-party code and installs persistent OpenClaw hooks and plugins outside the reviewed artifact.

Mitigation: Use a pinned, trusted mnemon release if available, inspect what `mnemon setup` will create before running it with `--yes`, and eject the integration when it is no longer needed.

Risk: Persistent memory can retain secrets or sensitive account data across future sessions.

Mitigation: Do not store secrets, passwords, tokens, or sensitive account data; review stored memories and delete unsuitable entries with mnemon lifecycle commands.

Risk: Installed hooks and plugins can modify OpenClaw behavior across future sessions.

Mitigation: Review the generated OpenClaw hook, plugin, prompt, and configuration files before enabling them, and use `mnemon setup --eject --target openclaw --yes` to remove the integration.

## Reference(s):

- [Mnemon Memory on ClawHub](https://clawhub.ai/grivn/skills/mnemon)
- [Publisher profile: grivn](https://clawhub.ai/user/grivn)
- [Go install package: github.com/mnemon-dev/mnemon](https://pkg.go.dev/github.com/mnemon-dev/mnemon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates through the external mnemon CLI; artifact guardrails cap each insight at 8,000 characters.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
