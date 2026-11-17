## Description:

LYGO CLI Bridge provides a unified Python CLI entrypoint for LYGO health, map, analyze, mint, radar, next, and version workflows, using optional companion skills without subprocess execution or auto-publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and engineers use this skill to run local LYGO command workflows from one CLI entrypoint, including public health checks, ecosystem mapping, text analysis, mint guidance, radar feed generation, and roadmap status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can load companion Python code from mutable or environment-directed locations.

Mitigation: Install companion skills from trusted releases, verify their provenance before use, and avoid setting LYGO_STACK_ROOT to directories writable by other users or automation.

Risk: The analyze command can process user-supplied text files.

Mitigation: Do not pass private mail, logs, or other sensitive text unless the user has consented and the environment is appropriate for that data.

Risk: The skill documentation includes @latest install commands.

Mitigation: Pin or otherwise verify package versions for trusted workflows instead of copying @latest commands into sensitive environments.

## Reference(s):

- [Security guidance](references/SECURITY.md)
- [Quickstart](examples/quickstart.md)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-cli-bridge)
- [ClawHub publisher profile](https://clawhub.ai/user/deepseekoracle)
- [Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-cli-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands can read local text or pack files, perform allowlisted HTTPS health checks, or write JSON and HTML artifacts only when the user passes explicit consent flags.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
