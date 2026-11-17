## Description:

Set up PixelVault CLI by installing the CLI and configuring API key authentication for image hosting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[facundofarias](https://clawhub.ai/user/facundofarias)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users use this skill when they need PixelVault CLI installed, authenticated, and verified before uploading images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation can install or update executable code from an external package source.

Mitigation: Verify the PixelVault CLI package and publisher before installation and avoid running the install with elevated privileges.

Risk: API keys can be exposed through shell history, shared shell profiles, or committed configuration files.

Mitigation: Prefer safer secret storage or a local untracked environment file, and avoid pasting live keys into shared files or command histories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/facundofarias/skills/pixelvault-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
