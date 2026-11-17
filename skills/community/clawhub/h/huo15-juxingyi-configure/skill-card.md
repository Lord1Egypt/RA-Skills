## Description:

Configures OpenClaw to use the Juxingyi provider by fetching the live /v1/models list with a user-supplied fsk key and writing the resulting provider, primary model, fallbacks, and aliases to openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to configure, update, inspect, and switch Juxingyi text-model entries in their local OpenClaw configuration. It is intended for users who already have a Juxingyi account and fsk-format API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default flow can expose the Juxingyi API key through command-line history, plaintext openclaw.json, and backup files.

Mitigation: Prefer the documented --env workflow or another secret-store workflow, avoid putting real keys in shared logs or prompts, restrict permissions on configuration and backup files, and rotate exposed keys.

Risk: The script changes OpenClaw model defaults and the fireworks-hub provider configuration.

Mitigation: Review the generated configuration before use, keep the automatic backups, and restore from backup if the provider, primary model, or fallbacks are not suitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-juxingyi-configure)
- [Juxingyi API documentation](https://fireworks-simulator.huo15.com/docs.html)
- [Juxingyi console](https://fireworks-simulator.huo15.com/app/)
- [User guide](docs/user-guide.md)
- [Developer guide](docs/dev-guide.md)
- [Changelog](docs/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local OpenClaw configuration changes through a Node.js script and reports model, backup, update, or switch status to the user.]

## Skill Version(s):

1.3.0 (source: frontmatter, changelog, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
