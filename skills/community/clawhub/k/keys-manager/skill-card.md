## Description:

Manage API keys and secrets locally from the terminal using the `keys` CLI, including storage, retrieval, search, import, export, `.env` file operations, profile isolation, and secure key workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stym06](https://clawhub.ai/user/stym06)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage local API keys and secrets with the `keys` CLI, including storing, retrieving, importing, exporting, injecting, auditing, profiling, and syncing secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages sensitive credentials and may print or expose secrets to terminal output.

Mitigation: Review commands before execution, avoid `eval $(keys expose)`, and prefer masked or scoped retrieval workflows when possible.

Risk: Generated `.env` files can persist secrets on disk or be committed accidentally.

Mitigation: Protect generated `.env` files with restrictive file permissions and `.gitignore` entries.

Risk: The skill depends on a third-party `keys` CLI that handles credentials.

Mitigation: Install only a pinned, trusted version of the CLI before using this skill with real secrets.

Risk: Secret sync can transfer credentials between machines over a local or reachable network.

Mitigation: Sync secrets only between trusted machines on trusted networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stym06/skills/keys-manager)
- [Publisher profile](https://clawhub.ai/user/stym06)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that read, write, print, export, inject, audit, or sync local secrets through the `keys` CLI.]

## Skill Version(s):

0.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
