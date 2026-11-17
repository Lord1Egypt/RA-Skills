## Description:

Provision, inspect, and terminate disposable OpenNebula virtual machines through a restricted control plane API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktfh-claw](https://clawhub.ai/user/ktfh-claw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, inspect, and clean up short-lived OpenNebula virtual machines for isolated development, debugging, integration testing, package installation, and risky experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and hard-delete OpenNebula virtual machines through a control plane API.

Mitigation: Use a restricted OpenNebula account, confirm delete targets carefully, and treat deletion as irreversible.

Risk: Weak authentication, plain HTTP examples, and example passwords can expose VM lifecycle controls if copied into a networked deployment.

Mitigation: Use the API only on loopback or a strongly protected network, add authentication and TLS before exposing it, and replace all example passwords.

Risk: Command-line or JSON password examples can leak credentials through shell history, process lists, or configuration files.

Mitigation: Move passwords out of command arguments and static JSON config into a protected secret source.

## Reference(s):

- [API Reference](references/api.md)
- [Restricted User Setup Reference](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/ktfh-claw/skills/nebula-claw-developer)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API endpoint details, VM lifecycle results, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the API endpoint, VM name, template name, guest IP when available, operation result, and whether the VM was left running or destroyed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
